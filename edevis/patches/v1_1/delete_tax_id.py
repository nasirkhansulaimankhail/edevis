import frappe

def execute():
    frappe.delete_doc_if_exists("Custom Field", "Supplier-custom_vat_id_validation_date")