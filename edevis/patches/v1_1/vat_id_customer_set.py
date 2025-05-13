import frappe

def execute():
    records = frappe.get_all("VAT ID Validation", filters={"customer": ["!=", ""], "party": ["in", [None, ""]]}, fields=["name", "customer"])

    for record in records:
        frappe.db.set_value("VAT ID Validation", record.name, {
            "party": record.customer,
            "party_type": "Customer"
        })
