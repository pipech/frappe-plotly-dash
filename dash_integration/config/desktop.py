# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		# {
		# 	'module_name': 'Dash Integration',
		# 	'color': 'grey',
		# 	'icon': 'octicon octicon-graph',
		# 	'type': 'module',
		# 	'label': _('Dash Integration')
		# },
		{
			'module_name': 'dash',
			'category': 'Places',
			'label': _('Dash'),
			'icon': 'octicon octicon-graph',
			'type': 'link',
			'link': '#dash',
			'color': '#FF4136',
			'standard': 1,
			'idx': 11
		},
	]
