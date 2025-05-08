import frappe

def create_sales_taxes_templates():
    company = frappe.defaults.get_defaults().get("company")
    if not company:
        frappe.log_error("No default company found.", "edevis Tax Template Setup")
        return

    # Fixed template definitions
    templates = [
        {"account_number": "8400", "name": "Inland, Lieferungen: USt 19 %", "des1": "Versandkosten", "des2": "Umsatzsteuer 19%", "rate": 19},
        {"account_number": "8401", "name": "Inland, Dienstleistungen: USt 19 %", "des1": "Versandkosten", "des2": "Umsatzsteuer 19%", "rate": 19},
        {"account_number": "8120", "name": "Drittland, Export-Lieferung: 0%", "des1": "Versandkosten", "des2": "Umsatzsteuer 0%", "rate": 0},
        {"account_number": "8338", "name": "Drittland, Dienstleistungen / Software: USt. 0%", "des1": "Versandkosten", "des2": "Umsatzsteuer 0%", "rate": 0},
        {"account_number": "8125", "name": "EU, Innergemeinschaftliche Lieferungen: USt 0 %", "des1": "Versandkosten", "des2": "Umsatzsteuer 0%", "rate": 0},
        {"account_number": "8336", "name": "EU, Sonstige Leistung §13B: USt. 0%", "des1": "Versandkosten", "des2": "Umsatzsteuer 0%", "rate": 0}
    ]

    for template in templates:
        template_name = f"{template['name']}"

        if frappe.db.exists("Sales Taxes and Charges Template", {"title": template_name, "company": company}):
            continue  # Skip if already exists

        # Get the account with the matching account number and company
        account_head = frappe.db.get_value("Account", {
            "account_number": template["account_number"],
            "company": company
        }, "name")

        if not account_head:
            frappe.log_error(
                title="edevis Tax Template Skipped",
                message=f"Account number {template['account_number']} not found in company '{company}'. Template '{template_name}' skipped."
            )
            continue

        doc = frappe.new_doc("Sales Taxes and Charges Template")
        doc.title = template_name
        doc.company = company
        doc.is_default = 0

        # Add fixed child table entries
        doc.append("taxes", {
            "charge_type": "Actual",
            "description": template['des2'],
            "account_head": account_head,
            "rate": 0.0
        })

        doc.append("taxes", {
            "charge_type": "On Previous Row Total",
            "description": template['des2'],
            "account_head": account_head,
            "row_id": 1,
            "rate": template['rate']
        })

        doc.insert()
        frappe.db.commit()

        frappe.log_error(f"Created Sales Taxes Template: {template_name}")
