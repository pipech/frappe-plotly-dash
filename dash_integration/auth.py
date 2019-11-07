import frappe


def has_desk_permission():
    desk_permission = not (
        frappe.session.user == 'Guest' or
        frappe.db.get_value('User', frappe.session.user, 'user_type') == 'Website User'
    )

    return desk_permission
