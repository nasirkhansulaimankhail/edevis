# Copyright (c) 2024, phamos.eu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EdevisSettings(Document):

	def validate(self):
		if self.debitors_parent_account:
			
			#get values for is_group and root_type
			is_group, root_type = frappe.db.get_value("Account", self.debitors_parent_account, ['is_group', 'root_type'])
			
			#validates if account is a group account and root type is Asset.
			if not is_group or root_type != "Asset":
				frappe.throw("Account must be a group account and root type must be Asset.") 