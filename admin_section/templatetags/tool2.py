from django import template
import base64
import requests as req
from admin_section.models import *
register = template.Library()

@register.simple_tag
def render_dec(number=None):
	print(number)
	pr = '{:.20f}'.format(float(number))
	if 'e' in str(float(number)):
		st_num = str(number)[1:]
		#print(st_num)
		indice = st_num.find('-')
		#print(indice)
		length1 = int(st_num[indice+1:])
		#print(length1)
		indice  = pr.find('.')
		final_num = pr[:length1+indice+1]
		return final_num
	else:
		return str(number)

@register.simple_tag
def render_int(number=None):
	return str(int(number))

@register.simple_tag
def get_percentage(val=None):
	index = str(val).find('.')
	if index == -1:
		index = 0
	num = str(val)[index+1:]
	print(num)
	if  int(num) != 0:
		return val
	else:
		return int(val)


@register.simple_tag
def get_qrcode(data=None):
	if data:
		resp = req.get('http://chart.apis.google.com/chart?cht=qr&chs=230x230&chl={0}'.format(data))
		encoded = base64.b64encode(resp.content)
		return 'data:image/png;base64,'+ encoded.decode()

	else:
		return ''

@register.simple_tag
def get_element(index=0,lst=[]):
	if index-1 <= 0:
		index = 0
	else:
		index -= 1
	print(lst)
	print(index)
	try:
		return lst[index]
	except:
		return ''


@register.simple_tag
def increment(val=None):
	val = int(val)
	val += 1
	return val



@register.simple_tag
def decrement(val=None):
	val = int(val)
	val -= 1

	return val



@register.simple_tag
def get_meta(index=0):

	meta = PageMeta.objects.filter(page=index)
	if len(meta) == 0:
		meta = PageMeta.objects.create(page=index)
		meta.save()
	else:
		meta = meta[0]



	return meta
