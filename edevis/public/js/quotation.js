frappe.ui.form.on("Quotation", {
    onload (frm) {
        setTimeout(() => {
            const autoRepeatElement = $("[data-doctype='Auto Repeat']");
            autoRepeatElement.hide();
            autoRepeatElement.siblings(".form-link-title").hide();
        }, 10);
    }
})