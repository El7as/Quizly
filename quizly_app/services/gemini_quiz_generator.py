import os
import json
from google import genai



class GeminiQuizGenerator:
    """
    Generates quiz questions from a transcript using the Gemini API.
    """


    def __init__(self):
        """
        Initialize the Gemini client using the API key from environment variables.
        """

        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError('GEMINI_API_KEY wurde nicht gesetzt oder konnte nicht erkannt werden')
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-3.5-flash'

    def generate_quiz(self, transcript: str):
        """
        Generate a 10‑question quiz from a transcript.
        """
        
        prompt = f'''
        Erstelle ein Quiz mit genau 10 Fragen basierend auf folgendem Transkript eines YouTube-Videos.
        Das Video behandelt ein allgemeines Thema, nicht technische Fehlermeldungen. Ignoriere alle technischen Begriffe oder Log-Ausgaben.
        Konzentriere dich auf das inhaltliche Thema des Videos.
        ---
        {transcript}
        ---

        Format: [
        {{
            "question": "Frage...",
            "options": ["A", "B", "C", "D"],
            "answer": "A"
        }},
        ]

        Regeln:
        - Schreibe alle Fragen und Antworten auf Deutsch.
        - Jede Frage hat genau 4 Antwortmöglichkeiten.
        - Die Antwort muss exakt einer der Optionen entsprechen.
        - Keine zusätzlichen Kommentare oder Erklärungen.

        '''

        try:
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            text = response.text.strip()

        except Exception as e:
            raise Exception(f'Fehler bei der Gemini API: {str(e)}')
        
        try:
            quiz_data = json.loads(text)
        except json.JSONDecodeError:
            raise ValueError('Gemini Antwort konnte nicht als JSON geparst werden. Antwort war :\n' + text)
        
        return quiz_data
    