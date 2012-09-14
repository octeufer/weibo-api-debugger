import sys
from bottle import request
from inspect import isfunction

from session_util import *
from weibo_api_const import *
from weibo import APIClient, APIError
from util import *

def receive_weibo_api(method):
	client = APIClient(app_key=weibo_appid, app_secret=weibo_app_secret, 
		redirect_uri=redirect_url_weibo)
	client.set_access_token(get_access_token(), get_expires_in())
	api_func = construct_weibo_api_url(method)
	if not api_func:
		return {'status': 'api_not_found'}
	print api_func
	try:
		json_rst = eval(api_func)
	except APIError as e:
		return {'status': str(e)}
	except:
		return {'status': str(sys.exc_info())}
	return {'status': 'success', 'rst': json_rst}

def receive_weibo_api_manual(method):
	client = APIClient(app_key=weibo_appid, app_secret=weibo_app_secret, 
		redirect_uri=redirect_url_weibo)
	client.set_access_token(get_access_token(), get_expires_in())
	api_func = construct_weibo_api_url(method)
	if not api_func:
		return {'status': 'api_not_found'}
	print api_func
	try:
		json_rst = eval(api_func)
	except APIError as e:
		return {'status': str(e)}
	except:
		return {'status': str(sys.exc_info())}
	return {'status': 'success', 'rst': json_rst}

def construct_weibo_api_url(method):
	params = ''
	for key in request.GET:
		if key != 'method':
			value = request.GET.get(key)
			if value != '':
				if isWeiboApiStringParameter(value):
					params += '%s=\'%s\',' %(key, value)
				else:
					params += '%s=%s,' %(key, value)
	api_func = ('client.get.%s' % (method.replace('/','__'))) + '(' + params + ')'
	return api_func
