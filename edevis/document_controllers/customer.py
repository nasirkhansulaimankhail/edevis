import frappe
from frappe.utils import cint, cstr
from frappe.query_builder.functions import _max as get_max_value
from erpnext.selling.doctype.customer.customer import Customer as ERPNextCustomer

class Customer(ERPNextCustomer):

    #overrides existing autoname function in standard Customer Class from ERPNext
    def autoname(self):
        customer_id = 10000
        last_customer_id = self.get_last_customer_id()
        
        #validates if the max customer id is greater than 10000, as the 10000 is the starting ID for Customer
        if last_customer_id >= 10000:
            customer_id = last_customer_id + 1
        
        #sets customer ID
        self.name = cstr(customer_id)

    def get_last_customer_id(self):
        customer = frappe.qb.DocType("Customer")
        
        #returns the max customer ID using SQL MAX() function
        return cint(get_max_value(customer, "name", customer.name.regexp(r"1[0-9]{4}")))

    #overrides and inherits existing after_insert function in standard Customer Class from ERPNext
    def after_insert(self):
        super(Customer, self).after_insert()
        
        #gets default company
        company = frappe.defaults.get_global_default("company")

        #creates and links a debit account with the customer
        self.create_and_link_debit_account(self, company)
   

    def create_and_link_debit_account(self, company):
        
        #get the value for auto debit account creation from settings 
        create_debit_account = frappe.db.get_single_value("Edevis Settings", "auto_create_customer_accounts")

         #validates if auto debit account creation is enabled in the settings
        if create_debit_account:

            #create_debit_account() creates debit account as customer_id - customer_name - company_abbr eg. 10001 - Nasir Khan - NKC
            debit_account = self.create_debit_account(company)
            
            #links auto created debit account to the customer
            self.append("accounts", {
                "company": company,
                "account": debit_account
            })
            self.save()

    def create_debit_account(self, company):

        #gets Debitors Parent Account from Account Settings
        parent_account = frappe.db.get_single_value("Edevis Settings", "debitors_parent_account")
        
        #validates if Debitors Parent Account is setup in Account Settings
        if not parent_account:
            frappe.throw(
                "Failed to create Debit Account for this customer, please set up Debitors Parent Account in {}."
                .format(frappe.utils.get_link_to_form("Edevis Settings", "Edevis Settings"))
            )

            #logs error in case of missing Debitors Parent Account in the Account Settings.
            frappe.log_error(
                "Failed to create Debit Account for customer {} as no Debitors Parent Account is setup in the {}"
                .format(
                    frappe.utils.get_link_to_form("Customer", self.name), 
                    frappe.utils.get_link_to_form("Edevis Settings", "Edevis Settings")
                ), 
                "failed to create customer debit account"
            )
            return
        
        #sets account name using customer_id - customer_name - company_abbr eg. 10001 - Nasir Khan - NKC
        account_account_name = f"{self.name} - {self.customer_name}"
        try:
            #creates New Debit Account document in the system
            new_account_doc = frappe.get_doc({
                'doctype': 'Account',
                'account_name': account_account_name,
                'parent_account': parent_account,
                'company': company,
                'account_type': "Receivable"
            })
            new_account_doc.insert()

            #returns newly created Debit account name
            return new_account_doc.name
        
        #handles exception and logs error in case of failure while creating a debit account
        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(), 
                "something went wrong while creating debit account for {}"
                .format(frappe.utils.get_link_to_form("Customer", self.name))
            )