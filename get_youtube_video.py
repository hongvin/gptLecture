from yt_dlp import YoutubeDL
import json

def get_youtube_videos(youtube_link: str) -> None:
    """Download Youtube video and subtitle

    Args:
        youtube_link (str): Youtube link
    """

    ytdl_opt = {'writeautomaticsub':True,'subtitlesformat':'json','verbose': True,'writeinfojson': True,'outtmpl': 'video'}
    with YoutubeDL(ytdl_opt) as ydl:
        ydl.download(youtube_link)

def read_youtube_data(json_file: str) -> str:
    """Read Youtube Title

    Args:
        json_file (str): The JSON metadata filename
    
    Return:
        str: Video Title
    """

    video_metadata = json.load(open(json_file))
    video_title = video_metadata['title']
    return video_title

if __name__ == '__main__':
    get_youtube_videos('https://www.youtube.com/watch?v=u0T4iu_2PZA')
    print(read_youtube_data('video.info.json'))