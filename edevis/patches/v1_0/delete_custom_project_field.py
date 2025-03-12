import frappe

def execute():
    frappe.db.delete("Custom Field", "Quotation-custom_project")