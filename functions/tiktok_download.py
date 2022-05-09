from tiktok_downloader import tikmate, Snaptik


def download_video(url, video_id):    
    path = 'downloads/tiktok/'+ str(video_id) + '.mp4'
    
    try: 
        Snaptik(url)[0].download(path)
    except:
        tikmate().get_media(url)[0].download(path) 
    

    



