import frappe
def execute():
    frappe.db.delete("Custom Field", "Sales Order-custom_another_test")
    frappe.db.delete("Custom Field", "Quotation-custom_another_test")
    frappe.db.delete("Custom Field", "Sales Order-custom_another_test")