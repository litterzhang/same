#!D:\Python34\python.exe
# -*- coding: utf-8 -*-

'same APP 黑子'

__author__ = 'litter_zhang'

from requests.auth import AuthBase

from setting import X_SAME_CLIENT_VERSION, DEVICE_UUID, MACHINE

class ImSameClient(AuthBase):
	def __init__(self, app_version=None, device_id=None, machine=None):
		self._app_version = app_version or X_SAME_CLIENT_VERSION
		self._device_id = device_id or DEVICE_UUID
		self._machine = machine or MACHINE

	def __call__(self, r):
		"""
		..  note::
			requests 会自动调用这个方法

		此函数在 PreparedRequest 的 HTTP header
		里加上了模拟 Android 客户端所需要的附加属性

		..  seealso::
			自动添加的属性参见 :meth:`__init__`
		"""
		r.headers['X-same-Client-Version'] = self._app_version
		r.headers['X-Same-Request-ID'] = 'd6cd644f-5457478c-947d-28216f45350a'
		r.headers['Machine'] = self._machine
		r.headers['X-same-Device-UUID'] = self._device_id
		r.headers['User-Agent'] = 'same/' + str(self._app_version)
		r.headers['Advertising-UUID'] = self._device_id
		r.headers['Extrainfo'] = 'offical'
		r.headers['Connection'] = 'keep-alive'
		r.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
		r.headers['Accept-Encoding'] = 'gzip'
		return r

class LoginSameClient(ImSameClient):
	def __init__(self, auth_token, app_version=None, device_id=None, machine=None):
		super(LoginSameClient, self).__init__(app_version, device_id, machine)
		self._auth_token = auth_token

	def __call__(self, r):
		"""
		..  note::
			requests 会自动调用这个方法

		此函数在 PreparedRequest 的 HTTP header
		里加上了 HTTP Authorization 头，值为 CLIENT_ID。

		由于是 :class:`.ImZhihuAndroidClient` 的子类，也会自动加上描述 APP 信息的头。

		..  seealso::
			:meth:`.ImZhihuAndroidClient.__call__`
		"""
		r = super(LoginSameClient, self).__call__(r)
		r.headers['Authorization'] = 'Token {0}'.format(self._auth_token)
		return r
