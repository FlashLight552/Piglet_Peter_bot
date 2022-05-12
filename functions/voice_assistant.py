from aiogram.utils.markdown import hlink
from youtube_search import YoutubeSearch
from googletrans import Translator
from pyowm import OWM
import random

from config.config import OPEN_WEATHER_TOKEN


def search_on_google(*args):
    return 'comming coon'


def search_on_youtube(*args):
    search = YoutubeSearch(f'{args}', max_results=5).to_dict()
    result = ''

    for item in search:
        id = item['id']
        title = item['title']
        url = f'https://www.youtube.com/watch?v={id}'
        result += f'{hlink(title, url)}\n'
    
    return result
        

def get_weather(*args):
    if args[0]:
        try:
            city = f'{args[0][0]}, {args[0][1]}'
        except:
            city = f'{args[0][0]}'
       
    owm = OWM(OPEN_WEATHER_TOKEN)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    w = observation.weather
    location = observation.location.to_dict()
    g_translate = Translator()

    country_name = location['country']
    city_name = location['name']
    temp = (int(w.temperature('celsius')['temp']))
    temp_feels_like = (int(w.temperature('celsius')['feels_like']))
    wind_speed = float('{:.2f}'.format(w.wind('km_hour')['speed']))
    wind_gust = float('{:.2f}'.format(w.wind('km_hour')['gust']))
    press = (int(float(w.barometric_pressure()['press']) * 0.75006157584566))
    humidity = w.humidity
    weather_status = g_translate.translate(text=w.detailed_status,dest='ru',src='en').text

    weather =   f'{city_name},{country_name}\n'\
                f'{weather_status.title()}\n'\
                f'Температура:{temp}°C\nОщущается: {temp_feels_like}°C\n'\
                f'Скорость ветра: {wind_speed}km/h\nПорывы ветра: {wind_gust}km/h\n'\
                f'Давление: {press}mm\nВлажность: {humidity}%'

    return weather

def toss_coin(*args):
    coim = ('Орел','Решка')
    return (random.choice(coim))


def execute_command_with_name(command_name: str, *args: list):
    for key in commands.keys():
        if command_name in key:
            return commands[key](*args)


commands = {
    ("search", "google", "гугл", "найди"): search_on_google,
    ("video", "youtube", "ютуб", "видео"): search_on_youtube,
    ("weather", "forecast", "погода", "прогноз"): get_weather,
    ("toss", "мотенка", "монета", "подбрось"): toss_coin,
}


def assistent(voice_input:str):
    split_input = voice_input.split()
    command = split_input[0].lower()
    command_param = split_input[1:]
    return execute_command_with_name(command, command_param)





    


