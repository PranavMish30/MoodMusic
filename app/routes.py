from flask import Blueprint, render_template, request, jsonify
from app.mood_analyzer import MoodAnalyzer
from app.spotify_handler import SpotifyHandler
import traceback
import logging
import json

main = Blueprint('main', __name__)
mood_analyzer = MoodAnalyzer()
spotify_handler = SpotifyHandler()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/analyze', methods=['POST'])
def analyze():
    text = request.form.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        # Analyze mood
        mood_data = mood_analyzer.analyze_mood(text)
        logger.debug(f"Mood data type: {type(mood_data)}")
        logger.debug(f"Mood data: {mood_data}")
        
        # Ensure mood_data is JSON serializable
        if not isinstance(mood_data, dict):
            try:
                mood_data = json.loads(mood_data)
            except:
                mood_data = {
                    "primary_mood": "neutral",
                    "energy_level": 5,
                    "genre_suggestions": ["pop", "rock", "electronic"]
                }
        
        # Generate playlist
        playlist = spotify_handler.create_playlist(mood_data)
        logger.debug(f"Playlist generated: {playlist}")
        
        return jsonify({
            'mood_data': mood_data,
            'playlist': playlist
        })
    except Exception as e:
        logger.error(f"Error in analyze route: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500