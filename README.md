# Quizly Backend

Quizly is a Django‑based backend application that automatically generates quizzes from YouTube videos.  
Users authenticate, submit a YouTube URL, and the system extracts the transcript, processes it with Google Gemini, and returns a fully structured quiz with questions, options, and correct answers.

---

## Features

### User Authentication
- Registration & login using Django REST Framework  
- JWT authentication stored in HTTP‑only cookies  

### YouTube Transcript Extraction
- Audio download via `yt-dlp`  
- Local transcription using Whisper  

### AI‑Generated Quizzes
- Powered by Google Gemini (Flash 3.5)  
- 10 questions per quiz  
- 4 answer options per question  
- Correct answer automatically assigned  

### Quiz Management
- Create quizzes from YouTube URLs  
- List all quizzes belonging to the authenticated user  
- Retrieve, update, and delete quizzes  
- Nested serialization (Quiz → Questions → Options)  

### Clean, modular architecture
- `auth_app` → authentication  
- `quizly_app` → quiz logic  
- `utils` → AI and transcript processing  

---

## Django Settings 

The project uses `python-dotenv` to load environment variables.

### Example from `settings.py`

```python
from dotenv import load_dotenv
import os

load_dotenv()
```


##  Environment Variables
```
SECRET_KEY = your_django_secret_key
GEMINI_API_KEY = your_gemini_api_key
DATABASE_URL=sqlite:///db.sqlite3
DEBUG = True
ALLOWED_HOSTS = 127.0.0.1,localhost
```


## Installation

```
git clone <your-repo-url>
```

```
cd project
```

```
python -m venv env
```

```
source env/bin/activate  # Windows: env\Scripts\activate
```

```
pip install -r requirements.txt
```

```
python manage.py makemigrations
```

```
python manage.py migrate
```

```
python manage.py runserver
```
