import frappe
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice

class CustomSalesInvoice(SalesInvoice):
    def set_missing_values(self, for_validate=False):
        # Populate company on child rows before v16's ctx merge reads it
        if self.company:
            for item in self.items:
                if not item.get("company"):
                    item.company = self.company
        super().set_missing_values(for_validate)