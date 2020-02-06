# -*- coding: utf-8 -*-
# Copyright (c) 2019, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class IPDItemMapping(Document):
	pass
def ipd_item_mapping(ipd_list,ipd_name,item):
	ipd_item=[]
	for ipd in ipd_list:
		for variant in ipd['variants']:
			description = get_description(ipd['process'],ipd['process_record'])
			if ipd['process']=='Knitting':
				ipd_item.append({'item': variant,'process_1':ipd['process'],'input_item': ipd['input_item'][0],'ipd_process_index': ipd['index'],'input_index': ipd['input_index'],'description': description})
			else:
				ipd_item.append({'item': variant,'process_1':ipd['process'],'ipd_process_index': ipd['index'],'input_index': ipd['input_index'],'description': description})
	ipd_item_=frappe.db.get_value("IPD Item Mapping",{'item_production_details': ipd_name},'name')
	if not ipd_item_:
		frappe.get_doc({
			'doctype': 'IPD Item Mapping',
			'item_production_details': ipd_name,
			'item': item,
			'item_mapping':ipd_item}).save()

def get_description(process , process_record):
	description = ''
	if not process_record=='':
		doc = frappe.get_doc(process,process_record)
		if doc.additional_information:
			for add_info in doc.additional_information:
				description += f'{add_info.parameter} : {add_info.value}\n'
			return description
		else:
			return 'none'
