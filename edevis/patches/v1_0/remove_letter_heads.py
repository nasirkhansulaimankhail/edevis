import frappe
def execute():
    frappe.db.delete("Letter Head")
