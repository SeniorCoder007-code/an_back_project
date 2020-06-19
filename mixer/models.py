from django.db import models

# Create your models here.


class Mix(models.Model):
	mix_id  = models.CharField(max_length=255)
	status =   models.CharField(max_length=255,default='active')
	mix_status = models.CharField(max_length=255,default='awaiting deposit ...')
	deposit_address = models.CharField(max_length=1000,default='')
	date = models.DateTimeField(auto_now_add=True)
	amount = models.FloatField(default=0)
	deposit_amount = models.FloatField(default=0)
	initial_deposit = models.FloatField(default=0)
	bonus = models.FloatField(default=0)
	message = models.CharField(max_length=500,default='')
	txid = models.CharField(max_length=500,default='not yet')
	confirmations = models.IntegerField(default=1)
	current_confirmations = models.IntegerField(default=0)
	number = models.IntegerField(default=0)
	winner = models.BooleanField(default=False)
	validated_winner = models.BooleanField(default=False)
	non_confirmed = models.FloatField(default=0)


	def __str__(self):
		return self.mix_id

	def save(self,new=False,*args, **kwargs):
		print(new)
		if new:
			super(Mix, self).save(*args, **kwargs)
		else:
			mix = Mix.objects.filter(mix_id = self.mix_id)
			print('length')
			print(len(mix))
			if len(mix) == 0 :
				return False
			else:
				print('saving here')
				super(Mix, self).save(*args, **kwargs)


class Winner_status(models.Model):
	status = models.BooleanField(default=False)

	def __str__(self):
		return str(self.status)




class Addresses(models.Model):
	mix =  models.ForeignKey(Mix,on_delete=models.CASCADE)
	percentage = models.FloatField()
	address = models.CharField(max_length=1000)
	delay = models.IntegerField()
	status = models.CharField(max_length=300,default='not done')
	amount_sent = models.FloatField(default = 0)
	message = models.CharField(max_length=500,default='')
	txid = models.CharField(max_length=5000,default='not sent yet')

	def __str__(self):
		return self.mix.mix_id  + self.address


class ViewProtection(models.Model):
	password = models.CharField(max_length=500)

	def __str__(self):
		return self.password


class Errors(models.Model):
	mix_id = models.CharField(max_length=255)
	error  = models.CharField(max_length=1000)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.date)

class Proc(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return str(self.name)
