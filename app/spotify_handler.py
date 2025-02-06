import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import json
import logging

class SpotifyHandler:
    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
        )
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    def create_playlist(self, mood_data):
        # Robust handling of mood_data
        self.logger.debug(f"Raw mood_data type: {type(mood_data)}")
        self.logger.debug(f"Raw mood_data: {mood_data}")
        
        # If mood_data is already a dictionary, use it directly
        if isinstance(mood_data, dict):
            processed_mood_data = mood_data
        else:
            try:
                # Try to parse if it's a string
                processed_mood_data = json.loads(mood_data) if mood_data else {}
            except (json.JSONDecodeError, TypeError):
                # Fallback to default if parsing fails
                self.logger.error("Failed to parse mood_data")
                processed_mood_data = {
                    "primary_mood": "neutral",
                    "energy_level": 5,
                    "genre_suggestions": ["pop", "rock", "electronic"]
                }
        
        # Log processed mood data
        self.logger.debug(f"Processed mood_data: {processed_mood_data}")
        
        tracks = []
        genres = processed_mood_data.get('genre_suggestions', ['pop'])
        self.logger.debug(f"Searching for genres: {genres}")
        
        for genre in genres:
            try:
                # More flexible search query
                search_query = f"genre:{genre.lower()}"
                self.logger.debug(f"Searching with query: {search_query}")
                
                results = self.sp.search(
                    q=search_query, 
                    type='track', 
                    limit=5
                )
                
                self.logger.debug(f"Search results for {genre}: {len(results['tracks']['items'])} tracks")
                
                for track in results['tracks']['items']:
                    track_info = {
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'url': track['external_urls']['spotify'],
                        'preview_url': track.get('preview_url')
                    }
                    tracks.append(track_info)
                    self.logger.debug(f"Added track: {track_info['name']} by {track_info['artist']}")
            
            except Exception as e:
                self.logger.error(f"Error searching for {genre}: {e}")
        
        self.logger.debug(f"Total tracks found: {len(tracks)}")
        return tracks