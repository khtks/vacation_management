import datetime

import pytest
from google.auth.transport import requests
from google.oauth2 import id_token
from flask import Blueprint, redirect, url_for, request, session, render_template
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

google_api_bp = Blueprint("google_api", __name__)
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid']


def get_event():
    if 'credentials' not in session:
        return redirect('/authorize')

    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    service = build('calendar', 'v3', credentials=credentials)

    # 'bluewhale.kr_0gbuu26gl7vue837u7f07mn360@group.calendar.google.com'  <== AIMMO Google calednar id
    events_result = service.events().list(
        calendarId='primary', timeMin=datetime.datetime(2020, 1, 1).isoformat() + 'Z', showDeleted=True,
        timeMax=datetime.datetime(2020, 2, 28).isoformat() + 'Z', maxResults=2500, singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    session['credentials'] = credentials_to_dict(credentials)
    session['events'] = events

    return events


@google_api_bp.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('application/oauth_cred.json', scopes=SCOPES)
    flow.redirect_uri = url_for('google_api.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='online',
        include_granted_scopes='true')

    session['state'] = state

    return redirect(authorization_url)


@pytest.fixture(scope='module')
def test_credential():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('application/oauth_cred.json', scopes=SCOPES)
    flow.redirect_uri = url_for('google_api.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='online',
        include_granted_scopes='true')

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('application/oauth_cred.json', scopes=SCOPES,
                                                                   state=state)
    flow.redirect_uri = url_for('google_api.oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    return flow.credentials


@google_api_bp.route('/oauth2callback')
def oauth2callback():

    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('application/oauth_cred.json', scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('google_api.oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('google_api.user_auth'))


@google_api_bp.route('/revoke')
def revoke():
    if 'credentials' not in session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
                'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    revoke = requests.post('https://oauth2.googleapis.com/revoke',
                           params={'token': credentials.token},
                           headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return 'Credentials successfully revoked.' + print_index_table()
    else:
        return 'An error occurred.' + print_index_table()


@google_api_bp.route('/clear')
def clear_credentials():
    if 'credentials' in session:
        del session['credentials']

    return 'Credentials have been cleared.<br><br>' + print_index_table()


@google_api_bp.route('/authenticate-token')
def user_auth():
    cred = session['credentials']

    id_info = id_token.verify_oauth2_token(cred.get('id_token'), requests.Request(), cred.get('client_id'))

    if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')

    google_id = id_info.get('email')

    session['google_id'] = google_id

    return redirect(url_for('main'))


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes,
            'id_token': credentials.id_token}


def print_index_table():
    return ('<table>' +
            '<tr><td><a href="/service">Test an API request</a></td>' +
            '<td>Submit an API request and see a formatted JSON response. ' +
            '    Go through the authorization flow if there are no stored ' +
            '    credentials for the user.</td></tr>' +
            '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
            '<td>Go directly to the authorization flow. If there are stored ' +
            '    credentials, you still might not be prompted to reauthorize ' +
            '    the application.</td></tr>' +
            '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
            '<td>Revoke the access token associated with the current user ' +
            '    session. After revoking credentials, if you go to the test ' +
            '    page, you should see an <code>invalid_grant</code> error.' +
            '</td></tr>' +
            '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
            '<td>Clear the access token currently stored in the user session. ' +
            '    After clearing the token, if you <a href="/test">test the ' +
            '    API request</a> again, you should go back to the auth flow.' +
            '</td></tr></table>')