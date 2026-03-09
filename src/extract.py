import os
import json
import logging
from datetime import datetime
from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SpotifyExtractor:
    """
    Kelas untuk mengambil data dari Spotify API.
    """

    def __init__(self):
        """Inisialisasi koneksi Spotify."""
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            raise ValueError("Missing Spotify credentials in .env file")

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope="user-read-recently-played",
            cache_path=".spotify_cache"
        ))
        logger.info("Spotify client initialized successfully")

    def fetch_recently_played(self, limit=50, after=None):
        """
        Mengambil recently played tracks.
        Args:
            limit (int): Jumlah track per halaman (max 50).
            after (int): Timestamp dalam milidetik untuk mengambil data setelah waktu tertentu.
        Returns:
            dict: Respons JSON dari API.
        """
        try:
            logger.info(f"Fetching recently played tracks (limit={limit}, after={after})")
            results = self.sp.current_user_recently_played(limit=limit, after=after)
            logger.info(f"Successfully fetched {len(results.get('items', []))} tracks")
            return results
        except Exception as e:
            logger.error(f"Error fetching recently played: {e}")
            raise

    def save_raw_data(self, data, prefix="recently_played"):
        """
        Menyimpan data mentah ke file JSON dalam folder data/raw/...
        """
        # Buat folder berdasarkan tanggal
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        timestamp = now.strftime("%Y%m%d_%H%M%S")

        # Path: data/raw/recently_played/year=2026/month=03/day=09/
        save_dir = Path("data") / "raw" / prefix / f"year={year}" / f"month={month}" / f"day={day}"
        save_dir.mkdir(parents=True, exist_ok=True)

        # Nama file: recently_played_20260309_153022.json
        filename = f"{prefix}_{timestamp}.json"
        filepath = save_dir / filename

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Raw data saved to {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to save raw data: {e}")
            raise

    def extract_and_save(self, limit=50):
        """
        Fungsi utama: mengambil data dan menyimpannya.
        """
        data = self.fetch_recently_played(limit=limit)
        filepath = self.save_raw_data(data)
        return filepath


# Jika dijalankan langsung sebagai script
if __name__ == "__main__":
    extractor = SpotifyExtractor()
    extractor.extract_and_save()