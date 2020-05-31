import os
import requests
from bs4 import BeautifulSoup
from IPython.display import Image
from PIL import Image as PILImage

# 출처: https://rednooby.tistory.com/101 [개발자의 취미생활]

# 전역변수
img_dir = './img'
sub_dir = ''
result_img_dir = './result'

result_name = '테러맨'
url = 'https://comic.naver.com/webtoon/detail.nhn?titleId=670149&no=1&weekday=fri'


file_list = []

ep_start_num = 1
ep_last_num = 211
ep_num_list = list(range(ep_start_num, ep_last_num+1))


# img 디렉토리 만들것
def check_dir():
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)


def check_sub_dir(sub_dir):
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)



### 이미지 받아오기 ###
def run_crawler(ep_url, sub_dir):
    # html 파싱
    # ep_url = 'https://comic.naver.com/webtoon/detail.nhn?titleId=662774&no=179&weekday=wed'
    html = requests.get(ep_url).text
    soup = BeautifulSoup(html, 'html.parser')
    img_num = 0

    # DOM에서 크롤링할 이미지 식별자 넣기
    for tag in soup.select('.wt_viewer img'):
        img_url = tag['src']
        headers = {'Referer': ep_url}
        img_data = requests.get(img_url, headers=headers).content # 해더 추가해서 리퀘스트 보내기
        # 파일 넘버링
        img_num = img_num + 1
        img_name = sub_dir + '/' + str(img_num).zfill(4) + '.jpg'

        with open(img_name, 'wb') as f:
            f.write(img_data)




### controller ###

# 디렉토리 만들고
check_dir()

for ep_num in ep_num_list:
    # 디렉토리 만들고
    sub_dir = './img/' + str(ep_num).zfill(4)
    check_sub_dir(sub_dir)

    # 주소 정하고
    ep_url = url.split('&')[0] + '&' + 'no=' + str(ep_num) + '&' + url.split('&')[2]
    print(ep_url)
    print('크롤링 시작 ep:' + str(ep_num))
    # 크롤링
    run_crawler(ep_url, sub_dir)
