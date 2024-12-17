import frappe

def execute():
   
    frappe.db.delete("Custom Field", "Customer-custom_supp_no_ref_cust_no")
    frappe.db.delete("Custom Field", "Customer-supp_no_ref_cust_no")