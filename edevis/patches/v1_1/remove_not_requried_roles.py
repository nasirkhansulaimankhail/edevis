import frappe
from edevis.patches.v1_1.update_and_merge_roles import execute as merge_roles


def execute():
	merge_roles()
	for d in ["00201 ADM", "00201 APP"]:
		if frappe.db.exists("Role", d):
			frappe.delete_doc("Role", d)
			print(f"Deleting {d}")

