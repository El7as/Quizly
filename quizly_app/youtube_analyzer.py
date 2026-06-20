from google import genai

def generate_quiz_from_video(transcript: str):
    client = genai.Client(api_key='TEST')

    prompt = f'Erstelle 10 Quizfragen mit je 4 Antwortoptionen basierend auf folgendem Video-Text: n\{transcript}'

    response = client.models.generate_content(model='gemini-1.5-flash', contents=prompt)

    return response.text
