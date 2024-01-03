from flask import Blueprint, redirect, url_for, session, request
from google_auth_oauthlib.flow import Flow
import os

# Environment variables for OAuth credentials
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login')
def login():
    # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI],
                "scopes": ["https://www.googleapis.com/auth/photoslibrary"]
            }
        },
        scopes=["https://www.googleapis.com/auth/photoslibrary"],
        redirect_uri=REDIRECT_URI)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent')

    session['state'] = state

    return redirect(authorization_url)

@bp.route('/callback')
def callback():
    state = session['state']

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI],
                "scopes": ["https://www.googleapis.com/auth/photoslibrary"]
            }
        },
        scopes=["https://www.googleapis.com/auth/photoslibrary"],
        state=state,
        redirect_uri=REDIRECT_URI)

    flow.fetch_token(authorization_response=request.url)

    if not flow.credentials.is_valid():
        return 'Authentication failed', 401

    session['credentials'] = credentials_to_dict(flow.credentials)

    return redirect(url_for('main.index'))

@bp.route('/logout')
def logout():
    if 'credentials' in session:
        del session['credentials']

    return redirect(url_for('main.index'))

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scopes': credentials.scopes
    }
