# main.py

from flask import Blueprint, render_template, session, redirect, url_for
import requests

main_bp = Blueprint('main', __name__)

@main_bp.route('/saved_tracks')
def saved_tracks():
    token_info = session.get('token_info')
    if not token_info:
        return redirect(url_for('auth.login'))

    access_token = token_info['access_token']
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    saved_tracks_api_endpoint = 'https://api.spotify.com/v1/me/tracks'
    saved_tracks_response = requests.get(saved_tracks_api_endpoint, headers=headers)

    if saved_tracks_response.status_code == 200:
        saved_tracks_data = saved_tracks_response.json()
        if 'items' in saved_tracks_data and saved_tracks_data['items']:
            return render_template('saved_tracks.html', saved_tracks_data=saved_tracks_data['items'])
        else:
            return render_template('saved_tracks.html', saved_tracks_data=[])  # Render template with empty list
    else:
        return f"Error fetching saved tracks: {saved_tracks_response.status_code}"

@main_bp.route('/profile')
def profile():
    token_info = session.get('token_info')
    if not token_info:
        return redirect(url_for('auth.login'))

    access_token = token_info['access_token']
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    user_profile_api_endpoint = 'https://api.spotify.com/v1/me'
    profile_response = requests.get(user_profile_api_endpoint, headers=headers)

    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        return render_template('profile.html', profile_data=profile_data)
    else:
        return f"Error fetching profile: {profile_response.status_code}"


@main_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['query']
        token_info = session.get('token_info')
        if not token_info:
            return redirect(url_for('auth.login'))

        access_token = token_info['access_token']
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        search_api_endpoint = f'https://api.spotify.com/v1/search?q={search_query}&type=track'
        search_response = requests.get(search_api_endpoint, headers=headers)

        if search_response.status_code == 200:
            search_data = search_response.json()
            return render_template('search.html', search_data=search_data)
        else:
            return f"Error searching tracks: {search_response.status_code}"

    return render_template('search.html')
