"""an URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mixer.views import *
from blog.views import *
from admin_section.views import *
from django.conf.urls.static import static
from an_back import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import include
from .settings import *

urlpatterns = [
    
    path('',index),
    path('newmix',new_mix_2),
    path('contact',contact),
    path('blog',view_blog),
    path('faq',view_faq),
    path('blog/<str:slug>',view_post),
    
    path('status',status),
    path('start',start_worker),
    path('check',check),
    path('overview/<str:idd>',overview),
    path('refresh',refresh),
    path('create',create_mix),
    path('deletenotif/<str:idd>',delete_notif),
    path('deletemix/<str:idd>',delete_mix),
    path('deletemixuser',delete_mix_usr),
    path('bitadm/balance',balance),
    path('sendmail',send_mail),
     path('verifyprot',verify_protection),
    path('viewprotection',view_protection),
    path('key',view_key),
    path('api/check',check_code_status),
    path('api/start',start_code),
     #captcha
    path('captcha',include('captcha.urls')),
    path('isactive',status_prot)




]
if act_db:
    urlpatterns.append(path('bitdbadmin/', admin.site.urls))

urlpatterns += i18n_patterns( # < here
    path('',index),
    path('newmix',new_mix_2),
    path('contact',contact),
    path('blog',view_blog),
    path('faq',view_faq),
    path('blog/<str:slug>',view_post),
   
    path('status',status),
    path('start',start_worker),
    path('check',check),
    path('overview/<str:idd>',overview),
    path('refresh',refresh),
    path('create',create_mix),
    path('deletenotif/<str:idd>',delete_notif),
    path('deletemix/<str:idd>',delete_mix),
    path('deletemixuser',delete_mix_usr),
    path('bitadm/balance',balance),
    path('sendmail',send_mail),
    path('verifyprot',verify_protection),
    path('viewprotection',view_protection),
    path('key',view_key),
    path('captcha',include('captcha.urls'))
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if act_pan:
    urlpatterns += [
        path('bitadm',login),
    path('bitadm/verify',verify_login),
    path('bitadm/panel',view_panel),
    path('bitadm/settings',view_settings),
    path('bitadm/change',change_sett),
    path('bitadm/all',view_all_posts),
    path('bitadm/new',new_post),
    path('bitadm/addpost',add_new_post),
    path('bitadm/modify/<str:slug>',modify),
    path('bitadm/modifypost',modify_post),
    path('bitadm/delete/<str:slug>',delete_post),
    path('bitadm/logout',logout)
    ]

    urlpatterns += i18n_patterns(
        path('bitadm',login),
    path('bitadm/verify',verify_login),
    path('bitadm/panel',view_panel),
    path('bitadm/settings',view_settings),
    path('bitadm/change',change_sett),
    path('bitadm/all',view_all_posts),
    path('bitadm/new',new_post),
    path('bitadm/addpost',add_new_post),
    path('bitadm/modify/<str:slug>',modify),
    path('bitadm/modifypost',modify_post),
    path('bitadm/delete/<str:slug>',delete_post),
    path('bitadm/logout',logout),
    )




handler404 = error_404
