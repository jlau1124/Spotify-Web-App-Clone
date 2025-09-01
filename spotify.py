"""
spotify.py - Flask app for Spotify integration demo

Handles:
- OAuth2 login with Spotify
- Fetching user profile data
- Searching for songs
- Rendering template pages
"""

from flask import Flask, redirect, request, session, url_for, render_template, abort
import requests
from dotenv import load_dotenv
import os
import base64

# Load environment variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
app_secret_key = os.getenv("app.secret_key")

# Flask setup
app = Flask(__name__)
app.secret_key = app_secret_key

# --- Mock Data  --- #
songs_data = [
    {
        "id": 0,
        "name": "Song One",
        "image": "assets/img1.jpg",
        "file": "assets/song1.mp3",
        "desc": "Put a smile on your face with these happy tunes",
        "duration": "3:00"
    },
    {
        "id": 1,
        "name": "Song Two",
        "image": "assets/img2.jpg",
        "file": "assets/song2.mp3",
        "desc": "Put a smile on your face with these happy tunes",
        "duration": "2:20"
    },
    {
        "id": 2,
        "name": "Song Three",
        "image": "assets/img3.jpg",
        "file": "assets/song3.mp3",
        "desc": "Put a smile on your face with these happy tunes",
        "duration": "2:32"
    },
    {
        "id": 3,
        "name": "Song Four",
        "image": "assets/img4.jpg",
        "file": "assets/song1.mp3",
        "desc": "Put a smile on your face with these happy tunes",
        "duration": "2:50"
    },
    {
        "id": 4,
        "name": "Song Five",
        "image": "assets/img5.jpg",
        "file": "assets/song2.mp3",
        "desc": "Put a smile on your face with these happy tunes",
        "duration": "3:10"
    },
    {
        "id": 5,
        "name": "Song Six",
        "image": "assets/img14.jpg",
        "file": "assets/song3.mp3",
        "desc": "Put a smile on your face with these happy tunes",
        "duration": "2:45"
    },
    {
        "id": 6,
        "name": "Song Seven",
        "image": "assets/img7.jpg",
        "file": "assets/song1.mp3",
        "desc": "Put a smile on your face with these happy tunes",
        "duration": "2:18"
    },
    {
        "id": 7,
        "name": "Song Eight",
        "image": "assets/img12.jpg",
        "file": "assets/song2.mp3",
        "desc": "Put a smile on your face with these happy tunes",
        "duration": "2:35"
    }
]


albums_data = [
    {
        "id": 0,
        "name": "Top 50 Global",
        "image": "img8.jpg",
        "desc": "Your weekly update of the most played tracks",
        "bgColor": "#2a4365"
    },
    {
        "id": 1,
        "name": "Top 50 India",
        "image": "img9.jpg",
        "desc": "Your weekly update of the most played tracks",
        "bgColor": "#22543d"
    },
    {
        "id": 2,
        "name": "Trending India",
        "image": "img10.jpg",
        "desc": "Your weekly update of the most played tracks",
        "bgColor": "#742a2a"
    },
    {
        "id": 3,
        "name": "Trending Global",
        "image": "img16.jpg",
        "desc": "Your weekly update of the most played tracks",
        "bgColor": "#44337a"
    },
    {
        "id": 4,
        "name": "Mega Hits",
        "image": "img11.jpg",
        "desc": "Your weekly update of the most played tracks",
        "bgColor": "#234e52"
    },
    {
        "id": 5,
        "name": "Happy Favs",
        "image": "img15.jpg",
        "desc": "Your weekly update of the most played tracks",
        "bgColor": "#DF7A1B"
    },
    {
        "id": 6,
        "name": "Chill Mix",
        "image": "img17.jpg",
        "desc": "Chill Vibes Anyone Can Listen To",
        "bgColor": "#8E47AA"
    },
    {
        "id": 7,
        "name": "Happy Mix",
        "image": "img18.jpg",
        "desc": "Happy Music Picked Just For You",
        "bgColor": "#DBDF1B"
    }
]

# Global variable to store playlists
user_playlists = []  


# ----------------------- ROUTES -----------------------

