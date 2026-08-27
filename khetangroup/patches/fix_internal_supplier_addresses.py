import frappe


def execute():
    company = "Khetan Udyog"

    addresses = [
        "Mundra Solar Pv Limited-Billing-8",
        "Mundra Solar Pv Limited (Assam)-Khetan Udyog-Billing-5",
        "Mundra Solar Pv Limited  (BIHAR)-Khetan Udyog-Billing-1",
    ]

    for addr_name in addresses:
        if not frappe.db.exists("Address", addr_name):
            frappe.log_error(
                title="fix_internal_supplier_addresses",
                message=f"Address not found: {addr_name}",
            )
            continue

        addr = frappe.get_doc("Address", addr_name)

        already_linked = any(
            l.link_doctype == "Company" and l.link_name == company
            for l in addr.links
        )
        if not already_linked:
            addr.append("links", {
                "link_doctype": "Company",
                "link_name": company,
            })

        if addr.is_your_company_address != 1:
            addr.is_your_company_address = 1

        addr.save(ignore_permissions=True)

    frappe.db.commit()