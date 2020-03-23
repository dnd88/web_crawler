import os
import requests
from bs4 import BeautifulSoup
from IPython.display import Image
from PIL import Image as PILImage

# 출처: https://rednooby.tistory.com/101 [개발자의 취미생활]

# 전역변수
img_dir = './img1'
result_img_dir = './result'


# img 디렉토리 만들것
def check_dir():
    img_dir = './img'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    # result 디렉토리 만들것
    result_img_dir = './result'
    if not os.path.exists(result_img_dir):
        os.makedirs(result_img_dir)


### 이미지 받아오기 ###
def run_crawler():
    # html 파싱
    ep_url = 'https://comic.naver.com/webtoon/detail.nhn?titleId=662774&no=179&weekday=wed'
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

# run_crawler() # 크롤러 실행

### 이미지 합치기 ###

# 파일 불러오기
file_list = os.listdir(img_dir + '/')
file_list.sort() # 이미지 이름 순서대로 정렬


# Maximum supported image dimension is 65500 pixels
# JPG 이미지 한계임

img_unit = 20
sum_imgs = len(file_list) # 이미지 총개수
quotient, remainder = divmod(sum_imgs, img_unit) # 나누기의 몫과 나머지


for i in range(quotient + 1):

    if i == (quotient): # 마지막 반복만
        # remainder
        cnt = 0
        # 차례대로 이미지를 저장할 리스트 생성
        image_list = []
        # 반복문이 돌때마다 값을 누적시킬 변수
        full_width, full_height = 0, 0

        for file in file_list[i * img_unit : i * img_unit + remainder]: # 합칠 이미지 단위 만큼만

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


        #반복문을 돌면 저장!
        canvas.save(result_img_dir + '/' + 'merged' + str(i+1).zfill(3) + '.jpg')

        break
    else:
        cnt = 0
        # 차례대로 이미지를 저장할 리스트 생성
        image_list = []
        # 반복문이 돌때마다 값을 누적시킬 변수
        full_width, full_height = 0, 0

        print(i * img_unit)
        print(i * img_unit + img_unit)
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


        #반복문을 돌면 저장!
        canvas.save(result_img_dir + '/' + 'merged' + str(i+1).zfill(3) + '.jpg')
