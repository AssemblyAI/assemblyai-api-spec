import yt_dlp

URLS = ['https://www.youtube.com/watch?v=wtolixa9XTg']

ydl_opts = {
    'format': 'm4a/bestaudio/best',  # The best audio version in m4a format
    'outtmpl': '%(id)s.%(ext)s',  # The output name should be the id followed by the extension
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }]
}


with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URLS)
