import requests as req
import json
from an_back.settings import *
import time




headers = {'content-type': 'application/json'}
payload = {"jsonrpc": "1.0", "id":"curltest", "method": "", "params": [] }





class Bitcoin:
	def __init__(self):
		#self.user = 'testuser'
		#self.password = 'testpassword'
		#self.url = 'http://{0}:{1}@127.0.0.1:8332/'.format(self.user,self.password)
		self.user = 'exchanger'
		self.password = 'exchangerpass'
		self.url = 'http://{0}:{1}@23.254.176.26:8332/'.format(self.user,self.password)








	def send(self,command,*args,aray=None,message=False):
		if len(args) != 0:
			params = [x for x in args]
			if aray:
				params.append(aray)
			else:
				pass
		else:
			params = []

		custom_payload = payload.copy()
		custom_payload['method'] = command
		custom_payload['params'] = params
		#print(custom_payload)
		# sending and recieving response from the node
		while True:
			try:
				resp = req.post(self.url,json = custom_payload,headers = headers)
				break
			except Exception as e:
				print('request failed')
				print(str(e))
				time.sleep(5)
		data = json.loads(resp.content.decode())
		#print(data)
		if data['error']:
			print('bitcoin node error')
			print(data['error'])
			if message:
				return [False,data['error']['message']]
			else:
				return False
		else:
			if message:
				return [data['result']]
			else:
				return data['result']



def get_handler(coin):
	if coin == 'BTC':
		return Bitcoin()
	else:
		return False
