frappe.ui.form.on("Sales Order", {
    tc_name: function (frm) {
        if (!frm.doc.tc_name) {
            frm.set_value("terms", "");
        }
    },
});