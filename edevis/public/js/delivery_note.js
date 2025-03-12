frappe.ui.form.on("Delivery Note", {
    onload(frm){
        frm.remove_custom_button("Installation Note", "Create");
        frm.remove_custom_button("Delivery Trip", "Create");
    },
    refresh(frm) {
        if(frm.doc.docstatus == 1) {
            setTimeout(() => {
                frm.remove_custom_button("Installation Note", "Create");
                frm.remove_custom_button("Delivery Trip", "Create");
            }, 10);
           
            frm.add_custom_button(__("Proforma Invoice"), function() {
                frappe.call({
                    method: "frappe.client.insert",
                args: {
                    doc: {
                        doctype: "Proforma Invoice",
                        delivery_note: frm.doc.name
                    }
                },
                callback: function(response) {
                        if (!response.exc) {
                            
                            frappe.set_route("proforma-invoice", response.message.name);
                        } else {
                            frappe.msgprint("Error creating Proforma Invoice");
                        }
                    }
                });
            }, __("Create"));
        }
    }
})