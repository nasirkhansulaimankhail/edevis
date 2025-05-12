frappe.ui.form.on("Supplier", {
  refresh(frm) {
    frm.add_custom_button(__('Validate Tax-ID'), function(){
      frappe.call({
        method: "edevis.custom_scripts.custom_python.checkvat.checkvat",
        args: {
          name: frm.doc.name,
          tax_id: frm.doc.tax_id,
          address: frm.doc.supplier_primary_address,
          party_type: 'Supplier'

        },
        freeze: true,
        freeze_message: __('Retrieving VAT Information from server...'),
        callback: function(r) {
          frm.refresh_field("tax_id_validation_result");
        }
      });
    }, __("Actions"));
  },
});
