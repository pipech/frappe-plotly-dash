import frappe


def has_desk_permission():
    user = frappe.session.user
    user_type = frappe.db.get_value('User', user, 'user_type')

    desk_permission = not (
        (user == 'Guest') or
        (user_type == 'Website User')
    )

    return desk_permission
