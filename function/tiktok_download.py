from tiktok_downloader import tikmate


def download_video(url, video_id):    
    path = 'downloads/tiktok/'+ str(video_id) + '.mp4'
    tikmate().get_media(url)[0].download(path)


