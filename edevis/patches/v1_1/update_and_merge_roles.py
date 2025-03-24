import frappe
from frappe.model.rename_doc import update_document_title
def execute():
    roles = [["00201 ADM", "0 ADM"], ["00201 APP", "0 APP"]]
    for r in roles:
        if frappe.db.exists("Role", r[0]) and frappe.db.exists("Role", r[1]):
            update_document_title(doctype="Role", docname=r[0], name=r[1], merge=True)
            print(f"renaming {r[0]} to {r[1]}.")
