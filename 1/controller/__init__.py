import bottle
from bottle import route, debug, default_app
from bottle import response, request, redirect
from bottle import jinja2_view as view

app = default_app()
bottle.debug(True)

from util import deployed_on_sae
from weibo_api_const import *
from weibo_api_rpc import *
from session_util import *
from weibo_auth import *

@app.route('/')
@view('static/view/main.html')
def main_page():
	isLogged, username = session_login()
	if isLogged == True:
		return {'username' : username, 'g_api': g_api}
	return {'g_api': g_api}

@app.route('/api')
def get_api_json():
	response.content_type = 'application/json'
	if not is_logged_session():
		return {'status': 'not_login'}

	if deployed_on_sae:
		if request.GET.get('method'):
			method = request.GET.get('method')
			return receive_weibo_api(method)
		else:
			return {'status': 'api_not_found'}
	else:
		d = {};
		for i in range(1, 10): d[str(i)] = i
		return {'status': 'success', 'rst': {'uid':12345, 'x' : {'x':[{'x':1, 'y':2}, {'x':1, 'y':2}, {'x':1, 'y':2}]},'other': d}}
	return {'status': 'error'}


@app.route('/weibo')
def weibo():
	return handle_weibo_oauth_callback()

@app.route('/login_to_weibo')
def login_to_weibo():
	return redirect_to_weibo_oauth_url()

@app.route('/logout')
def logout():
	session_logout()
	return redirect('/')

from beaker.middleware import SessionMiddleware
session_opts = {
  'session.type': 'cookie',
  'session.expires': 3600,
  'session.validate_key': '1234',
}
app = SessionMiddleware( app, session_opts )
