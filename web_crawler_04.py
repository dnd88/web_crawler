import os
import requests
from bs4 import BeautifulSoup
from IPython.display import Image
from PIL import Image as PILImage

# 출처: https://rednooby.tistory.com/101 [개발자의 취미생활]

# 전역변수
img_dir = './img'
result_img_dir = './result'

result_name = '좀비딸'
url = 'https://comic.naver.com/webtoon/detail.nhn?titleId=715772&no=1&weekday=thu'
img_unit = 20 # 이미지 병합 단위

file_list = []
# ep_num = int(url.split('&')[1][3:]) # 회차
ep_start_num = 1
ep_last_num = 3
ep_num_list = list(range(ep_start_num, ep_last_num+1))
ep_url = url.split('&')[0] + '&' + 'no=' + str(ep_start_num) + '&' + url.split('&')[2]

# img 디렉토리 만들것
def check_dir():
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    # result 디렉토리 만들것
    result_img_dir = './result'
    if not os.path.exists(result_img_dir):
        os.makedirs(result_img_dir)


# 폴더 내 모든 파일 제거
def remove_all_files(filepath = img_dir):
    if os.path.exists(filepath):
        for file in os.scandir(filepath):
            os.remove(file.path)
        return 'Remove All Files'
    else:
        return 'Directory Not Found'

# 파일 불러오기
def load_files():
    file_list = os.listdir(img_dir + '/')
    file_list.sort() # 이미지 이름 순서대로 정렬


### 이미지 받아오기 ###
def run_crawler(ep_url):
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
        img_name = img_dir + '/' + str(img_num).zfill(3) + '.jpg'

        with open(img_name, 'wb') as f:
            f.write(img_data)



### 이미지 합치기 ###
# Maximum supported image dimension is 65500 pixels :: JPG 이미지 한계임


def merge_img(file_list = file_list, img_unit = 20, quotient = 'none', remainder = 'none', ep_num = 0):
    cnt = 0
    # 차례대로 이미지를 저장할 리스트 생성
    image_list = []
    # 반복문이 돌때마다 값을 누적시킬 변수
    full_width, full_height = 0, 0

    # 나머지 파라미터를 전달받았다면 그걸 단위로 사용할 것
    if remainder != 'none':
        img_unit = remainder

    for file in file_list[i * img_unit : i * img_unit + img_unit]: # 합칠 이미지 단위 만큼만

        #지금 이미지를 im에 넣기
        im = PILImage.open(img_dir + '/' + file)
        #가로, 세로 size를 지금 들러온 im에 맞춘다
        width, height = im.size
        #작업을 마친 이미지를 미리선언한 list에 차례대로 저장
        image_list.append(im)
        #최대 가로길이 설정. 가로의 x축0, y축은 im.size에서 수정한 가로너비
        full_width = max(full_width, width)
        #세로길이는 이미지가 누적될수록 계속 길어지므로 길이를 기존길이에서 더함
        full_height += height

    # 캔버스 설정. 배경은 흰색 캔버스 설정을 위해서 최대 크기를 먼저 알아야함 jpg 압축 한계 때문에 높이 65500 넘지 말것
    canvas = PILImage.new('RGB', (full_width, full_height), 'white')

    output_height = 0

    # 리스트에 있는 이미지를 캔버스에 덮어씌우기
    for im in image_list: # 이미지 하나하나, final_image_list는 im을 모아놓은 리스트
        # 현재 이미지의 사이즈를 가로세로 변수에 넣는다
        width, height = im.size
        # 캔버스에 현재 이미지를 붙여넣고(x축0, y축누적높이)
        canvas.paste(im, (0, output_height))
        #세로로 이미지를 붙이기 때문에 높이값을 누적시켜줘야 함
        output_height += height


    # 반복문을 돌면 저장!
    canvas.save(result_img_dir + '/' + result_name + str(ep_num).zfill(3) + '_' + str(i+1).zfill(3) + '.jpg')


### controller ###

# 디렉토리 만들고
check_dir()

for ep_num in ep_num_list:
    # 디렉토리 먼저 비우고
    remove_all_files()

    # 주소 정하고
    ep_url = url.split('&')[0] + '&' + 'no=' + str(ep_num) + '&' + url.split('&')[2]
    print(ep_url)
    print('크롤링 시작 ep:' + str(ep_num))
    # 크롤링
    run_crawler(ep_url)

    # 크롤링 한 파일 불러오고
    load_files()
    # 이미지 총개수를 단위로 나누기
    quotient, remainder = divmod(len(file_list), img_unit) # 나누기의 몫과 나머지

    # 병합하기
    for i in range(quotient + 1):

        if i == (quotient): # 마지막 반복만
            # remainder
            merge_img(file_list = file_list, quotient = quotient, remainder = remainder, ep_num = ep_num)
        else:
            merge_img(file_list = file_list, quotient = quotient, ep_num = ep_num)
