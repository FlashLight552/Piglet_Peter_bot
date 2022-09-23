from bs4 import BeautifulSoup as bs
import asyncio
import requests 
import re

from config.create_bot import telegram_bot as bot
from functions.sql import Database


def request_anime_info(url):
    """
    this function will return info about anime
    url: link to anime title in animego
    return: anime name, poster, anime status, amount ep, next ep, fundub studio
    """
    r = requests.get(url)
    if r.status_code != 404:
        soup = bs(r.text, 'lxml')
        title = soup.find('div', class_='anime-title').h1.text
        poster = soup.find('div', class_='anime-poster position-relative cursor-pointer').img['src']
        raw_info = soup.find('dl', class_='row')
        
        info = []
        for item in raw_info:
            raw = re.sub(" +", " ", item.text).strip().splitlines()
            try:
                info.append(raw[0])
            except: pass

        next_ep = [f'{info[i+1]}' for i in range(len(info)) if info[i]=='Следующий эпизод'] or ['']
        amount_ep = [f'{info[i+1]}' for i in range(len(info)) if info[i]=='Эпизоды'] or ['']
        status = [f'{info[i+1]}' for i in range(len(info)) if info[i]=='Статус'] or ['']
        dub = [f'{info[i+1]}' for i in range(len(info)) if info[i]=='Озвучка'] or ['']
        
        return(str(title), str(poster), status[0], amount_ep[0], next_ep[0], str(dub[0]).replace('Профессиональный многоголосый', 'Профессиональный'))


async def new_ep_detector_and_send_msg():
    while True:
        await asyncio.sleep(60 * 15)
        url = 'https://animego.org/'
        r = requests.get(url)
        if r.status_code != 404:
            soup = bs(r.text, 'lxml')
            # new = soup.find_all('span', class_='last-update-title font-weight-600')
            last_update = soup.find('div', class_='last-update')
            new = last_update.find_all('div', class_='media-body')
            list = []

            for item in new:
                title = str(item.span.text).replace('Профессиональный многоголосый', 'Профессиональный')
                ep = item.find('div', class_='font-weight-600 text-truncate').text
                studio = str(item.find('div', class_='text-gray-dark-6').text).replace('(','').replace(')','')
                result = {'title':title, 'studio':studio, 'ep':ep}
                list.append(result)

            db = Database()
            with db.connection:
                for item in list:
                    if db.select_from_last_anime_update(item['title'], item['ep'], item['studio']):
                        # print(f'allready have {item}')
                        pass
                    else:
                        # print(f'add {item}')
                        db.add_last_anime_update(item['title'], item['ep'], item['studio'])

                        user_list = db.select_user_from_sub_to_title(item['title'], item['studio'])
                        for user in user_list:
                            text = f"Вышел новый эпизод!\nНазвание: {item['title']}\nЭпизод: {item['ep']}\nСтудия: {item['studio']}"
                            await bot.send_message(user, text)
                            # print("Отправил сообщение {user}")
                            await asyncio.sleep(0.2)