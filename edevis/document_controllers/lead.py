from erpnext.crm.doctype.lead.lead import Lead as CRMLead
import frappe


class Lead(CRMLead):
    def set_title(self):
        if not self.title:
            self.title = self.company_name or self.lead_name

