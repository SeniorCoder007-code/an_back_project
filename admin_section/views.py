from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *
from blog.models import *
from mixer.models import *
from mixer.nod_handler import *
from mixer.views import *

# Create your views here.


def login(request):
	username = request.session.get('user','')
	if username != '':
		return redirect('/bitadm/panel')
	else:

		return render(request,'login.html')


def verify_login(request):
	if request.method == 'POST':
		username = request.POST.get('username','')
		password = request.POST.get('password','')

		if username == '' or password == '':
			return render(request,'login.html',{'message':'empty field'})

		usr = User.objects.filter(username =  username )
		if len(usr) != 0:
			usr = usr[0]
			if password == usr.password:
				request.session.set_expiry(0)
				request.session['user'] = usr.username
				return  redirect('/bitadm/panel')
			else:
				return render(request,'login.html',{'message':'password is incorrect'})

		else:
			return render(request,'login.html',{'message':'user not found'})

	else:
		return HttpResponse('not valid')


def view_panel(request):
	username = request.session.get('user','')
	if username != '':
		usr = User.objects.filter(username = username)[0]
		notifications = Notifications.objects.all()
		mixes = Mix.objects.all().order_by('-date')
		num  = request.GET.get('rank','')
		if num != '':
			try:
				num = int(num)
			except:
				num = 0
		else:
			num = 0

		mixes_list = []
		counter = 1
		partial_list = []
		for x in mixes:

			if counter % 100 == 0:
				partial_list.append((counter,x))
				mixes_list.append(partial_list)
				partial_list = []

				counter += 1
			else:
				partial_list.append((counter,x))
				counter += 1
		if len(partial_list) >  0:
			mixes_list.append(partial_list)
			partial_list =  []

		if num + 1 <= len(mixes_list)  and num >= 0:
			fin_mixes = mixes_list[num]
		else:
			try:
				fin_mixes = mixes_list[0]

			except:
				fin_mixes = []
			num = 0


		ret_dict = {
		'notifications':notifications,
		'mixes':fin_mixes,
		'counter':num
		}

		return render(request,'dashboard.html',ret_dict)
	else:
		return render(request,'login.html',{'message':'please blog_login first'})

def delete_notif(request,idd):
	username = request.session.get('user','')
	if username != '':
		notif = Notifications.objects.filter(mix_id=idd)[0]
		notif.delete()
		return redirect('/bitadm/panel')
	else:
		return render(request,'login.html')

def delete_mix(request,idd):
	username = request.session.get('user','')
	if username != '':
		mix = Mix.objects.filter(mix_id=idd)[0]
		mix.delete()
		return redirect('/bitadm/panel')
	else:
		return render(request,'login.html')

def view_settings(request,message=False,error=False):
	username = request.session.get('user','')
	if username != '':
		s = Settings.objects.all()[0]
		notifications = Notifications.objects.all()
		if len(notifications) == 0:
			notifications  = False
		return render(request,'settings.html',{'s':s,'notifications':notifications,'message':message,'error':error})
	else:
		return render(request,'login.html')


def change_sett(request):
	if request.method == 'POST':
		username = request.session.get('user','')
		if username != '':
			s = Settings.objects.all()[0]
			s_fee = request.POST.get('s_fee','')
			t_fee = request.POST.get('t_fee','')
			supp_mail = request.POST.get('supp_mail','')
			min_usr_pay = request.POST.get('min_usr_pay','')
			max_usr_pay = request.POST.get('max_usr_pay','')
			max_usr_disp_pay = request.POST.get('max_usr_disp_pay','')
			d_inactive = request.POST.get('d_inactive','')
			d_deleted = request.POST.get('d_deleted','')
			protection = request.POST.get('protection','')
			donation = request.POST.get('donation','')
			site = request.POST.get('site','')
			s_perc = request.POST.get('shuffle_perc','')
			s_num = request.POST.get('shuffle_num','')
			show = request.POST.get('show','')
			color = request.POST.get('color','')
			btext = request.POST.get('btext','')
			text = request.POST.get('text','')
			mirrors = request.POST.get('mirror','')
			page = request.POST.get('page','')
			page_title = request.POST.get('title',None)
			page_keywords = request.POST.get('keywords',None)
			page_description = request.POST.get('description',None)
			cronical = request.POST.get('cronical',None)


			if s_fee != '':
				s.s_fee = float(s_fee)
				s.save()
			print('protection')
			print(protection)

			if mirrors != '':
				s.mirror = mirrors
				s.save()

			if protection != '':
				print('here')
				print(protection)
				if protection == '1':
					s.protection  = True
					s.save()
				else:
					s.protection = False
					s.save()

			if show != '':
				if int(show) == 1:
					s.banner_show = True
				else:
					s.banner_show = False
				s.save()

			if color != '':
				s.banner_color = color
				s.save()

			if btext != '':
				s.bold = btext
				s.save()

			if text != '':
				s.banner_text = text
				s.save()


			if s_num != '':
				s.shuffle_num = int(s_num)
				s.save()

			if t_fee != '':
				s.shuffle_perc = float(s_perc)
				s.save()

			if t_fee != '':
				s.t_fee = float(t_fee)
				s.save()

			if site  != '':
				s.site = site
				s.save()

			if donation  != '':
				s.donation = donation
				s.save()

			if supp_mail != '':
				s.support_mail = supp_mail
				s.save()

			if min_usr_pay != '':
				s.min_usr_pay = float(min_usr_pay)
				s.save()

			if max_usr_pay != '':
				s.max_usr_pay = float(max_usr_pay)
				s.save()

			if max_usr_disp_pay != '':
				s.max_usr_disp_pay = float(max_usr_disp_pay)
				s.save()

			if  d_inactive != '':
				s.d_inactive = float(d_inactive)
				s.save()

			if d_deleted != '':
				s.d_deleted = d_deleted
				s.save()

			if page != '':
				if not any([x == None for  x in [page_title,page_description,page_keywords,cronical]]):
					try:
						meta = PageMeta.objects.filter(page = int(page))
						if len(meta) == 0:
							meta = PageMeta.objects.create(page = int(page),title = page_title ,keywords = page_keywords ,description = page_description,cronical=cronical )
						else:
							meta = meta[0]
							meta.title = page_title
							meta.keywords = page_keywords
							meta.description = page_description
							meta.cronical = cronical
						meta.save()

					except:
						pass

			return view_settings(request,message='success')
		else:
			return render(request,'login.html')




	else:
		return view_settings(request,error='failed')


