#!D:\Python34\python.exe
# -*- coding: utf-8 -*-

'same APP 黑子'

__author__ = 'litter_zhang'

import time
import requests
import multiprocessing	
from threadpool import ThreadPool, makeRequests

headers = {
	'X-same-Client-Version': '426', 'X-Same-Request-ID': 'd6cd644f-5457478c-947d-28216f45350a',
	'Machine': 'android|301|android5.1.1|MX4 Pro|865863024824281|1536|2560', 'X-same-Device-UUID': '865863024824281', 
	'User-Agent': 'same/426', 'Connection': 'keep-alive', 'Advertising-UUID': '865863024824281', 
	'Authorization': 'Token 1471502420-p5klM6M6Q1M8qfck-4575261', 
	'Extrainfo': 'offical', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
	'Accept-Encoding': 'gzip'
	}

rs_ms = {}
time_ms = 1471503600

#向same发送get请求
def do_same_get(url):
	r = requests.get(url, headers=headers)
	return r

#向same发送post请求
def do_same_post(url, data):
	r = requests.post(url, data=data, headers=headers)
	return r

#统计秒杀请求结果
def same_ms_callback(req, code):
	rs_ms[str(code)] = rs_ms.get(str(code), 0) + 1

#秒杀请求
def same_ms_req(url, data):
	time_n = time.time()
	if time_ms-time_n>1:
		print('秒杀开始还有：%s分%s秒\n' % (int(time_ms-time_n)//60, int(time_ms-time_n)%60))
		print('休眠: 0.5秒\n')
		time.sleep(1)
		return same_ms_req(url, data)
	else:
		r = do_same_post(url, data)
		r.encoding = 'utf-8'
		print(r.text)
		return r.json().get('code', 0)

	# r = do_same_post(url, data)
	# r.encoding = 'utf-8'

	# return r.json().get('code', 0)

#秒杀
def same_ms(product_id):
	data = {'product_id': product_id, 'address_id': '72858'}
	url = 'http://payment.ohsame.com/order_create'
	
	time_s = time.time()
	pool = ThreadPool(20)
	reqs = makeRequests(same_ms_req, [((url, data), {}) for i in range(200)], same_ms_callback)
	[pool.putRequest(req) for req in reqs]
	pool.wait()
	time_e = time.time()

	print('秒杀商品：%s\n' % str(product_id))
	print('秒杀结果：%s\n' % rs_ms)
	print('秒杀耗时：%s\n' % (time_e-time_s))

#获取秒杀商品列表
def same_ms_products(list_ch=[0, ]):
	url = 'http://v2.same.com/channel/1176813/senses'
	r = do_same_get(url)
	r.encoding = 'utf-8'

	products = [it['media']['product'] for it in r.json()['data']['results']]
	products = list(filter(lambda x: x['count_remaining']!='0', products))
	products_id = [it['id'] for it in products]

	r_ids = list()
	for l in list_ch:
		r_ids.append(products_id[l])
	return r_ids

if __name__=='__main__':
	#same_ms(2244)
	products_id = same_ms_products(list_ch=[0, 1, 2, 3])
	#products_id = [2361, ]
	print(products_id)
	for product_id in products_id:
		p = multiprocessing.Process(target=same_ms, args=(product_id, ))
		p.start()
	
