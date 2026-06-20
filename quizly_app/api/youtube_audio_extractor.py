import os
import yt_dlp
import uuid
import tempfile
import subprocess


class YouTubeAudioExtractor:
    def download_audio(self, youtube_url: str):
        tmp_filename = os.path.join(tempfile.gettempdir(), f'{uuid.uuid4().hex}.mp3')

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': tmp_filename,
            'quiet': True,
            'noplaylist': True,
            
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            'exec': 'node'
            }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
        except Exception as e:
            raise Exception(f'Fehler beim Herunterladen der Audio: {str(e)}')
        if not os.path.exists(tmp_filename):
            raise FileNotFoundError('Audio-Datei wurde nicht erstellt.')
        return tmp_filename


    def transcribe_audio_whisper_cli(self, audio_path: str):

        try:
            result = subprocess.run(['whisper', audio_path, '--model', 'base', '--language', 'de', '--fp16', 'False'],
                                    capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            raise Exception(f'Whisper CLI Fehler: {str(e)}')
        

    def generate_transcript_from_youtube_url(self, url: str):
        audio_path = self.download_audio(url)
        transcript = self.transcribe_audio_whisper_cli(audio_path)
        return transcript
    
