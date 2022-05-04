import instaloader
import data.config

def instagram_downloader(url):
    raw_url = url.split('/')
    shortcode = raw_url[4] 

    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'


    L = instaloader.Instaloader(filename_pattern=shortcode, save_metadata=False, 
                                download_video_thumbnails=False, quiet=True, 
                                user_agent=user_agent, dirname_pattern = 'downloads/instagram')
         
    try:
        L.load_session_from_file(username=data.config.username, filename=f'data/session-{data.config.username}')
    except:
        L.login(data.config.user, data.config.passwd)   

    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target='instagram')
    except:
        shortcode = 'Access denied: закрытый аккаунт.' 
    
    L.save_session_to_file(rf"data/session-{data.config.username}")
    return shortcode
