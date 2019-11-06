## Dash Integration

Plotly Dash integration for Frappe web framework

### Usage

You have to edit frappe apps in `frappe/frappe/app.py`

import function at the top of the file

`from dash_integration.app import build_ajax, build_page`

in application function `def application(request):` add these line

    if frappe.local.form_dict.cmd:
        response = frappe.handler.handle()

    elif frappe.request.path.startswith("/dash/_dash"):
        response = build_ajax(request)

    elif frappe.request.path.startswith("/dash/"):
        response = build_page(request)

    elif frappe.request.path.startswith("/api/"):
        response = frappe.api.handle()

### Description

[CoreUi bootstrap admin template](https://github.com/coreui/coreui-free-bootstrap-admin-template/) is use to templating dash page. 

#### License

This repository has been released under the MIT License.
