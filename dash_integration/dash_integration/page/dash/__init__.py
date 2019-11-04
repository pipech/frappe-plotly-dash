import frappe


@frappe.whitelist()
def get_dashboard_path(dashboard_name):
    return frappe.get_value(
        'Dash Dashboard',
        dashboard_name,
        'url',
    )
