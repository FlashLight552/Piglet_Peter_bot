from TikTokAPI import TikTokAPI
from tiktok_downloader import tikmate
import requests
from bs4 import BeautifulSoup

def get_video_id(url): 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
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

    tikmate().get_media(url)[0].download('tiktok_download/' + video_id + '.mp4')

def download_video_test(video_id):    
    api = TikTokAPI()
    api.downloadVideoById(video_id=video_id, save_path = 'tiktok_download/' + video_id + '.mp4')
