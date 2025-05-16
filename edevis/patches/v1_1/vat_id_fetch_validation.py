import frappe

def execute():
    vat_records = frappe.get_all("VAT ID Validation", fields=["name", "party_type", "party", "validation_date","creation"])

    for record in vat_records:
        try:
            party_doc = frappe.get_doc(record.party_type, record.party)

            company_name = ""
            if record.party_type == "Customer":
                company_name = party_doc.customer_name
            elif record.party_type == "Supplier":
                company_name = party_doc.supplier_name
            frappe.db.set_value("VAT ID Validation", record.name, {
                "company_name": company_name,
                "validation_date": record.creation
            })

        except Exception as e:
            frappe.log_error(frappe.get_traceback(), f"VAT Patch (Only Company Name) Error: {record.name}")
