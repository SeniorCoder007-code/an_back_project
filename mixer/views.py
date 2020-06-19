from django.shortcuts import render,HttpResponse,redirect
import uuid
from .models import *
from admin_section.models import *
import threading
from .worker import *
from .nod_handler import *
from an_back.settings import  *
from .env import *
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.views.decorators.csrf import csrf_exempt
from pysendpulse.pysendpulse import PySendPulse
import base64
import string
import random
from captcha.views import *
from captcha.models import *

# Create your views here.
def check_valid(address,h):

	res = h.send('validateaddress',address)['isvalid']
	return res

def check_valid_call(request):
	if request.method == 'post':
		passcall = request.POST.get('passcall',False)
	else:
		passcall = request.GET.get('passcall',False)
	if passcall == callpass:
		return True
	else:
		return False


def index(request):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	res = check_protection(request)
	if res:
		pass
	else:
		return redirect('/viewprotection')
	sett = Settings.objects.all()[0]
	meta = PageMeta.objects.filter(page=0)
	if len(meta) == 0:
		meta = PageMeta.objects.create(page=1)
		meta.save()
	else:
		meta = meta[0]
	return render(request,'index.html',{'s':sett,'title':'home','meta':meta})

def new_mix(request):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	if request.method == 'POST':
		addresses = request.POST.get('addresses','')
		if addresses != '':
			h = get_handler('BTC')
			splited = addresses.split(',')
			adds = []
			for add in splited:
				if check_valid(add,h):
					adds.append(add)
				else:
					return render(request,'new_mix.html',{'message':'wrong bitcoin address'})

			if len(adds) ==  0:
				return render(request,'new_mix.html',{'message':'please type an address'})
			else:
				return render(request,'new_mix_2.html',{'adds':adds,'length':len(adds)})



		else:
			pass
	else:
		return render(request,'new_mix.html')

def start():
	w = worker()
	w.main()


def view_protection(request):
	#input(request.COOKIES)
	print(request.session.session_key)
	return render(request,'protection.html')



def verify_protection(request):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	if request.method == 'POST':
		print(request.session.session_key)

		password = request.POST.get('password','')

		if  password == '':
			return render(request,'login.html',{'message':'empty field'})

		usr = ViewProtection.objects.filter(password =  password )
		if len(usr) != 0:
			usr = usr[0]
			if password == usr.password:
				request.session.set_expiry(0)
				request.session['protection'] = usr.password
				return  redirect('/')
			else:
				return render(request,'protection.html',{'message':'password is incorrect'})

		else:
			return render(request,'protection.html',{'message':'user not found'})

	else:
		return render(request,'protection.html',{'message':'not valid'})


def check_protection(request):
	sett = Settings.objects.all()[0]
	if sett.protection:
		pass
	else:
		return True
	password = request.session.get('protection','')
	if password != '':
		return True
	else:
		return False
@csrf_exempt
def status_prot(request):
	print('here')
	sett = Settings.objects.all()[0]
	if sett.protection:
		return HttpResponse(json.dumps({'status':True}))
	else:
		return HttpResponse(json.dumps({'status':False}))


def new_mix_2(request,message=False,count='',adds=[]):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	res = check_protection(request)
	sett =  Settings.objects.all()[0]
	keyy = CaptchaStore.pick()
	print(keyy)
	url = '/gencaptcha'
	meta = PageMeta.objects.filter(page=1)
	if len(meta) == 0:
		meta = PageMeta.objects.create(page=1)
		meta.save()
	else:
		meta = meta[0]
	if res:
		pass
	else:
		return redirect('/viewprotection')
	if request.method == 'POST':


		#count = request.GET.get('count','')
		ad_dict = {}
		counter = 1
		for x in adds:
			ad_dict[counter] = x
			counter += 1


		if count != '':
			try:
				count = int(count)

				if count > 5:
					count = 5
				elif count < 1:
					count  = 1

			except Exception as e:
				count = 1
			lst = list(range(1,count+1))
			ad_dict.update({'count':count,'title':'Begin Mix','lst':lst,'message':message,'adds':adds,'s':sett,'link':url,'token':keyy,'meta':meta})
			print(ad_dict)
			return render(request,'new_mix_3.html',ad_dict)
		else:
			return render(request,'new_mix_3.html',{'count':1,'title':'Begin Mix','message':message,'s':sett,'link':url,'token':keyy,'meta':meta})
	elif request.method == 'GET':
		return render(request,'new_mix_3.html',{'count':1,'title':'Begin Mix','message':message,'s':sett,'link':url,'token':keyy,'meta':meta})

	else:
		return render(request,'404.html',{'s':sett,'link':url,'token':keyy})

