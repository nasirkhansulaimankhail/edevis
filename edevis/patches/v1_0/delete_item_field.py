import frappe

def execute():
   
    frappe.db.delete("Custom Field", "Item-custom_warranty_text")
    print("Item-custom_warranty_text")