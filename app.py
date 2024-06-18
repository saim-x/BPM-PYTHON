# from flask import Flask, request, redirect, session, url_for
# import requests
# import base64
# import json
# import config

# app = Flask(__name__)
# app.secret_key = 'randomsecretkey'  # Replace with a random secret key

# @app.route('/')
# def index():
#     return '<a href="/login">Login with Spotify</a>'

# @app.route('/login')
# def login():
#     auth_url = (
#         'https://accounts.spotify.com/authorize'
#         '?response_type=code'
#         '&client_id=' + config.CLIENT_ID +
#         '&scope=user-library-read'
#         '&redirect_uri=' + config.REDIRECT_URI
#     )
#     return redirect(auth_url)

# @app.route('/callback')
# def callback():
#     code = request.args.get('code')
#     auth_token_url = 'https://accounts.spotify.com/api/token'
#     auth_token_data = {
#         'grant_type': 'authorization_code',
#         'code': code,
#         'redirect_uri': config.REDIRECT_URI,
#         'client_id': config.CLIENT_ID,
#         'client_secret': config.CLIENT_SECRET,
#     }
#     auth_token_headers = {
#         'Content-Type': 'application/x-www-form-urlencoded'
#     }
#     auth_response = requests.post(auth_token_url, data=auth_token_data, headers=auth_token_headers)
#     auth_response_data = auth_response.json()
#     session['token_info'] = auth_response_data
#     return redirect(url_for('profile'))

# def get_token():
#     token_info = session.get('token_info', None)
#     if not token_info:
#         raise "Exception"
#     return token_info['access_token']

# @app.route('/profile')
# def profile():
#     token = get_token()
#     headers = {
#         'Authorization': 'Bearer ' + token
#     }
#     user_profile_api_endpoint = 'https://api.spotify.com/v1/me'
#     profile_response = requests.get(user_profile_api_endpoint, headers=headers)
#     profile_data = profile_response.json()
#     return f'<h1>Welcome, {profile_data["display_name"]}</h1>'

# if __name__ == '__main__':
#     app.run(debug=True)
# app.py

from flask import Flask
from routes import auth, main

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Register blueprints
app.register_blueprint(auth.auth_bp)
app.register_blueprint(main.main_bp)

if __name__ == '__main__':
    app.run(debug=True)