def generate_code(length=10):
	choice = [1,2,3]
	x = 1
	final_code = ''
	while x <= length:
		c = random.choice(choice)
		if c == 1:
			final_code += str(random.choice(string.ascii_lowercase))
		elif c == 2:
			final_code += str(random.choice(string.ascii_uppercase))
		else:
			final_code += str(random.randint(0,9))

		x += 1

	return final_code


def create_mix(request):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	if request.method == 'POST':
		res = check_protection(request)
		if res:
			pass
		else:
			return redirect('/viewprotection')
		h = get_handler('BTC')
		sett = Settings.objects.all()[0]
		#idd = ''.join(str(uuid.uuid1()).split('-'))
		idd = generate_code(length=20)
		total = 0

		add = request.POST.get('add','')
		if add != '':
			add_list = []
			for x in range(1,4):
				address = request.POST.get('address{0}'.format(str(x)),'')
				if address  != '':
					add_list.append(address)

				else:
					pass
			return new_mix_2(request,count=add,adds=add_list)
		else:
			pass
		correction = False
		for x in range(1,4):
			print(x)

			address = request.POST.get('address{0}'.format(str(x)),'')
			print(address)
			delay = request.POST.get('delay{0}'.format(str(x)),'')
			percentage = request.POST.get('percent{0}'.format(str(x)),'')
			captcha = request.POST.get('captcha','')
			#key = request.POST.get('token','')
			lg = request.POST.get('lang','')
			print(delay)
			print(percentage)
			if address != '' and delay != '' and percentage !=  '' and captcha != '': #and key != '':
				#resp_cont = CaptchaStore.objects.filter(hashkey = key)
				#print(key)
				#print(len(resp_cont))
				#resp = resp_cont[0].response
				#print(resp)
				print(captcha)
				if captcha:

					pass
				else:
					return new_mix_2(request,message='Captcha Not Valid')
				if x == 1:
					mixes = Mix.objects.all().order_by('-number')
					try:
						recent_number = mixes[0].number
					except:
						recent_number = 0
					current_number = recent_number + 1
					rest = current_number % sett.shuffle_num
					status = Winner_status.objects.all()
					if len(status) != 0 :
						status = status[0]
					else:
						status = Winner_status.objects.create()
						status.save()
					print('result')
					print(rest)

					if rest == 0:

						status.status = False
						status.save()
						winner = True
					else:
						if status.status:
							status.status = False
							status.save()
							winner  = True
						else:
							winner = False
					print(winner)
					m = Mix.objects.create(mix_id=idd,number=current_number,winner=winner)
					address_d = h.send('getnewaddress',main_test_label)
					m.deposit_address = address_d
					m.save(new=True)
				try:
					if float(percentage) <= 0:
						percentage = '0'
					total += float(percentage)
					if check_valid(address,h):
						if total <= 100:
							if float(percentage) == 0:
								continue
							set_ = m.addresses_set.create(address=address,percentage=float(percentage),delay=int(delay),status='delaying ...')
						else:
							request.session['message']  = True
							perc_res = float(100 - (total -  float(percentage)))
							if perc_res <= 0 :
								perc_res = 0
							if perc_res == 0:
								continue
							set_ = m.addresses_set.create(address=address,percentage=perc_res,delay=int(delay),status='delaying ...')
					else:
						return new_mix_2(request,message='not a valid address ...')
				except Exception as e:
					print(str(e))
					return new_mix_2(request,message='not  valid  ...')



			else:
				continue
		if total < 100:
			request.session['message']  = True
			print('changing')
			print(100 - total)
			print(set_.percentage)
			set_.percentage += 100 - total
			set_.save()



		return redirect('/{0}/check?idd={1}'.format(lg,idd))
		#return check(request,message=correction,idd_in=idd)
	else:
		return redirect('/{0}/newmix'.format(lg))


def check_in(request):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	res = check_protection(request)
	if res:
		pass
	else:
		return redirect('/viewprotection')
	idd = request.GET.get('idd','')
	if idd != '':
		mix = Mix.objects.filter(mix_id=idd)
		if len(mix) != 0:
			mix = mix[0]
			if mix.mix_status == 'awaiting deposit ...':
				addresses = mix.addresses_set.all()
				ret_dict = {
				'mix':mix,
				'addresses':addresses,
				'len':str(len(addresses))
				}
				return render(request,'awaiting_depo.html',ret_dict)
			elif mix.mix_status == 'Waiting fo confirmation ....':
				addresses = mix.addresses_set.all()
				ret_dict = {
				'mix':mix,
				'addresses':addresses,
				'len':str(len(addresses))
				}
				return render(request,'received.html',ret_dict)
			elif mix.mix_status == 'Mixing ....':
				addresses = mix.addresses_set.all()
				ret_dict = {
				'mix':mix,
				'addresses':addresses,
				'len':str(len(addresses))
				}
				return render(request,'started.html',ret_dict)
			elif mix.mix_status == 'done':
				addresses = mix.addresses_set.all()
				ret_dict = {
				'mix':mix,
				'addresses':addresses,
				'len':str(len(addresses))
				}
				return render(request,'completed.html',ret_dict)



		else:
			return HttpResponse('not found')
	else:
		return HttpResponse('not valid')

