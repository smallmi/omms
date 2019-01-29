# -*- encoding:utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''
from django import template 

register = template.Library()

@register.filter()  
def usetostr(value):

	data = []
	for v in value:
		data.append("%s(%s)"%(v.username,v.fullname))

	if data:
		data = (',').join(data)
	return data

@register.filter()
def grouptostr(value):

	data = []
	for v in value:
		data.append("%s"%(v.name))

	if data:
		data = (',').join(data)
	return data

@register.filter()  
def gsetostr(value):

	data = []
	for v in value:
		data.append(v.name)

	if data:
		data = (',').join(data)
	return data