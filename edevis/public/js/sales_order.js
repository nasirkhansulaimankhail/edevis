frappe.ui.form.on("Sales Order", {
    tc_name: function (frm) {
        if (!frm.doc.tc_name) {
            frm.set_value("terms", "");
        }
    },
    onload(frm){
        if(frm.is_new()){
            let term = frm.doc.payment_terms_template;
            frm.set_value("payment_terms_template", "")
            frm.set_value("payment_terms_template", term)   
        }
        
    }
});