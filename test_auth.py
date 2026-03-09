import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-top-read",
    cache_path=".spotify_cache"
))

# Ambil top tracks periode medium_term (6 bulan)
results = sp.current_user_top_tracks(limit=5, time_range='medium_term')
print(f"Berhasil mengambil {len(results['items'])} top track:")
for track in results['items']:
    artists = ", ".join([a['name'] for a in track['artists']])
    print(f"- {track['name']} by {artists}")