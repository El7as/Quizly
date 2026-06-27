import re
from youtube_transcript_api._api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


class YouTubeTranscriptExtractor:
    """
    A helper class responsible for:
    1. Extracting a valid YouTube video ID from different URL formats.
    2. Fetching the transcript of a YouTube video using youtube-transcript-api.
    """

    def extract_video_id(self, url: str) -> str:
        """
        Extracts the YouTube video ID from various possible URL formats.

        Supported formats:
        - https://www.youtube.com/watch?v=VIDEOID
        - https://youtu.be/VIDEOID
        - https://www.youtube.com/embed/VIDEOID

        Args:
            url (str): The full YouTube URL provided by the user.

        Returns:
            str: The extracted 11‑character YouTube video ID.

        Raises:
            Exception: If no valid video ID can be found in the URL.
        """

        patterns = [
            r"v=([a-zA-Z0-9_-]{11})",
            r"youtu\.be/([a-zA-Z0-9_-]{11})",
            r"youtube\.com/embed/([a-zA-Z0-9_-]{11})"
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        raise Exception("Konnte keine gültige YouTube-Video-ID extrahieren.")

    def get_transcript(self, youtube_url: str) -> str:
        """
        Fetches the transcript of a YouTube video.

        Steps:
        1. Extract the video ID from the provided URL.
        2. Use youtube-transcript-api to fetch the transcript.
        3. Combine all transcript segments into a single string.

        Args:
            youtube_url (str): The full YouTube URL.

        Returns:
            str: The full transcript text.

        Raises:
            Exception: If transcripts are disabled, not found, or any other error occurs.
        """

        video_id = self.extract_video_id(youtube_url)

        try:
            api = YouTubeTranscriptApi()
            transcript_list = api.fetch(video_id, languages=['de', 'de-DE', 'en'])

            transcript_text = " ".join([item.text for item in transcript_list])
            return transcript_text

        except TranscriptsDisabled:
            raise Exception('This video has no subtitles (TranscriptsDisabled).')

        except NoTranscriptFound:
            raise Exception('No transcript was found for this video.')

        except Exception as e:
            raise Exception(f'Error while fetching transcript: {str(e)}')
