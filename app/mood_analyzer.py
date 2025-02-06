import google.generativeai as genai
import os

class MoodAnalyzer:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_mood(self, text):
        prompt = f'''Analyze the mood in this text: "{text}"
        Return a JSON object with these fields:
        1. primary_mood: The main emotion (e.g., "happy", "sad", "energetic")
        2. energy_level: A number from 1-10
        3. genre_suggestions: List of 3 music genres that match this mood
        Keep it concise and focus on musical relevance.
        DON'T ADD ANY STATEMENTS IN THE RESPONSE THAT WILL MAKE PARSING THE JSON DIFFICULT'''
        
        response = self.model.generate_content(prompt)
        wrapped_text =  f"'''{response.text}'''"
        return wrapped_text