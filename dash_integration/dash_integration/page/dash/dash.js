frappe.pages['dash'].on_page_load = (wrapper) => {
	const cookie = frappe.get_cookies();
	const sid = cookie.sid;
	const siteName = frappe.boot.sitename;

	// init page
	const page = frappe.ui.make_app_page({
		'parent': wrapper,
		'title': 'Dashboard',
		'single_column': true,
	});

	attachIframe(page, sid, siteName);
	createSelectionField(wrapper);
};


/** Attach iframe to page
 * @param {object} page
 * @param {string} sid
 * @param {string} siteName
*/
function attachIframe(page, sid, siteName) {
	// attach iframe
	const iframeHtml = `
		<iframe
		id="dash-iframe"
		src="http://site1.local:8000/dash/page-1?sid=${sid}&site_name=${siteName}"
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
					console.log(dashboardName);
				}
			},
			'get_query': () => {
				return {
					'filters': {
						'is_active': 1,
					},
				};
			},
		},
		'render_input': true,
	});
	selDashboard.$wrapper.css('text-align', 'left');
}
