from tiktok_downloader import tikmate
import requests
from bs4 import BeautifulSoup

def get_video_id(url): 
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')


    for item in soup.find_all('link'):    
        check_link = item.get('href').split('/')
        if check_link[2] == 'www.tiktok.com' and check_link[4] == 'video':
            video_id = check_link[5]
            break  
    return(video_id)


def download_video(url, video_id):    
    path = 'downloads/tiktok/'+ str(video_id) + '.mp4'
    tikmate().get_media(url)[0].download(path)


