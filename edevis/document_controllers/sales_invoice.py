from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice as ERPNextSalesInvoice
from edevis.document_controllers.sales_controller import SalesController

class SalesInvoice(ERPNextSalesInvoice, SalesController):
    def before_save(self):
        super().before_save()
        self.validate_vat()

    def before_submit(self):
        super().before_submit()
        self.check_vat()