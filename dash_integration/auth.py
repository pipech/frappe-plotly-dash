import frappe


def has_desk_permission():
    user = frappe.session.user
    user_type = frappe.db.get_value('User', user, 'user_type')

    desk_permission = not (
        (user == 'Guest') or
        (user_type == 'Website User')
    )

    return desk_permission


def has_dashboard_permission(dashboard):
    user = frappe.session.user

    # get allow role for dashboard
    allowed_roles_dict = frappe.get_all(
        'Has Role',
        fields=['role'],
        filters={
            'parenttype': 'Dash Dashboard',
            'parent': dashboard,
        }
    )

    # convert list of role dict to role list
    allow_roles = []
    for roles_dict in allowed_roles_dict:
        role = roles_dict.get('role')
        if role:
            allow_roles.append(role)

    # get user roles
    user_roles = frappe.permissions.get_roles(user)

    return frappe.utils.has_common(allow_roles, user_roles)
