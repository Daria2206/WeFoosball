import os
import json
import requests
import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from . import auth
from .. import db
from ..models import User, Team


CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/userinfo.email']
API_SERVICE_NAME = 'plus'
API_VERSION = 'v1'


@auth.route('/servisobject')
def built_servis_object():
    if 'credentials' not in flask.session:
      return flask.redirect('register')
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])
    plus = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)
    person = plus.people().get(userId='me').execute()
    flask.session['credentials'] = credentials_to_dict(credentials)
    preserve_user_data(person)
    return flask.redirect(flask.url_for('main.teams'))


@auth.route('/authorize', methods = ['GET', 'POST']) 
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = flask.url_for('auth.gCallback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent',
        state='sample_pass_value', 
        include_granted_scopes='true')
    flask.session['state'] = state
    return flask.redirect(authorization_url)


@auth.route('/gCallback')
def gCallback():
    state = flask.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('auth.gCallback', _external=True)
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)
    return flask.redirect(flask.url_for('auth.built_servis_object'))


@auth.route('/logout') 
def logout():
    if 'credentials' not in flask.session:
      return flask.redirect('register')
    if 'credentials' in flask.session:
      del flask.session['credentials']
      del flask.session['user_info'] 
    return flask.render_template("logout.html")

# In real life user's access and tokens refreshement should take place in data store.
def credentials_to_dict(credentials): 
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def preserve_user_data(g_data):
    """Adds authenticated user to db if not already there and stores some usful 
    user data in flask session."""
    flask.session['user_info'] = {'emails':g_data['emails'][0]['value'],
                                  'name':g_data['displayName']}
    user = User.query.filter_by(email=g_data['emails'][0]['value']).first()
    if user is None:
        user = User(
            email=g_data['emails'][0]['value'], 
            name=g_data['displayName'])
        db.session.add(user)
        db.session.commit()

    
    
    