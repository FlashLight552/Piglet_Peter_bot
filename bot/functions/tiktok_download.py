# from tiktok_downloader import snaptik, tikwm

# import requests
# import bs4
# import os
# import re

# class


# class tiktok_downloader11:
#     def __init__(self):
#         pass

#     def musicaldown(self, url, output_name):
#         """url: tiktok video url
#         output_name: output video (.mp4). Example : video.mp4
#         """
#         ses = requests.Session()
#         server_url = 'https://musicaldown.com/'
#         headers = {
#             "Host": "musicaldown.com",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#             "Accept-Language": "en-US,en;q=0.5",
#             "DNT": "1",
#             "Upgrade-Insecure-Requests": "1",
#             "Sec-Fetch-Dest": "document",
#             "Sec-Fetch-Mode": "navigate",
#             "Sec-Fetch-Site": "none",
#             "Sec-Fetch-User": "?1",
#             "TE": "trailers"
#         }
#         ses.headers.update(headers)
#         req = ses.get(server_url)
#         data = {}
#         parse = bs4.BeautifulSoup(req.text, 'html.parser')
#         get_all_input = parse.findAll('input')
#         for i in get_all_input:
#             if i.get("id") == "link_url":
#                 data[i.get("name")] = url
#             else:
#                 data[i.get("name")] = i.get("value")
#         post_url = server_url + "id/download"

#         req_post = ses.post(post_url, data=data, allow_redirects=True)
#         if req_post.status_code == 302 or 'This video is currently not available' in req_post.text or 'Video is private or removed!' in req_post.text:
#             print('- video private or remove')
#             return 'private/remove'
#         elif 'Submitted Url is Invalid, Try Again' in req_post.text:
#             print('- url is invalid')
#             return 'url-invalid'
#         get_all_blank = bs4.BeautifulSoup(req_post.text, 'html.parser').findAll(
#             'a', attrs={'target': '_blank'})

#         download_link = get_all_blank[0].get('href')

#         get_content = requests.get(download_link)

#         path = f'{output_name}.mp4'
#         with open(path, 'wb') as fd:
#             fd.write(get_content.content)
#             file_size = os.stat(path).st_size / (1024*1024)

#         if file_size > 0.02:
#             return [path]
    
#         os.remove(path)
#         url_rx = re.compile(r'https?://(?:www\.)?.+')
#     # img url 
#         get_all_img = bs4.BeautifulSoup(req_post.text, 'html.parser').findAll(
#             'a', class_='btn waves-effect waves-light orange')
#         urls = []
#         for item in get_all_img:
#             urls.append(item.get('href'))

#     # mp3 url download
#         get_mp3 = bs4.BeautifulSoup(req_post.text, 'html.parser').findAll(
#             'a', class_='btn waves-effect waves-light orange download')

#         urls.append(get_mp3[0].get('href'))
        
#         path_list = []
#         urlist_len = len(urls)-1
#         file_extension = 'jpeg'
        
#         for num, item in enumerate(urls):
#             if not url_rx.match(item):
#                 continue
            
#             get_content = requests.get(item)
            
#             if urlist_len == num:
#                 file_extension = 'mp3'
            
#             path = f'{output_name}_{num}.{file_extension}'
            
#             with open(path, 'wb') as fd:
#                 fd.write(get_content.content)
#                 path_list.append(path)
#         return path_list

# # def download_video(url, id):    
# #     path = 'downloads/tiktok/'+ str(id)
# #     try:
# #         dl = tiktok_downloader()
# #         list = dl.musicaldown(url=url,output_name=path)
# #         return list
# #     except: pass



