import frappe
def execute():
    frappe.db.delete("Custom Field", "Quotation-custom_delivery_time")
    frappe.db.delete("Custom Field", "Quotation-delivery_time")