def check(request,message=False,idd_in =''):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	message = request.session.get('message',False)
	if message:
		del request.session['message']
	else:
		pass
	res = check_protection(request)
	if res:
		pass
	else:
		return redirect('/viewprotection')
	if idd_in == '':
		idd = request.GET.get('idd','')
	else:
		idd = idd_in
	if idd != '':
		idd = idd.strip()
		mix = Mix.objects.filter(mix_id=idd)
		if len(mix) != 0:
			mix = mix[0]
			sett = Settings.objects.all()[0]
			addresses = mix.addresses_set.all()
			if mix.mix_status == 'pending':
				if 'minimum' in mix.message:
					status = 1
				elif 'maximum' in mix.message:
					status = 2
				elif 'equals'  in mix.message:
					status = 3
			elif mix.mix_status == 'Waiting for confirmation ....':
				status = 4
			else:
				status = 0

			total = sett.t_fee * len(addresses)

			ret_dict = {
				'mix':mix,
				'adds':addresses,
				'txids':mix.txid.split(','),
				'len':str(len(addresses)),
				'status':status,
				'sett':sett,
				'total':total,
				'correction':message,
				'title':'status',
				's':sett
				}
			return render(request,'mix_status.html',ret_dict)




		else:
			return render(request,'404.html')
	else:
		return HttpResponse('not valid')


def overview(request,idd):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	res = check_protection(request)
	if res:
		pass
	else:
		return redirect('/viewprotection')
	mix = Mix.objects.filter(mix_id=idd)
	if len(mix) != 0:
		mix = mix[0]
		sett = Settings.objects.all()[0]
		min_ = sett.min_usr_pay
		max_ = sett.max_usr_pay
		ret_dict = {
		'mix' :  mix,
		'min':min_,
		'max':max_,
		'title':'overview',
		's':sett
		}
		return render(request,'deposit.html',ret_dict)
	else:
		return HttpResponse('not found')

def refresh(request):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	if request.method == 'POST':
		idd = request.POST.get('idd','')
		if idd != '':
			mix = Mix.objects.filter(mix_id=idd)
			if len(mix) != 0:
				mix = mix[0]
				h = get_handler('BTC')
				address = h.send('getnewaddress',main_test_label)
				print('updating')
				mix.deposit_address = address
				mix.save()
				print('saving')
				return HttpResponse(json.dumps({'status':True,'address':address}))
			else:
				return HttpResponse('not found')
		else:
			return HttpResponse(json.dumps({'status':False}))
	else:
		return HttpResponse(json.dumps({'status':False}))


def delete_mix_usr(request):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	res = check_protection(request)
	if res:
		pass
	else:
		return redirect('/viewprotection')
	sett = Settings.objects.all()[0]
	if request.method == 'POST':
		lg = request.POST.get('lang','')
		idd = request.POST.get('idd','')
		mix = Mix.objects.filter(mix_id=idd)
		if len(mix) == 0:
			return render(request,'status.html',{'message':'session ID not found','s':sett})
		else:
			mix = mix[0]
			mix.delete()
			return redirect('/{0}'.format(lg))
	else:
		idd = request.GET.get('idd','')

		return render(request,'delete.html',{'title':'Delete Mix','s':sett,'idd':idd})


