import frappe

def set_serial_no_from_delivery_note(doc, method):
    # Run only when Sales Invoice is being created from Delivery Note
    if doc.is_new():
        for item in doc.items:
            # Skip if serial_no already exists or no delivery_note linked
            if item.serial_no or not item.delivery_note:
                continue

            # Try to find matching Delivery Note Item
            dn_item = frappe.db.get_value(
                "Delivery Note Item",
                {
                    "parent": item.delivery_note,
                    "item_code": item.item_code,
                    "docstatus": 1,
                    "qty": item.qty  # optional, for tighter match
                },
                ["serial_no"],
                as_dict=True
            )

            if dn_item and dn_item.serial_no:
                item.serial_no = dn_item.serial_no
