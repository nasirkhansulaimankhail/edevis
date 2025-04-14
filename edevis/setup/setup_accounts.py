import frappe

def create_accounts_after_migrate():
    company = frappe.defaults.get_defaults().get("company")
    if not company:
        frappe.log_error("Account setup skipped: No default company set in site config.", "edevis Setup")
        return

    abbr = frappe.get_value("Company", company, "abbr")
    parent_account_base = "Erlöskonten 8"
    parent_account_name = f"{parent_account_base} - {abbr}"

    # Check if parent account exists
    parent_account = frappe.db.get_value("Account", {
        "account_name": parent_account_base,
        "company": company,
        "is_group": 1
    }, "name")

    if not parent_account:
        frappe.log_error(
            title="edevis Account Setup Failed",
            message=f"Parent account '{parent_account_name}' does not exist for company '{company}'. Child account creation skipped."
        )
        return

    # Define accounts to create
    child_accounts = [
        {
            "account_name": "Erlöse 19% Systems", 
            "account_number": "8400", 
            "parent_account": parent_account_name,
            "account_type": "Tax",
            "is_group": 0,
            "company": company,
            "free_account": "No",
            "root_type": "Income", 
            "report_type": "Profit and Loss"
        },
        {
            "account_name": "Erlöse 19% Services", 
            "account_number": "8401", 
            "parent_account": parent_account_name,
            "account_type": "Tax",
            "is_group": 0,
            "company": company,
            "free_account": "No",
            "root_type": "Income", 
            "report_type": "Profit and Loss"
        },
        {
            "account_name": "Steuerfreie EG- Lieferungen § 4, 1b UstG", 
            "account_number": "8125", 
            "parent_account": parent_account_name,
            "account_type": "Tax",
            "is_group": 0,
            "company": company,
            "free_account": "No",
            "root_type": "Income", 
            "report_type": "Profit and Loss"
        },
        {
            "account_name": "Erlöse sonst. Leistungen im and. EG-Land stpfl., 13b UstG", 
            "account_number": "8336", 
            "parent_account": parent_account_name,
            "account_type": "Tax",
            "is_group": 0,
            "company": company,
            "free_account": "No",
            "root_type": "Income", 
            "report_type": "Profit and Loss"
        },
        {
            "account_name": "Steuerfreie Umsätze § 4 Nr.1a UStG", 
            "account_number": "8120", 
            "parent_account": parent_account_name,
            "account_type": "Tax",
            "is_group": 0,
            "company": company,
            "free_account": "No",
            "root_type": "Income", 
            "report_type": "Profit and Loss"
        },
        {
            "account_name": "Nicht steuerbare Umsätze Drittland", 
            "account_number": "8338", 
            "parent_account": parent_account_name,
            "account_type": "Tax",
            "is_group": 0,
            "company": company,
            "free_account": "No",
            "root_type": "Income", 
            "report_type": "Profit and Loss"
        },
    ]

    for acc in child_accounts:
        if frappe.db.exists("Account", {
            "account_number": acc["account_number"],
            "company": company
        }):
            continue

        frappe.get_doc({
            "doctype": "Account",
            "account_name": acc["account_name"],
            "account_number": acc["account_number"],
            "parent_account": parent_account,
            "account_type": acc["account_type"],
            "is_group": acc["is_group"],
            "company": company,
            "free_account": acc["free_account"],
            "root_type": acc["root_type"],
            "report_type": acc["report_type"]
        }).insert()

    frappe.db.commit()
