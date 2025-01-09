import frappe

def execute():
    fields = ["Customer-custom_tax_id_validation_result", "Customer-custom_vat_id_validation_date", "Pruefproblem-custom_inquiry_description_details"]
    for cf in fields:
        frappe.db.delete("Custom Field", cf)
        print(f"Deleting {cf}")