from mixer.models import *
from an_back.settings import *
from admin_section.models import *
from .nod_handler import *
import time
import datetime




class worker():
	def __init__(self):
		self.handler = get_handler('BTC')

	def check_balance(self,balance,old):
		if balance <= old:
			return True
		else:
			return False

	def check_if_active(self,mix,sett):
		days = self.get_days(mix.date)
		if days >= ( sett.d_inactive * 24 ):
			if mix.mix_status != 'Mixing ....' and mix.mix_status != 'Waiting for confirmation ....':
				mix.status = 'not active'
				mix.save()
				return True
			else:
				return False
		else:
			return False


	def get_transaction(self,address,trs):
		txids = []
		for tr in trs:
			if tr['address'] == address:
				print('getting transaction')
				print(tr['txid'])
				txids.append(tr['txid'])
				res  = self.locker(lock=True,txid= tr['txid'])
				if res:
					print('locked')
				else:
					print('not locked')

			else:
				pass

		return txids

	def locker(self,lock=True,txid=''):
		print(txid)
		array = [{"txid":str(txid),"vout":0}]
		print(array)

		if lock:
			lst = self.handler.send('listunspent',0)
			for l in lst:
				if txid == l['txid']:
					array[0]['txid'] = l['txid']
					array[0]['vout'] = l['vout']
					res = self.handler.send('lockunspent',False,aray=array)
					if res:
						print('locked')
						return True
					else:
						print('not locked')
						return False
		else:
			lst = self.handler.send('listlockunspent')
			for l in lst:
				if txid == l['txid']:
					array[0]['txid'] = l['txid']
					array[0]['vout'] = l['vout']
					res = self.handler.send('lockunspent',True,aray=array)
					if res:
						print('unlocked')
						return True
					else:
						print('not unlocked')
						return False

	def get_confirmations(self,txid,mix):
		confirmation = 999999
		non_confirmed = 0
		for tx in txid.split(','):
			tr = self.handler.send('gettransaction',tx)
			if int(tr['confirmations']) == 0:
				print('###################### Detected  #######################')
				non_confirmed += round(float(tr['amount']),8)
			if int(tr['confirmations']) <= confirmation:
				confirmation = int(tr['confirmations'])
		print('###################### Saving  #######################')
		mix.non_confirmed = non_confirmed
		mix.save()
		return confirmation

	def check_deposit(self,address,sett,mix):
		print('start check')
		print(address)
		amount = self.handler.send('getreceivedbyaddress',address,0)
		amount_in = amount
		res = self.check_balance(round(float(amount),8),mix.initial_deposit)
		if res:

			if 'yet' not in mix.txid:
				pass
			else:
				print('deposit not received yet')
				return [False]
		else:
			print('deposit received')
			print('balance changed')
			pass

		txid = self.get_transaction(address,self.handler.send('listtransactions','*',999999999))
		print('txids elements')
		print(txid)
		if len(txid) != 0:
			mix.txid= ','.join(txid)
			mix.save()
		else:
			print('no txid')
			return [False]
		if 'yet' not in mix.txid:

			mix.initial_deposit = round(float(amount),8)
			confirmations = self.get_confirmations(mix.txid,mix)
			mix.current_confirmations = confirmations
			mix.save()
			new = False
			if mix.current_confirmations >= 1:
				if mix.winner:
					bonus = float(amount*(sett.shuffle_perc/100))
					amount_temp = amount + bonus
					print(amount_temp)
					if amount_temp > sett.max_usr_pay or amount_temp >= (0.1 * sett.max_usr_pay):
						mix.winner = False
						mix.save()
						status = Winner_status.objects.all()[0]
						status.status = True
						statsu = True
						status.save()
					else:
						mix.bonus = float(amount*(sett.shuffle_perc/100))
						mix.deposit_amount += mix.bonus
						mix.deposit_amount = round(mix.deposit_amount,8)
						amount = round(amount_temp,8)
						new = True
						mix.winner  = False
						mix.validated_winner = True
						mix.save()
			else:
				return [True,'confirmation']

			amount = self.handler.send('getreceivedbyaddress',address,0)
			amount_in = amount

			if amount_in < sett.min_usr_pay:
				mix.deposit_amount = float(amount_in)
				mix.winner = False
				mix.save()
				return [True,'minimum amount not reached']
			elif amount_in > sett.max_usr_pay:
				mix.deposit_amount = float(amount_in)
				mix.winner = False
				mix.save()
				return [True,'maximum amount reached']
			else:
				print('deposit')
				print(mix.deposit_amount)
				print(mix.bonus)
				#prec = len(str(mix.bonus).split('.')[-1])
				prec = 8
				print(prec)

				check_amount = round(mix.deposit_amount - mix.bonus,prec)
				print(check_amount)
				if float(amount) > check_amount:
					print('here temp amounts')
					print(mix.amount)
					temp_amount = round(float(amount) - check_amount,prec)
					print(temp_amount)
					if temp_amount == mix.bonus:
						print('it\'s only bonus ')
						if not mix.winner and mix.validated_winner and not new:
							temp_amount = float(amount) + mix.bonus
						else:
							temp_amount = float(amount)
						add = False
					else:
						print('not a bonus added it\'s new')
						add = True

					fees = (temp_amount * (sett.s_fee/100)) + (sett.t_fee * len(mix.addresses_set.all()))
					print(fees)
					if add:
						mix.amount += (temp_amount - fees  )
					else:
						mix.amount = (temp_amount - fees  )
					mix.amount = round(mix.amount,8)
					print('mix amount')
					print(mix.amount)

					mix.deposit_amount = float(amount)
					#input('check')
				else:
					pass

				print(mix.amount)
				if mix.amount  <=  0:
					return [True,'Less or equals 0']

				mix.save()
				#confirmations = self.get_confirmations(mix.txid)
				#mix.current_confirmations = confirmations
				#mix.save()
				print(confirmations)
				if confirmations >= 0:
					if mix.amount <= 20:
						mix.confirmations = 1
						mix.save()
						if confirmations < 1:
							return [True,'confirmation']
						else:
							return [True,'ok']
					else:
						mix.confirmations = 6
						mix.save()
						if confirmations < 6:
							return [True,'confirmation']
						else:
							return [True,'ok']
		else:
			print('still a yet')
			return [False]






	def change_mix_status(self,mix,st):
		mix.mix_status = st
		mix.save()

	def get_days(self,first):
		now = datetime.datetime.now(datetime.timezone.utc)
		#d_first = datetime.date(first.year,first.month,first.day)
		#d_last = datetime.date(now.year,now.month,now.day)
		res =  now - first

		#res = d_last-d_first
		return int( (res.days * 24) +res.seconds // 3600)



	def clear_mixes(self):
		sett = Settings.objects.all()[0]

		mixes = Mix.objects.all()
		for mix in mixes:
			days = self.get_days(mix.date)
			if days >= (sett.d_deleted * 24 ):
				mix.delete()
			else:
				continue

	def send_transaction(self,add,amount,sett):
		print('sending')
		amount = float(amount)
		amount_out = round(float(amount),8)

		if amount_out !=  add.amount_sent:
			temp_amount = amount_out
			amount_out = amount_out - add.amount_sent
			amount_out = round(float(amount_out),8)

			print('sending amount : ',end=' ')
			print(amount_out)

			res = self.handler.send('sendtoaddress',add.address,amount_out,message = True)
			print(res)
			if res[0]:
				add.status = 'done'
				add.txid = ','.join(res)
				#if 'sent' in add.txid:
				#	add.txid = str(res[0])
				#else:
				#	add.txid += ','+str(res)
				add.amount_sent = temp_amount
				
				add.save()
			else:
				add.status = 'failed {0}'.format(res[-1])
				add.amount_sent = 0
				add.save()



	def carry_mix(self,mix,sett):
		print('carrying the mix')
		addresses_container = mix.addresses_set.all()
		for add in addresses_container:
			now = datetime.datetime.now(datetime.timezone.utc)
			diff = now - mix.date
			minutes = int(diff.seconds / 3600) + int(diff.days * 24)
			print(minutes)
			print(add.delay)
			if minutes >= add.delay:
				print('sending transaction')
				self.send_transaction(add,float( mix.amount * (add.percentage/100)),sett)
			else:
				continue

		addresses_container = mix.addresses_set.all()
		all_done = 0
		for x in addresses_container:
			if x.status == 'done':
				all_done += 1
			else:
				continue

		print(len(addresses_container))
		print(all_done)

		if all_done == len(addresses_container):
			txids = mix.txid
			for tx in txids.split(','):
				self.locker(lock=False,txid=tx)
			#mix.status = 'done'
			mix.mix_status = 'done'
			mix.save()













	def main(self):
		try:
			print('strating')
			while True:
				self.clear_mixes()
				mixes = Mix.objects.filter(status = 'active')
				if len(mixes) == 0:
					print('waiting')
					time.sleep(15)
					print('restarting')
					continue
				else:
					time.sleep(10)
				for mix in mixes:
					print('checking the mix : ',end=' ')
					print(mix.mix_id)
					sett = Settings.objects.all()[0]
					res_ch = self.check_if_active(mix,sett)
					if res_ch:
						continue
					else:
						pass

					res = self.check_deposit(mix.deposit_address,sett,mix)
					print('returned')
					print(res)
					if res[0]:
						if res[-1] == 'ok':
							self.change_mix_status(mix,'Mixing ....')
							self.carry_mix(mix,sett)
						elif res[-1] == 'confirmation':
							self.change_mix_status(mix,'Waiting for confirmation ....')

						else:
							if 'minimum' in res[-1]:
								mix.mix_status = 'pending'
							elif 'equals' in res[-1]:
								mix.mix_status = 'pending'

							else:
								mix.status = 'pending'
								mix.mix_status = 'pending'
								notif = Notifications.objects.create(mix_id=mix.mix_id,message=res[-1])
								notif.save()
							mix.message = res[-1]

							mix.save()


					else:
						continue



		except Exception as e:
			try:
				err  = Errors.objects.create(mix_id=mix.mix_id,error=str(e))
			except:
				err = Errors.objects.create(mix_id='Unknown',error=str(e))

			err.save()
