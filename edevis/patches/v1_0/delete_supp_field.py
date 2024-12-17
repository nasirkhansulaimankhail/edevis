import frappe

def execute():
    frappe.db.delete("Customer-custom_supp_no_ref_cust_no")
    frappe.db.delete("Customer-supp_no_ref_cust_no")