def view_all_posts(request,message=False):
	username = request.session.get('user','')
	if username != '':
		posts = Posts.objects.all().order_by('-date')
		notifications = Notifications.objects.all()
		if len(notifications) == 0:
			notifications  = False
		return render(request,'all_posts.html',{'posts':posts,'message':message})
	else:
		return render(request,'login.html')


def new_post(request):
	username = request.session.get('user','')
	if username != '':
		notifications = Notifications.objects.all()
		if len(notifications) == 0:
			notifications  = False
		return render(request,'add.html',{'notifications':notifications})
	else:
		return render(request,'login.html')
def balance(request):
	username = request.session.get('user','')
	if username != '':
		notifications = Notifications.objects.all()
		if len(notifications) == 0:
			notifications  = False
		h = get_handler('BTC')
		address = h.send('getnewaddress','deposit')
		balance = h.send('getbalance')
		return render(request,'balance.html',{'notifications':notifications,'deposit':address,'balance':balance})
	else:
		return render(request,'login.html')

def start_worker(request):
	username = request.session.get('user','')
	if username != '':
		tr = threading.Thread(target=start)
		tr.daemon = True
		tr.start()
		procs = Proc.objects.all()
		if len(procs) == 0:
			pr = Proc.objects.create(name='test')
		else:
			pr = procs[0]

		pr.name = tr.name
		pr.save()
		return HttpResponse('success')
	else:
		return render(request,'login.html')

def add_new_post(request):
	if request.method == 'POST':
		username = request.session.get('user','')
		if username == '':
			return redirect('/bitadm')
		else:
			if request.method == 'POST' and request.FILES['myfile'] :
				myfile = request.FILES['myfile']
				title = request.POST.get('title')
				description =request.POST.get('description')
				#tag = request.POST.get('tag')
				m_title = request.POST.get('metatitle')
				m_desc = request.POST.get('metadesc')
				m_key = request.POST.get('metakey')
				fs = FileSystemStorage()
				cronical = request.POST.get('cronical','')

				filename = fs.save(myfile.name, myfile)
				uploaded_file_url = fs.url(filename)
				print('url here')
				print(uploaded_file_url)
				p = Posts.objects.create(
					title = title,
					small_description = m_desc,
					content = description,
					image = uploaded_file_url,
					meta_title = m_title,
					meta_key = m_key,
					cronical = cronical
				)
				p.save()
				message = 'success'
			else:
				message = 'failed'

			return view_all_posts(request,message)

	else:
		return HttpResponse('not valid')

def modify(request,slug):
	username = request.session.get('user','')
	if username != '':
		post  = get_object_or_404(Posts,slug=slug)
		notifications = Notifications.objects.all()
		if len(notifications) == 0:
			notifications  = False
		return render(request,'modify.html',{'post':post,'notifications':notifications})
	else:
		return redirect('/bitadm')

def modify_post(request):
	username = request.session.get('user','')
	if username == '':
		return redirect('/bitadm')
	else:
		if request.method == 'POST' and request.FILES.get('myfile',True) :
			myfile = request.FILES.get('myfile','')
			slug = request.POST.get('slug')
			title = request.POST.get('title')
			description =request.POST.get('description')


			m_title = request.POST.get('metatitle')
			m_desc = request.POST.get('metadesc')
			m_key = request.POST.get('metakey')
			cronical = request.POST.get('cronical','')

			p = get_object_or_404(Posts,slug=slug)
			p.title = title
			if len(description) == 0 and len(p.content) == 0:
				pass
			else:
				if len(p.content) != 0:
					if len(description) != 0:
						p.content = description
					else:
						pass
				else:

					p.content = description

			if myfile == '':
				pass
			else:
				fs = FileSystemStorage()
				filename = fs.save(myfile.name, myfile)
				uploaded_file_url = fs.url(filename)
				print(uploaded_file_url)
				p.image = uploaded_file_url
			p.meta_title = m_title
			p.meta_key = m_key
			p.small_description = m_desc
			p.cronical  = cronical
			p.save()
			message = 'success'
		else:
			message  = 'failed'
		return view_all_posts(request,message)

def delete_post(request,slug):
	username = request.session.get('user','')
	if username == '':
		return redirect('/bitadm')
	else:

		post = get_object_or_404(Posts,slug=slug)
		post.delete()
		message = 'success'
		return view_all_posts(request,message)

def logout(request):
	del request.session['user']
	return redirect('/bitadm')
