import frappe

class SalesController:
    def validate_vat(self):

        if self.tax_category in ["EU", "Inland"]:
            if not self.tax_id:
                frappe.msgprint("Im Kunden ist keine VAT ID hinterlegt")


    def check_vat(self):
        if self.tax_category in ["EU", "Inland"]:
            if not self.tax_id:
               frappe.throw("Im Kunden ist keine VAT ID hinterlegt")
        validate = False
        if self.tax_category == "EU":
            
            customer = frappe.get_doc("Customer", self.customer)
            validate = customer.check_vat()
            if not validate:
                frappe.throw(f"Im Kunden ist keine gültige VAT ID hinterlegt")