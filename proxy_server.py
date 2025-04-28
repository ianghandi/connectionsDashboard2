import os
import secrets
import hashlib
import base64
import requests
import jwt
from flask import Flask, request, jsonify, redirect, session, url_for, render_template, send_from_directory
from flask_session import Session
from datetime import timedelta
from config import ENVIRONMENTS, OAUTH_CONFIG, ALLOWED_GROUPS

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
Session(app)

def generate_pkce_pair():
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login')
def login():
    code_verifier, code_challenge = generate_pkce_pair()
    session['code_verifier'] = code_verifier

    auth_url = (
        f"{OAUTH_CONFIG['authorization_endpoint']}?"
        f"response_type=code&"
        f"client_id={OAUTH_CONFIG['client_id']}&"
        f"redirect_uri={OAUTH_CONFIG['redirect_uri']}&"
        f"scope={'%20'.join(OAUTH_CONFIG['scopes'])}&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method=S256"
    )
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Missing authorization code", 400

    token_response = requests.post(
        OAUTH_CONFIG['token_endpoint'],
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': OAUTH_CONFIG['redirect_uri'],
            'client_id': OAUTH_CONFIG['client_id'],
            'code_verifier': session.get('code_verifier')
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        verify=False
    )

    if token_response.status_code != 200:
        return "Failed to fetch tokens", 400

    tokens = token_response.json()
    id_token = tokens.get('id_token')

    if not id_token:
        return "ID Token missing", 400

    decoded = jwt.decode(id_token, options={"verify_signature": False})
    groups = decoded.get('attire_memberof', [])

    if not any(group in ALLOWED_GROUPS for group in groups):
        return render_template('unauthorized.html')

    session['id_token'] = id_token
    session.permanent = True

    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/')
@login_required
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
@login_required
def send_static(path):
    return send_from_directory('static', path)

@app.route('/api/get-connections', methods=['GET'])
@login_required
def get_connections():
    environment = request.args.get('environment')
    connection_type = request.args.get('type')

    if not environment or not connection_type:
        return jsonify({"error": "Missing environment or type parameter."}), 400

    env_config = ENVIRONMENTS.get(environment)
    if not env_config:
        return jsonify({"error": "Unknown environment."}), 400

    base_url = env_config['url']
    username = env_config['username']
    password = env_config['password']

    # Default headers
    headers_pf = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-XSRF-Header": "PingFederate"
    }
    headers_pa = {
        "Content-Type": "application/json"
    }

    if connection_type.lower() == "saml":
        endpoint = "/pf-admin-api/v1/idp/spConnections"
        full_url = base_url + endpoint
        try:
            resp = requests.get(full_url, headers=headers_pf, auth=(username, password), verify=False)
            resp.raise_for_status()
            return jsonify(resp.json())
        except requests.RequestException as e:
            return jsonify({"error": str(e)}), 500

    elif connection_type.lower() == "oauth":
        endpoint = "/pf-admin-api/v1/oauth/clients"
        full_url = base_url + endpoint
        try:
            resp = requests.get(full_url, headers=headers_pf, auth=(username, password), verify=False)
            resp.raise_for_status()
            return jsonify(resp.json())
        except requests.RequestException as e:
            return jsonify({"error": str(e)}), 500

    elif connection_type.lower() == "pingaccess":
        applications_url = base_url + "/pa-admin-api/v3/applications"
        try:
            resp = requests.get(applications_url, headers=headers_pa, auth=(username, password), verify=False)
            resp.raise_for_status()
            apps = resp.json().get("items", [])

            site_cache = {}
            vh_cache = {}

            results = []
            for app in apps:
                app_name = app.get("name", "")
                site_id = app.get("siteId")
                virtual_host_ids = app.get("virtualHostIds", [])
                active = app.get("enabled", False)

                # Fetch first target from site (with caching)
                target = ""
                if site_id is not None:
                    if site_id in site_cache:
                        targets = site_cache[site_id]
                    else:
                        site_resp = requests.get(f"{base_url}/pa-admin-api/v3/sites/{site_id}", headers=headers_pa, auth=(username, password), verify=False)
                        if site_resp.ok:
                            targets = site_resp.json().get("targets", [])
                            site_cache[site_id] = targets
                        else:
                            targets = []
                    if targets:
                        target = targets[0]

                # Fetch first virtual host (with caching)
                host = ""
                if virtual_host_ids:
                    vh_id = virtual_host_ids[0]
                    if vh_id in vh_cache:
                        host = vh_cache[vh_id]
                    else:
                        vh_resp = requests.get(f"{base_url}/pa-admin-api/v3/virtualhosts/{vh_id}", headers=headers_pa, auth=(username, password), verify=False)
                        if vh_resp.ok:
                            host = vh_resp.json().get("host", "")
                            vh_cache[vh_id] = host

                results.append({
                    "appName": app_name,
                    "target": target,
                    "host": host,
                    "active": active
                })

            return jsonify(results)

        except requests.RequestException as e:
            return jsonify({"error": str(e)}), 500

    else:
        return jsonify({"error": "Unknown connection type."}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