@app.route("/")
def index():
    """Home page - shows albums and songs"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('home-content.html', 
                             albums=albums_data, 
                             songs=songs_data)
    else:
        return render_template("index.html", song=songs_data[0] if songs_data else None, songs=songs_data, albums=albums_data, albums_data=albums_data, songs_data=songs_data)


@app.route('/album/<int:album_id>/content')
def album_content(album_id):
    """Album detail page - shows songs inside an album"""
    album = next((a for a in albums_data if a['id'] == album_id), None)
    if not album:
        abort(404)
    songs = songs_data
    if not songs:
        abort(404)
    return render_template('album_content.html', album=album, songs=songs, album_name=album['name'])

@app.route("/login")
def login():
    """Redirect user to Spotify login page"""
    auth_url = (
        "https://accounts.spotify.com/authorize" 
        "?response_type=code"
        f"&client_id={client_id}" 
        f"&redirect_uri={redirect_uri}" 
        "&scope=user-read-private%20user-read-email" 
    )
    return redirect(auth_url) 


@app.route("/login_page")
def login_page():
    """Custom login page"""
    return render_template("login.html")


@app.route("/callback")
def callback():
    """Spotify OAuth callback - exchange code for access token"""
    code = request.args.get("code")
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code", 
        "code": code, 
        "redirect_uri": redirect_uri,
        "client_id": client_id, 
        "client_secret": client_secret 
    }
    response = requests.post(token_url, data=payload)
    token = response.json()
    session["access_token"] = token.get("access_token")
    return redirect(url_for("profile"))

@app.route("/profile")
def profile():
    """Fetch and display user's Spotify profile"""
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("login"))
    
    headers = {"Authorization": f"Bearer {access_token}"}
    endpoint = "https://api.spotify.com/v1/me"
    response = requests.get(endpoint, headers=headers)
    profile_data = response.json()

    user_name = profile_data.get("display_name", "Unknown User") 
    email = profile_data.get("email", "") 
    profile_image = profile_data['images'][0]['url'] if profile_data['images'] else None
    followers = profile_data['followers']['total']
    product = profile_data.get("product", "")

    return render_template("profile.html",
                           user_name=user_name,
                           email=email,
                           profile_image=profile_image,
                           followers=followers,
                           product=product)
    
@app.route("/search", methods=["GET", "POST"])
@app.route("/page/search", methods=["GET", "POST"])  # Add this line
def search():
    """Search Spotify tracks by keyword"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.path == '/page/search':
        return handle_ajax_search()
    
    results = []
    if request.method == "POST":
        search_term = request.form['search_term']
        auth_string = f"{client_id}:{client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
        token_url = "https://accounts.spotify.com/api/token"
        token_headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        token_data = {"grant_type": "client_credentials"}
        token_response = requests.post(token_url, headers=token_headers, data=token_data)
        access_token = token_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        endpoint = f"https://api.spotify.com/v1/search?q={search_term}&type=track&limit=5"
        response = requests.get(endpoint, headers=headers)
        search_data = response.json()
        tracks = search_data.get('tracks', {}).get('items', [])

        for track in tracks:
            track_name = track.get('name', 'Unknown Track')
            artist_name = track.get('artists', [{}])[0].get('name', 'Unknown Artist')
            album_name = track.get('album', {}).get('name', 'Unknown Album')
            spotify_link = track.get('external_urls', {}).get('spotify', '#')
            preview_url = track.get('preview_url')
            results.append({   # ← fixed here
                "track_name": track_name,
                "artist_name": artist_name,
                "album_name": album_name,
                "spotify_link": spotify_link,
                "preview_url": preview_url
            })
    return render_template("search.html", results=results) 

def handle_ajax_search():
    """Handle AJAX search requests returning partial HTML"""
    results = []
    if request.method == "POST":
        search_term = request.form['search_term']
        
        auth_string = f"{client_id}:{client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
        
        token_url = "https://accounts.spotify.com/api/token"
        token_headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        token_data = {"grant_type": "client_credentials"}
        token_response = requests.post(token_url, headers=token_headers, data=token_data)
        access_token = token_response.json().get("access_token")
        
        headers = {"Authorization": f"Bearer {access_token}"}
        endpoint = f"https://api.spotify.com/v1/search?q={search_term}&type=track&limit=5"
        response = requests.get(endpoint, headers=headers)
        search_data = response.json()
        tracks = search_data.get('tracks', {}).get('items', [])
        
        for track in tracks:
            track_name = track.get('name', 'Unknown Track')
            artist_name = track.get('artists', [{}])[0].get('name', 'Unknown Artist')
            album_name = track.get('album', {}).get('name', 'Unknown Album')
            spotify_link = track.get('external_urls', {}).get('spotify', '#')
            preview_url = track.get('preview_url')
            
            results.append({
                "track_name": track_name,
                "artist_name": artist_name,
                "album_name": album_name,
                "spotify_link": spotify_link,
                "preview_url": preview_url
            })
    
    return render_template("search-partial.html", results=results)


@app.route('/page/<page_name>')
def load_page(page_name):
    """Generic page loader (home, search, etc.)"""
    if page_name == 'home':
        return render_template('home-content.html', albums=albums_data, songs=songs_data)
    elif page_name == 'search':
        return render_template('search.html')  
    else:
        return render_template('home-content.html', albums=albums_data, songs=songs_data)


@app.route('/playlist/<int:playlist_id>')
def playlist_view(playlist_id):
    """Render a saved playlist by ID"""
    playlist = next((p for p in user_playlists if p['id'] == playlist_id), None)
    if not playlist:
        return "Playlist not found", 404
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('playlist-view.html', playlist=playlist)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
