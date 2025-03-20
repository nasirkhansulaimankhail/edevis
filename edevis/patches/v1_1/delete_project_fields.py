import frappe

def execute():
    frappe.db.delete("Custom Field", {"dt": "Project"})