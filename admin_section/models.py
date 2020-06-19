from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class User(models.Model):
	username = models.CharField(max_length=255,unique=True)
	password = models.CharField(max_length=255)

	def __str__(self):
		return self.username


class Settings(models.Model):
	s_fee = models.FloatField(default=0)
	t_fee = models.FloatField(default=0)
	support_mail = models.CharField(max_length=300,default='')
	min_usr_pay = models.FloatField(default=0)
	max_usr_pay = models.FloatField(default=0)
	max_usr_disp_pay = models.FloatField(default=0)
	d_inactive = models.FloatField(default=0)
	d_deleted = models.FloatField(default=0)
	donation = models.CharField(max_length=300,default='')
	site = models.CharField(max_length=300,default='')
	protection = models.BooleanField(default=False)
	shuffle_num = models.IntegerField(default=0)
	shuffle_perc = models.FloatField(default=0)
	mirror = models.TextField(default='')
	#banner settings
	banner_show  = models.BooleanField(default=False)
	banner_color = models.CharField(default='red',max_length=255)
	bold = models.CharField(max_length=1000,default='')
	banner_text = models.CharField(max_length=1000,default='')



	def __str__(self):
		return self.support_mail


class Notifications(models.Model):
	mix_id = models.CharField(max_length=255)
	message = models.CharField(max_length = 255)

	def __str__(self):
		return self.mix_id + ' ' + self.message



class PageMeta(models.Model):
	page = models.IntegerField(default = 0)
	title = models.CharField(max_length = 300,default='')
	keywords = models.CharField(max_length=300,default='')
	description = models.CharField(max_length = 500,default='')
	cronical = models.CharField(max_length=300,default='')

	def __str__(self):
		return "[{0}] {1} ".format(str(self.page),self.title)