def send_mail(request):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	res = check_protection(request)
	if res:
		pass
	else:
		return redirect('/viewprotection')
	ckey = CaptchaStore.pick()
	pkey = pgp_public
	#print(keyy)
	url_c = captcha_image_url(ckey)
	if request.method == 'POST':

		email = request.POST.get('email','')
		subject = request.POST.get('subject','')
		idd = request.POST.get('session','')
		message = request.POST.get('bodyMessage','')
		captcha = request.POST.get('captcha','')
		#keyy = request.POST.get('token','')
		print(captcha)
		if email != '' and subject != '' and idd != '' and message != '' and captcha != '' :#and keyy != '':
			#resp_cont = CaptchaStore.objects.filter(hashkey = keyy)
			#print(len(resp_cont))
			#resp = resp_cont[0].response
			#print(resp)
			if captcha:

				pass
			else:
				return render(request,'contact.html',{'message':'captcha not valid','key':pkey,'link':url_c,'token':ckey})
			pre_message = "MIX ID :  {0} \nEMAIL  :  {1} \n".format(idd,email)
			message = pre_message + message
			sett = Settings.objects.all()[0]

			email_temp = {
				'subject':'{0}'.format(subject) ,
				'html': '<p>'+message+'</p>',
				'text': message,
				'from': {'name': 'Anonymix', 'email': '{0}'.format(sender_mail)},
				'to': [
					{'name': 'User', 'email': sett.support_mail}
				]
			}
			#input(email_temp)
			#sg = SendGridAPIClient(send_grid_api_key)
			s = PySendPulse(key,private)
			resp = s._PySendPulse__handle_result(s._PySendPulse__send_request('smtp/emails', 'POST', {'email': json.dumps(email_temp)}))
			if resp['result']:
				return render(request,'contact.html',{'message':'success','key':pkey,'link':url_c,'token':ckey})
			else:
				return render(request,'contact.html',{'message':'failed','key':pkey,'link':url_c,'token':ckey})

		else:
			return render(request,'contact.html',{'message':'failed','key':pkey,'link':url_c,'token':ckey})

	else:
		return render(request,'contact.html',{'message':'failed','key':pkey,'link':url_c,'token':ckey})




"""
message = Mail(
    from_email=email,
    to_emails=sett.support_mail,
    subject='[{0}] {1}'.format(idd,subject),
    html_content=message)

	"""




def contact(request):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	res = check_protection(request)
	if res:
		pass
	else:
		return redirect('/viewprotection')

	key = pgp_public
	sett = Settings.objects.all()[0]
	keyy = CaptchaStore.pick()
	print(keyy)
	url = '/gencaptcha'
	meta = PageMeta.objects.filter(page=5)
	if len(meta) == 0:
		meta = PageMeta.objects.create(page=5)
		meta.save()
	else:
		meta = meta[0]
	return render(request,'contact.html',{'title':'Contact','s':sett,'key':key,'link':url,'token':keyy,'meta':meta})


def status(request):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	res = check_protection(request)
	if res:
		pass
	else:
		return redirect('/viewprotection')
	sett = Settings.objects.all()[0]
	meta = PageMeta.objects.filter(page=2)
	if len(meta) == 0:
		meta = PageMeta.objects.create(page=2)
		meta.save()
	else:
		meta = meta[0]
	return render(request,'status.html',{'title':'Mix Info','s':sett,'meta':meta})
def view_faq(request):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	res = check_protection(request)
	if res:
		pass
	else:
		return redirect('/viewprotection')
	sett = Settings.objects.all()[0]
	meta = PageMeta.objects.filter(page=3)
	if len(meta) == 0:
		meta = PageMeta.objects.create(page=3)
		meta.save()
	else:
		meta = meta[0]
	return render(request,'faq.html',{'s':sett,'title':'FAQ','meta':meta})

def view_key(request):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	res = check_protection(request)
	if res:
		pass
	else:
		return redirect('/viewprotection')
	key = pgp_public
	sett = Settings.objects.all()[0]
	return render(request,'public_pgp.html',{'s':sett,'key':key})


def error_404(request,exception):
	sett = Settings.objects.all()[0]
	return render(request,'404.html',{'s':sett})

##### check api #####

def check_if_active():
	name = Proc.objects.all()
	if len(name) == 0:
		return False
	else:
		name = name[0].name

	for pr in threading.enumerate():
		if pr.name == name:
			if pr.is_alive():
				return True
			else:
				return False
	return False

@csrf_exempt
def check_code_status(request):
	if request.method == 'POST':
		secret = request.POST.get('code','')
		print(secret)
		print(secret_code)
		if secret == secret_code:
			print('before')
			result = check_if_active()
			print('after')
			print(result)
			if result:
				return HttpResponse(json.dumps({'response':True,'runing':True}))
			else:
				return HttpResponse(json.dumps({'response':True,'runing':False}))
		else:
			return HttpResponse(json.dumps({'response':False}))
	else:
		return HttpResponse(json.dumps({'response':False}))

@csrf_exempt
def start_code(request):
	if request.method == 'POST':
		secret = request.POST.get('code','')
		if secret == secret_code:
			try:
				tr = threading.Thread(target=start)
				tr.daemon = True
				tr.start()
				procs = Proc.objects.all()
				if len(procs) == 0:
					pr = Proc.objects.create(name='worker1')
				else:
					pr = procs[0]


				pr.save()
				tr.name = pr.name
				return HttpResponse(json.dumps({'response':True,'started':True}))
			except Exception as e:
				return HttpResponse(json.dumps({'response':True,'error':str(e)}))

		else:
			return HttpResponse(json.dumps({'response':False}))
	else:
		return HttpResponse(json.dumps({'response':False}))
