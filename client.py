#!D:\Python34\python.exe
# -*- coding: utf-8 -*-

'same APP 黑子'

__author__ = 'litter_zhang'

import requests
import json
import functools
import time
from threadpool import ThreadPool, makeRequests

from auth.i_am_same import ImSameClient, LoginSameClient
from setting import LOGIN_URL, LOGIN_DATA, SENSES_URL

rs_ms = {}

def check_login(func):
	@functools.wraps(func)
	def wrapper(self, *args, **kwargs):
		if self._user:
			return func(self, *args, **kwargs)
		else:
			raise '没有登录 %s' % func.__name__
	return wrapper

def check_unlogin(func):
	@functools.wraps(func)
	def wrapper(self, *args, **kwargs):
		if not self._user:
			return func(self, *args, **kwargs)
		else:
			raise '已经登录了 %s' % func.__name__
	return wrapper

class SameClient:
	def __init__(self):
		self._session = requests.session()
		self._auth = ImSameClient()
		self._user = None

	@check_unlogin
	def login(self, mobile, password):
		LOGIN_DATA['mobile'] = '+86-' + str(mobile)
		LOGIN_DATA['password'] = password

		r = self._session.post(LOGIN_URL, data=LOGIN_DATA, auth=self._auth)
		r.encoding = 'utf-8'
		try:
			r_j = r.json()
			code = r_j['code']
			if code==0:
				user = r_j['data']['user']
				self._user = user
				self._auth = LoginSameClient(user['auth_token'])
			else:
				raise r_j['detail']
		except Exception as e:
			print('登录失败：%s' % str(e))

	@check_login
	def save_token(self, filename='user'):
		user_str = json.dumps(self._user, ensure_ascii=False)
		with open(filename, 'w', encoding='utf-8') as fw:
			fw.write(user_str)

	@check_unlogin
	def load_token(self, filename='user'):
		user_str = ''
		with open(filename, 'r', encoding='utf-8') as fr:
			for line in fr:
				user_str += line.strip()
		user = json.loads(user_str)
		self._user = user
		self._auth = LoginSameClient(user['auth_token'])

	@check_login
	#获取秒杀商品列表
	def same_ms_products(self):
		url = SENSES_URL
		r = self._session.get(url, auth=self._auth)
		r.encoding = 'utf-8'

		products = [it['media']['product'] for it in r.json()['data']['results']]
		products = list(filter(lambda x: x['count_remaining']!='0', products))
		products_id = [it['id'] for it in products]
		for product in products:
			print(product['title'])
			print(product['count_remaining'])
			print('-------------------------')
		return products_id

	#秒杀请求
	def same_ms_req(self, url, data):
		time_ms = 1462086000 
		time_n = time.time()
		if time_ms-time_n>1:
			print('秒杀开始还有：%s分%s秒\n' % (int(time_ms-time_n)//60, int(time_ms-time_n)%60))
			print('休眠: 0.5秒\n')
			time.sleep(0.5)
			return self.same_ms_req(url, data)
		else:
			r = self._session.post(url, data=data, auth=self._auth)
			r.encoding = 'utf-8'
			# print(r.text)
			return r.json().get('code', 0)

	#统计秒杀请求结果
	def same_ms_callback(self, req, code):
		global rs_ms
		rs_ms[str(code)] = rs_ms.get(str(code), 0) + 1

	def same_ms(self, product_id):
		data = {'product_id': product_id, 'address_id': '72858'}
		url = 'http://payment.ohsame.com/order_create'
		
		time_s = time.time()
		pool = ThreadPool(20)
		reqs = makeRequests(self.same_ms_req, [((url, data), {}) for i in range(200)], self.same_ms_callback)
		[pool.putRequest(req) for req in reqs]
		pool.wait()
		time_e = time.time()

		print('秒杀商品：%s\n' % str(product_id))
		print('秒杀结果：%s\n' % rs_ms)
		print('秒杀耗时：%s\n' % (time_e-time_s))


if __name__=='__main__':
	same = SameClient()
	same.load_token()
	# same.login('18810578897', '19940824zw')
	# same.save_token()
	products_id = same.same_ms_products()
	for product_id in products_id:
		same.same_ms(product_id)
		break
