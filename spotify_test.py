import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_spotify_connection():
    try:
        # Create Spotify client
        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        # Try a simple search
        results = sp.search(q='genre:pop', type='track', limit=5)
        
        # Print out the track names
        print("Successful connection! Here are some tracks:")
        for track in results['tracks']['items']:
            print(f"Track: {track['name']} - Artist: {track['artists'][0]['name']}")
        
        return True
    except Exception as e:
        print(f"Connection failed. Error: {e}")
        return False

# Run the test
if __name__ == '__main__':
    test_spotify_connection()