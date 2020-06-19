import os
import json
import requests as req
import logging
import time
from pysendpulse.pysendpulse import PySendPulse





class Checker:

	def __init__(self):
		self.code = 'a6d2fad4-0e44-11ea-b2cc-f40f24360bd9'
		# please type the url in this form http://www.example.com/ (replace http by https if the domain has https enabled)
		self.main_url = 'http://127.0.0.1:8000/'
		logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		self.sender_email = '' # here you put the support email
		self.email = ''
		self.key = ''
		self.private = ''


	def report_error(self,reason,message):
		full_message = reason + ' ' + message
		subject = '[Checker Script Report]'
		email_temp = {
				'subject':'{0}'.format(subject) ,
				'html': '<p>'+full_message+'</p>',
				'text': full_message,
				'from': {'name': 'Anonymix', 'email': '{0}'.format(self.sender_email)},
				'to': [
					{'name': 'User', 'email': self.email}
				]
			}
			#input(email_temp)
			#sg = SendGridAPIClient(send_grid_api_key)
		s = PySendPulse(self.key,self.private)
		resp = s._PySendPulse__handle_result(s._PySendPulse__send_request('smtp/emails', 'POST', {'email': json.dumps(email_temp)}))
		if resp['result']:
			return True
		else: 
			return False
		



	def log(self,message,type=0):
		if type == 0:
			logging.debug(message)
		else:
			logging.error(message)

		


	def handle_request(self,url):
		params = {
			'code':self.code
		}
		max_try = 0
		print('here')
		err = False
		while max_try < 3:
			try:
				resp = req.post(self.main_url + url,data=params,timeout=60)
				print(resp.content)
				print(resp.status_code)
				if resp.status_code != 200:
					max_try += 1
					continue
				else:
					data = json.loads(resp.content.decode())
					return data
				

			except Exception as e:
				max_try += 1
				err = str(e)
				continue
		print('here2')
		if err:
			self.report_error('communication error with the server (might be down)',str(err))
			self.log('communication error with the server (might be down) ' + str(err) , type=1 )

			return False
		else:
			self.report_error('communication error with the server (might be down)','')
			self.log('communication error with the server (might be down) ' + '' , type=1 )
			return False

	def is_runing(self):
		data = self.handle_request('api/check')
		if data:
			response = data['response']
			if response:
				if data['runing']:
					self.log('Thread runing ....')
					return True

				else:
					self.log('not Runing ...')
					return False
			


	def main(self):
		try:
			print('start checking')
			data = self.handle_request('api/check')
			runing  = False
			counter = 0
			for _ in range(100):
				print('check')
				time.sleep(30)
				res = self.is_runing()
				if res:
					counter += 1
				else:
					continue
			
			if counter > 0:
				runing = True


			if runing:
				self.log('Thread runing after 20 checks  ....')

			else:
				self.log('Thread not runing restarting it now ...')
				data1 = self.handle_request('api/start')
				if data1:
					response = data1['response']
					if response:
						if 'error' in data1.keys():
							self.report_error('error in the api response ',data1['error'])
							self.log(data1['error'],type=1)
						elif 'started' in data1.keys():
							self.log('background process started')
						else:
							self.log('UKNOWN ERROR ',type=1)

					else:
						pass
				else:
					pass

		
		except Exception as e:
			print('error')
			print(str(e))
			self.log(str(e),type=1)
			self.report_error(str(e),'')


print('starting the checker')
ch  = Checker()
ch.main()

	