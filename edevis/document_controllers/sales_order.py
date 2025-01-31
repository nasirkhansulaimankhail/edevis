from erpnext.selling.doctype.sales_order.sales_order import SalesOrder as ERPNextSalesOrder
from edevis.document_controllers.sales_controller import SalesController

class SalesOrder(ERPNextSalesOrder, SalesController):
    def before_save(self):
        self.validate_vat()

    def before_submit(self):
        self.check_vat()