frappe.pages['dash'].on_page_load = (wrapper) => {
	// init page
	const page = frappe.ui.make_app_page({
		'parent': wrapper,
		'title': 'Dashboard',
		'single_column': true,
	});

	// attatch dash iframe
	const iframeHtml = `
		<iframe
		id="dash-iframe"
		src="http://site1.local:8000/dash/page-1"
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

	window.addEventListener('message', resizeIframe, false);
};
