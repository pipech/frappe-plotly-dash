/* eslint require-jsdoc: 0 */

frappe.pages['dash'].on_page_load = (wrapper) => {
	// init page
	const page = frappe.ui.make_app_page({
		'parent': wrapper,
		'title': 'Dashboard',
		'single_column': true,
	});

	new Dash(page, wrapper);
};


class Dash {
	constructor(page, wrapper) {
		this.wrapper = wrapper;
		this.page = page;
		this.siteOrigin = window.location.origin;
		this.pageMain = $(page.main);
		this.pageAction = (
			$(this.wrapper)
				.find('div.page-head div.page-actions')
		);
		this.pageTitle = $(this.wrapper).find('div.title-text');
		this.iframeHtml = `
			<iframe
			id="dash-iframe"
			style="
				border: none;
				width: 100%;
			">
			</iframe>
		`;
		this.init();
	}

	init() {
		// attatch iframe
		this.$dashIframe = $(this.iframeHtml).appendTo(this.pageMain);
		// attatch iframe resizer
		this.resizer();
		// attatch dashboard selector
		this.createSelectionField();
	}

	resizer() {
		window.addEventListener('message', resize, false);
		function resize(event) {
			const dashIframe = document.getElementById('dash-iframe');
			const frameHeight = event.data.frameHeight;
			dashIframe.style.height = `${frameHeight + 30}px`;
		}
	}

	createSelectionField() {
		// create dashboard selection field
		this.selectionField = frappe.ui.form.make_control({
			'parent': this.pageAction,
			'df': {
				'fieldname': 'Dashboard',
				'fieldtype': 'Link',
				'options': 'Dash Dashboard',
				'onchange': () => {
					const dashboardName = this.selectionField.get_value();
					if (dashboardName) {
						this.dashboardName = dashboardName;
						this.changeIframeUrl();
						this.changeTitle(dashboardName);
						// clear input
						this.selectionField.set_input('');
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

		// change css
		this.pageAction.removeClass('page-actions');
		this.selectionField.$wrapper.css('text-align', 'left');
	}

	changeIframeUrl() {
		this.iframeUrl = `${this.siteOrigin}/dash/dashboard?dash=${this.dashboardName}`;
		this.$dashIframe.attr('src', this.iframeUrl);
	}

	changeTitle() {
		this.pageTitle.text(`${this.dashboardName} Dashboard`);
	}
}
