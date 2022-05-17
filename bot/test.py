from ytmusicapi import YTMusic

ytmusic = YTMusic()
search_result = ytmusic.search('Монеточка', limit = 5, filter='songs')

list = list()
for item in search_result:
    videoid = item['videoId']
    url = f'https://music.youtube.com/watch?v={videoid}'
    list.append(url)

print(list)