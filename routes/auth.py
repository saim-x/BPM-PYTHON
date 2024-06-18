from flask import Blueprint, redirect, request, session, url_for
import requests
import config


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    return '<a href="/login">Login with Spotify</a>'


@auth_bp.route("/login")
def login():
    auth_url = (
        "https://accounts.spotify.com/authorize"
        "?response_type=code"
        "&client_id=" + config.CLIENT_ID + "&scope=user-library-read"
        "&redirect_uri=" + config.REDIRECT_URI
    )
    return redirect(auth_url)


@auth_bp.route("/callback")
def callback():
    error = request.args.get("error")
    if error:
        return f"Error: {error}"

    code = request.args.get("code")

    # Exchange authorization code for access token
    token_url = "https://accounts.spotify.com/api/token"
    token_params = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.REDIRECT_URI,
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
    }
    token_response = requests.post(token_url, data=token_params)
    token_data = token_response.json()

    # Store token data in session
    session["token_info"] = token_data
    print(session["token_info"])  # Check what data is stored
    # Redirect to a new route or page after successful authentication
    return redirect(url_for("main.profile"))  # Replace 'main.profile' with your route


@auth_bp.route("/logout")
def logout():
    session.clear()
    return "Logged out successfully"
