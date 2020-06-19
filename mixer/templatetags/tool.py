from django import template
import os
from an_back.settings import  *
from mixer.env import *
from admin_section.models import *
from mixer.models import *
import requests as req
import datetime
import base64
try:
	from pretty_bad_protocol import gnupg
except:
	import gnupg


register = template.Library()



@register.simple_tag
def define(val=None):
	return val

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
def render_adds_next(ads):
	new_list = []
	counter = 1
	for x in ads:
		new_list.append('address{0}={1}'.format(str(counter),x))
		counter += 1

	return '&'.join(new_list)

@register.simple_tag
def render_adds_prev(ads):
	ads = ads[:-1]
	new_list = []
	counter = 1
	for x in ads:
		new_list.append('address{0}={1}'.format(str(counter),x))
		counter += 1

	return '&'.join(new_list)

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
def get_txs(txids=None):
	if txids:
		return txids.split(',')
	else:
		return []

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
def get_txs(txs=None):
	if txs:
		return txs.split(',')
	else:
		return []

def render_dec_int(number=None):
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
def get_year():
	now = datetime.datetime.now()
	return str(now.year)

@register.simple_tag
def get_elems(mirrors=None):
	print(mirrors)
	mirrs = mirrors.split(',')
	return mirrs

@register.simple_tag
def get_count(elems):
	return len(elems)

@register.simple_tag
def get_pgp(mix_id=None):
	if mix_id:
		gpg = gnupg.GPG(homedir=os.path.join(BASE_DIR, '.gnupg2'))
		imported_k = gpg.import_keys(pgp_public)
		imported_p = gpg.import_keys(pgp_private)
		print(gpg.list_keys())
		print(gpg.list_keys(True))
		sett = Settings.objects.all()[0]
		mix = Mix.objects.filter(mix_id = mix_id)[0]
		adds = mix.addresses_set.all()
		adds_dets = [','.join(['Amount : '+str(render_dec_int(number=float(x.amount_sent))),'Delay : ' + str(x.delay),'Transaction ID : ' + str(x.txid)]) for x in adds]
		adds_msg = '\n'.join(adds_dets)
		print(adds_msg)
		date = mix.date.strftime('%Y-%m-%d %H:%M:%S')
		message = """
		This certificate was issued by Anonymix.io, a Bitcoin mixing service.
It can be utilized to proof that the Bitcoins received through the following transaction(s) were sent by Anonymix.

Transaction(s) details:
 {0}
 Session is valid for {1} days From {2}

 Service Fee  : {3}
 Transaction_fee : {4}


 PGP fingerprint: {5}""".format(adds_msg,sett.d_inactive,date,render_dec_int(number=sett.s_fee),render_dec_int(number=sett.t_fee),fingerprint)
		print(message)
		signed = gpg.sign(message,passphrase=passphrase,default_key=imported_k.fingerprints[0])
		return str(signed)

	else:
		return ''
