import frappe

class SalesController:
    def validate_vat(self):

        if self.tax_category in ["EU", "Inland"]:
            if not self.tax_id:
                frappe.msgprint("Bitte beachten Sie, dass im Kunden keine VAT ID hinterlegt ist.")


    def check_vat(self):
        if self.tax_category in ["EU", "Inland"]:
            if not self.tax_id:
               frappe.throw("Bitte beachten Sie, dass im Kunden keine gültige VAT ID hinterlegt ist")
        validate = False
        if self.tax_category == "EU":
            
            customer = frappe.get_doc("Customer", self.customer)
            validate = customer.check_vat()
            if validate:
                frappe.db.commit()
                frappe.throw(f"Customer VAT validation failed")