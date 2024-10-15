// Copyright (c) 2024, phamos.eu and contributors
// For license information, please see license.txt

frappe.ui.form.on("Edevis Settings", {
 	refresh(frm) {
        frm.set_query("debitors_parent_account", function(){
            return {
                filters:{
                    "is_group": 1,
                    "root_type": "Asset"
                }
            }
        })
    },
});
