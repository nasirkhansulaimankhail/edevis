frappe.ui.form.on("Customer", {
  refresh(frm) {
    frm.trigger("setup_opportunity_button");
    frm.trigger("setup_connections");
    frm.remove_custom_button("Get Customer Group Details", "Actions");
    frm.remove_custom_button("Pricing Rule", "Create");
    frm.remove_custom_button("Accounting Ledger", "View");
    frm.add_custom_button(__('Validate Tax-ID'), function(){
      frappe.call({
        method: "edevis.custom_scripts.custom_python.checkvat.checkvat",
        args: {
          name: frm.doc.customer_name,
          tax_id: frm.doc.tax_id,
          address: frm.doc.customer_primary_address
        },
        freeze: true,
        freeze_message: __('Retrieving VAT Information from server...'),
        callback: function(r) {
          // frappe.msgprint (r)
        }
      });
    }, __("Actions"));
  },

  setup_opportunity_button(frm) {
    frm
      .add_custom_button(
        __("Opportunity"),
        () => {
          frm.trigger("create_opportunity");
        },
        __("Create")
      )
      .addClass("btn-primary");
  },
  setup_connections(frm) {
    //add connections for opportunity
    $('[class="document-link"][data-doctype="Opportunity"]').remove();
    if ($('.document-link-badge[data-doctype="Opportunity"]').length == 0) {
      frappe.db
        .get_list("Opportunity", {
          filters: {
            custom_lead: cur_frm.doc.lead_name,
          },
          fields: ["name"],
        })
        .then((r) => {
          var opportunities = r.map(function (item) {
            return item["name"];
          });
          opportunities = [...new Set(opportunities)];
          if (!cur_frm.doc.lead_name) {
            opportunities = [];
          }
          if (opportunities.length > 0) {
            $('[class="document-link"][data-doctype="Quotation"]')
              .parent()
              .append(
                `<div class="document-link" data-doctype="Opportunity"><div class="document-link-badge" data-doctype="Opportunity"><span class="count">${opportunities.length}</span><a class="badge-link" id="open-op">Opportunity</a></div></div>`
              );
          } else {
            $('[class="document-link"][data-doctype="Quotation"]')
              .parent()
              .append(
                `<div class="document-link" data-doctype="Opportunity"><div class="document-link-badge" data-doctype="Opportunity"><a class="badge-link" id="open-op">Opportunity</a></div></div>`
              );
          }
          $("#open-op").click((r) => {
            frappe.set_route("List", "Opportunity", {
              name: ["in", opportunities],
            });
          });
          $(".form-documents *> button").hide();
          $(".open-notification").hide();
        });
    }

    //add connections for Lead
    $('[class="document-link"][data-doctype="Lead"]').remove();
    if ($('.document-link-badge[data-doctype="Lead"]').length == 0) {
      frappe.db
        .get_list("Lead", {
          filters: {
            name: frm.doc.lead_name,
          },
          fields: ["name"],
        })
        .then((r) => {
          var leads = r.map(function (item) {
            return item["name"];
          });
          leads = [...new Set(leads)];

          if (!frm.doc.lead_name) {
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
  },
  create_opportunity(frm) {
    frappe.model.open_mapped_doc({
      method: "edevis.custom_scripts.custom_python.customer.create_opportunity",
      frm: frm,
    });
  },
});
