#!D:\Python34\python.exe
# -*- coding: utf-8 -*-

'same APP 黑子'

__author__ = 'litter_zhang'

#same客户端版本
X_SAME_CLIENT_VERSION = 428

DEVICE_UUID = '865863024824281'

MACHINE = 'android|301|android5.1.1|MX4 Pro|865863024824281|1536|2560'

API_ROOT = 'http://v2.same.com'

LOGIN_URL = API_ROOT + '/user/login'

LOGIN_DATA = {
	'device': DEVICE_UUID,
	'mobile': '',
	'password': '',
	'push_token': 'mi-uid' 
} 

SENSES_URL = 'http://v2.same.com/channel/1176813/senses'