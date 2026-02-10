import assemblyai as aai
import yt_dlp

def transcribe_youtube_video(video_url: str, api_key: str) -> str:
    """
    Transcribe a YouTube video given its URL.

    Args:
        video_url: The YouTube video URL to transcribe
        api_key: AssemblyAI API key

    Returns:
        The transcript text
    """
    # Configure yt-dlp options for audio extraction
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    # Download and extract audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        # Get video ID from info dict
        info = ydl.extract_info(video_url, download=False)
        video_id = info['id']

    # Configure AssemblyAI
    aai.settings.api_key = api_key

    # Transcribe the downloaded audio file
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(f"{video_id}.m4a")

    return transcript.text

transcript_text = transcribe_youtube_video("https://www.youtube.com/watch?v=wtolixa9XTg", "YOUR-API-KEY")
print(transcript_text)
