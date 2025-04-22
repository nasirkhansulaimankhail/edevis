def execute():
    from frappe.model.delete_doc import delete_doc
    import frappe
    frappe.log_error("working_patch")
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
