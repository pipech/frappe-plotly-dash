import frappe


def check_permitted(dashboard_name, username):
    """Returns true if Has Role is not set or the user is allowed."""
    allowed = False

    # get allow role for dashboard
    allowed_roles_dict = frappe.get_all(
        'Has Role',
        fields=['role'],
        filters={
            'parenttype': 'Dash Dashboard',
            'parent': dashboard_name,
        }
    )

    # convert list of role dict to role list
    allow_roles = []
    for roles_dict in allowed_roles_dict:
        role = roles_dict.get('role')
        if role:
            allow_roles.append(role)

    # get user roles
    user_roles = frappe.permissions.get_roles(username)

    # check
    if frappe.utils.has_common(allow_roles, user_roles):
        allowed = True

    return allowed
