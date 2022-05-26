from tiktok_downloader import Snaptik


def download_video(url, video_id):    
    path = 'downloads/tiktok/'+ str(video_id) + '.mp4'
    
    try:
        Snaptik(url)[0].download(path)
    except: pass


