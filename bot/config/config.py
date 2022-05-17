# token = "5107264367:AAETMeLMXqszBgC7wzv4elk2MRLuJeaFWIo"  main
import os

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN') or "5183365795:AAHWNSzTh5CiK_2xzjukh0zOGbYceDZw3JA"   
OWNER = os.environ.get('OWNER') or '330663508' 
FILES_STORAGE_GROUP = os.environ.get('FILES_STORAGE_GROUP') or '-644081867'


# instagram
INST_USER = os.environ.get('INST_USER') or 'boxb0y'
INST_PASSWD = os.environ.get('INST_PASSWD') or 'Tardis245'
INST_USERNAME = os.environ.get('INST_USERNAME') or 'boxb0y'


# discord
DISCORD_CHAT_ID = os.environ.get('DISCORD_CHAT_ID') or '226588118394994688'


# Mariadb
MARIA_USER = os.environ.get('MARIA_USER') or 'piter'
MARIA_PASSWD = os.environ.get('MARIA_PASSWD') or 'piter'
MARIA_HOST = os.environ.get('MARIA_HOST') or 'localhost'
MARIA_PORT = os.environ.get('MARIA_PORT') or 3306
MARIA_DB = os.environ.get('MARIA_DB') or 'piter'

# openweather
OPEN_WEATHER_TOKEN = os.environ.get('OPEN_WEATHER_TOKEN') or '70c272edb229fc5251128fe1370f3846'

# socket server
SOCKET_SERVER_IP = os.environ.get('SOCKET_SERVER_IP') or '127.0.0.1'
SOCKET_SERVER_PORT = os.environ.get('SOCKET_SERVER_PORT') or 8888

# webapps url
WEBAPPS_URL = os.environ.get('WEBAPPS_URL') or 'https://127.0.0.1:9000'