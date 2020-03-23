import os
import requests
from bs4 import BeautifulSoup
from IPython.display import Image

# https://rednooby.tistory.com/101 출처
# img 디렉토리 만들것

ep_url = 'https://comic.naver.com/webtoon/detail.nhn?titleId=670152&no=217&weekday=sun'
html = requests.get(ep_url).text
soup = BeautifulSoup(html, 'html.parser')
num = 0

for tag in soup.select('.wt_viewer img'):
    img_url = tag['src']
    # img_name = os.path.basename(img_url)
    headers = {'Referer': ep_url}
    img_data = requests.get(img_url, headers=headers).content

    num = num + 1
    # print(num)
    img_name = './img/' + str(num).zfill(3) + '.jpg'

    with open(img_name, 'wb') as f:
        f.write(img_data)
