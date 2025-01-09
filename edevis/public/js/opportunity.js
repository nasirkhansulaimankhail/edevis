frappe.ui.form.on("Opportunity", {
  refresh: function (frm) {
    frm.trigger("setup_connections");
  },
  validate: function (frm) {
    if (frm.doc.opportunity_from !== "Customer") {
      frappe.throw(
        "Please select 'Customer' as the Opportunity Form. Opportunities can only be created from a customer."
      );
    }
  },
  setup_connections(frm) {
    //add connections for Lead
    $('[class="document-link"][data-doctype="Supplier Quotation"]').remove();
    $('[class="document-link"][data-doctype="Request for Quotation"]').remove();
    $('[class="document-link"][data-doctype="Lead"]').remove();
    if ($('.document-link-badge[data-doctype="Lead"]').length == 0) {
      frappe.db
        .get_list("Lead", {
          filters: {
            name: cur_frm.doc.custom_lead,
          },
          fields: ["name"],
        })
        .then((r) => {
          var leads = r.map(function (item) {
            return item["name"];
          });
          leads = [...new Set(leads)];

          if (!cur_frm.doc.custom_lead) {
            leads = [];
          }
          if (leads.length > 0) {
            $('[class="document-link"][data-doctype="Quotation"]')
              .parent()
              .append(
                `<div class="document-link" data-doctype="Lead"><div class="document-link-badge" data-doctype="Lead"><span class="count">${leads.length}</span><a class="badge-link" id="open-le">Lead</a></div></div>`
              );
          } else {
            $('[class="document-link"][data-doctype="Quotation"]')
              .parent()
              .append(
                `<div class="document-link" data-doctype="Lead"><div class="document-link-badge" data-doctype="Lead"><a class="badge-link" id="open-le">Lead</a></div></div>`
              );
          }
          $("#open-le").click((r) => {
            frappe.set_route("List", "Lead", {
              name: ["in", leads],
            });
          });
          $(".form-documents *> button").hide();
          $(".open-notification").hide();
        });
    }
    //add connections for Customer
    $('[class="document-link"][data-doctype="Customer"]').remove();
    if ($('.document-link-badge[data-doctype="Customer"]').length == 0) {
      frappe.db
        .get_list("Customer", {
          filters: {
            name: frm.doc.party_name,
          },
          fields: ["name"],
        })
        .then((r) => {
          var customers = r.map(function (item) {
            return item["name"];
          });
          customers = [...new Set(customers)];

          if (!cur_frm.doc.name) {
            customers = [];
          }
          if (customers.length > 0) {
            $('[class="document-link"][data-doctype="Quotation"]')
              .parent()
              .append(
                `<div class="document-link" data-doctype="Customer"><div class="document-link-badge" data-doctype="Customer"><span class="count">${customers.length}</span><a class="badge-link" id="open-cu">Customer</a></div></div>`
              );
          } else {
            $('[class="document-link"][data-doctype="Quotation"]')
              .parent()
              .append(
                `<div class="document-link" data-doctype="Customer"><div class="document-link-badge" data-doctype="Customer"><a class="badge-link" id="open-cu">Customer</a></div></div>`
              );
          }
          $("#open-cu").click((r) => {
            frappe.set_route("List", "Customer", {
              name: ["in", customers],
            });
          });
          $(".form-documents *> button").hide();
          $(".open-notification").hide();
        });
    }
  },
});



frappe.ui.form.on("Opportunity Item", {
	calculate: function (frm, cdt, cdn) {
		let row = frappe.get_doc(cdt, cdn);
		frappe.model.set_value(cdt, cdn, "amount", flt(row.qty) * flt(row.rate));
		frappe.model.set_value(cdt, cdn, "base_rate", flt(frm.doc.conversion_rate) * flt(row.rate));
		frappe.model.set_value(cdt, cdn, "base_amount", flt(frm.doc.conversion_rate) * flt(row.amount));
		frm.trigger("calculate_total");
	},
	qty: function (frm, cdt, cdn) {
		frm.trigger("calculate", cdt, cdn);
	},
	rate: function (frm, cdt, cdn) {
		frm.trigger("calculate", cdt, cdn);
	},
  item_code: function(frm, cdt, cdn){
    var item = frappe.get_doc(cdt, cdn);
    var price_list = frm.doc.custom_price_list; // Get the selected price list from the Opportunity DocType
    var item_code = item.item_code;
    if(!frm.doc.custom_price_list){
      frappe.msgprint("Please setup price list first")
      return
    }
    frappe.call({
        method: 'frappe.client.get_value',
        args: {
            doctype: 'Item Price',
            filters: {
                item_code: item_code,
                price_list: price_list
            },
            fieldname: 'price_list_rate'
        },
        callback: function(response) {
            if (response && response.message) {
                frappe.model.set_value(cdt, cdn, 'rate', response.message.price_list_rate);
            }
        }
    });
  }
});