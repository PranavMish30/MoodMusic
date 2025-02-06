import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import json
import re

class SpotifyHandler:
    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
        )
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def extract_json(self, text):
        """Extract JSON from text using regex."""
        match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        return json.loads(match.group(1))

    def create_playlist(self, mood_data):
        """Create a playlist based on mood data."""
        processed_mood_data = self.extract_json(mood_data)
        print(processed_mood_data)

        if not processed_mood_data:
            
            processed_mood_data = {
                "primary_mood": "neutral",
                "energy_level": 5,
                "genre_suggestions": ["pop", "rock", "electronic"]
            }
        print(processed_mood_data)
        tracks = []
        genres = processed_mood_data.get('genre_suggestions', ['pop'])
        print(genres)
        for genre in genres:
            try:
                search_query = f"genre:{genre.lower()}"
                results = self.sp.search(q=search_query, type='track', limit=5)

                for track in results['tracks']['items']:
                    track_info = {
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'url': track['external_urls']['spotify'],
                        'preview_url': track.get('preview_url')
                    }
                    tracks.append(track_info)

            except Exception as e:
                print(e)

        print(tracks)
        return tracks,processed_mood_data
