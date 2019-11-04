const dash = {};

frappe.pages['dash'].on_page_load = (wrapper) => {
	const cookie = frappe.get_cookies();
	dash.sid = cookie.sid;
	dash.siteName = frappe.boot.sitename;
	dash.wrapper = wrapper;

	// init page
	const page = frappe.ui.make_app_page({
		'parent': wrapper,
		'title': 'Dashboard',
		'single_column': true,
	});

	attachIframe(page);
	createSelectionField(wrapper);
};


/** Attach iframe to page
 * @param {object} page
*/
function attachIframe(page) {
	// attach iframe
	const iframeHtml = `
		<iframe
		id="dash-iframe"
		style="
			border: none;
			width: 100%;
		">
		</iframe>
	`;
	$(page.main).append(iframeHtml);

	/** Resize iframe function.
	 * @param {object} event - A string param
	 */
	function resizeIframe(event) {
		const dashIframe = document.getElementById('dash-iframe');
		const frameHeight = event.data.frameHeight;
		dashIframe.style.height = `${frameHeight + 30}px`;
	}
	// attach resizer
	window.addEventListener('message', resizeIframe, false);
}


/** Create customer dashboard selection field
 * @param {object} wrapper
 */
function createSelectionField(wrapper) {
	const $pageAction = (
		$(wrapper)
			.find('div.page-head div.page-actions')
	);
	// remove change page-actions class
	$pageAction.removeClass('page-actions');

	// create dashboard selection field
	const selDashboard = frappe.ui.form.make_control({
		'parent': $pageAction,
		'df': {
			'fieldname': 'Dashboard',
			'fieldtype': 'Link',
			'options': 'Dash Dashboard',
			'onchange': () => {
				const dashboardName = selDashboard.get_value();
				if (dashboardName) {
					changeIframeUrl(dashboardName);
					changeTitle(dashboardName);
					// clear input
					selDashboard.set_input('');
				}
			},
			'get_query': () => {
				return {
					'filters': {
						'is_active': 1,
					},
				};
			},
			'placeholder': 'Select Dashboard',
		},
		'render_input': true,
	});
	selDashboard.$wrapper.css('text-align', 'left');
}


/** Change Iframe url
 * @param {str} dashboardName
*/
function changeIframeUrl(dashboardName) {
	const siteOrigin = window.location.origin;

	frappe.call({
		'method': 'dash_integration.dash_integration.page.dash.get_dashboard_path',
		'args': {
			'dashboard_name': dashboardName,
		},
		'callback': function(r) {
			const path = r.message;
			if (r) {
				const iframeUrl = `${siteOrigin}/dash/${path}?sid=${dash.sid}&site_name=${dash.siteName}`;
				$('#dash-iframe').attr('src', iframeUrl);
			}
		},
	});
}


/** Change page title
 * @param {str} title
*/
function changeTitle(title) {
	const pageTitle = $(dash.wrapper).find('div.title-text');
	pageTitle.text(`${title} Dashboard`);
}
