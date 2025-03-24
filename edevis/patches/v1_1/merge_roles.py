import frappe
from frappe.model.rename_doc import update_document_title
def execute():
    roles = ["edevis Pruefproblem", "edevis Vertrieb", "edevis CRM User"]
    for r in roles:
        if frappe.db.exists("Role", r):
            update_document_title(doctype="Role", docname=r, name="Sales User", merge=True)
            print(f"Merging {r}.")