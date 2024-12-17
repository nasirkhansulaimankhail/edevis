import frappe
def execute():
    frappe.db.delete("Letterhead")