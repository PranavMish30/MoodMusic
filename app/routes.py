from flask import Blueprint, render_template, request, jsonify
from app.mood_analyzer import MoodAnalyzer
from app.spotify_handler import SpotifyHandler
import traceback
import logging
import json

main = Blueprint('main', __name__)
mood_analyzer = MoodAnalyzer()
spotify_handler = SpotifyHandler()

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/analyze', methods=['POST'])
def analyze():
    text = request.form.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    try :
        mood_data = mood_analyzer.analyze_mood(text)
        with open("json.txt", "w") as file:
            file.write(mood_data)   
        # Generate playlist
        playlist,processed_mood_data = spotify_handler.create_playlist(mood_data)
        # logger.debug(f"Playlist generated: {playlist}")
        
        return jsonify({
            'mood_data': processed_mood_data,
            'playlist': playlist
        })
    except Exception as e:

        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500