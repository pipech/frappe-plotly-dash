## Dash Integration

Plotly Dash integration for Frappe web framework

### Usage

You have to edit frappe apps in `frappe/frappe/website/render.py`

add these line on top of render function

```python
from dash_integration.app import dash_render

@dash_render
def render(path=None, http_status_code=None):
```

### Description

[CoreUi bootstrap admin template](https://github.com/coreui/coreui-free-bootstrap-admin-template/) is use to templating dash page. 

#### License

This repository has been released under the MIT License.
