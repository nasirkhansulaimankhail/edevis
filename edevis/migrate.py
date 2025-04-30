import frappe
from frappe.model.delete_doc import delete_doc

def remove_custom_print_formats():
    # List of print formats to delete from DB so they load from code
    print_formats_to_remove = [
        "Sales Invoice - ED",
        "Proforma Invoice",
        "Quotation - ED",
        "Purchase Order - ED",
        "Sales Order - ED",
        "Delivery Note - ED",
        "Down Payment Request"
    ]

    for pf in print_formats_to_remove:
        if frappe.db.exists("Print Format", pf):
            delete_doc("Print Format", pf, force=True)