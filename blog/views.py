from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from .models import *
from blog.models import *
from django.core.files.storage import FileSystemStorage
from admin_section.models import *
from an_back.settings import *



def check_valid_call(request):
	if request.method == 'post':
		passcall = request.POST.get('passcall',False)
	else:
		passcall = request.GET.get('passcall',False)
	if passcall == callpass:
		return True
	else:
		return False


def view_blog(request):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	part = request.GET.get('page','')
	if part == '':
		part = 0
	else:
		try:
			part = int(part)
		except:
			part = 0
	posts = Posts.objects.all().order_by('-date')
	posts_list = []
	counter = 1
	partial_list = []
	for x in posts:

		if counter % 4 == 0:
			partial_list.append(x)
			posts_list.append(partial_list)
			partial_list = []

			counter += 1
		else:
			partial_list.append(x)
			counter += 1
	if len(partial_list) >  0:
		posts_list.append(partial_list)
		partial_list =  []


	print(partial_list)
	if part+1 <= len(posts_list) and part >= 0:
		pass
	elif part < 0:
		part = 0
	else:
		part = len(posts_list) -1
	print('here')
	if len(posts_list) ==  0:
		print('this1')
		res_posts = []
	else:
		print('this')
		res_posts = posts_list[part]
	print('here2')
	print(res_posts)

	meta = PageMeta.objects.filter(page=4)
	if len(meta) == 0:
		meta = PageMeta.objects.create(page=4)
		meta.save()
	else:
		meta = meta[0]


	populars = Posts.objects.all().order_by('-clicked')
	ret_dict = {}
	ret_dict['posts']= res_posts
	ret_dict['populars'] = populars
	tags = Tags.objects.all()
	ret_dict['tags'] = tags
	ret_dict['pageold'] = str(part + 1)
	ret_dict['pagenew'] = str(part - 1)
	ret_dict['s'] = Settings.objects.all()[0]
	ret_dict['title'] = 'Blog'
	ret_dict['meta'] = meta

	return render(request,'blog_main.html',ret_dict)

def view_post(request,slug):
	rescall = check_valid_call(request)
	if rescall:
		pass
	else:
		return HttpResponse(status=401)
	post = get_object_or_404(Posts,slug=slug)
	populars = Posts.objects.all().order_by('-clicked')
	post.clicked += 1
	ret_dict = {}
	ret_dict['post']=post
	ret_dict['populars'] = populars
	ret_dict['s'] = Settings.objects.all()[0]
	ret_dict['title'] = post.title
	meta = PageMeta.objects.filter(page=4)
	if len(meta) == 0:
		meta = PageMeta.objects.create(page=4)
		meta.save()
	else:
		meta = meta[0]

	meta.title = post.meta_title
	meta.keywords = post.meta_key
	meta.description = post.small_description
	meta.cronical = post.cronical
	ret_dict['meta'] = meta


	return render(request,'blog_details.html',ret_dict)
