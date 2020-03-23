import os
import requests
from bs4 import BeautifulSoup
from IPython.display import Image
from PIL import Image as PILImage


ep_url = 'https://comic.naver.com/webtoon/detail.nhn?titleId=670152&no=217&weekday=sun'
html = requests.get(ep_url).text
soup = BeautifulSoup(html, 'html.parser')

#차례대로 이미지를 저장할 리스트 생성
image_list = []

#반복문이 돌때마다 값을 누적시킬 변수
full_width, full_height = 0, 0


for tag in soup.select('.wt_viewer img'):
    img_url = tag['src']
    img_name = os.path.basename(img_url)
    headers = {'Referer': ep_url}
    img_data = requests.get(img_url, headers=headers).content

    #파일 읽기/쓰기
    with open(img_name, 'wb') as f:
        #데이터를 써주기
        f.write(img_data)

        #지금 이미지를 im에 넣기
        im = PILImage.open(img_name)

        #가로, 세로 size를 지금 들러온 im에 맞춘다
        width, height = im.size

        #작업을 마친 이미지를 미리선언한 list에 차례대로 저장
        image_list.append(im)

        #최대 가로길이 설정. 가로의 x축0, y축은 im.size에서 수정한 가로너비
        full_width = max(full_width, width)

        #세로길이는 이미지가 누적될수록 계속 길어지므로 길이를 기존길이에서 더함
        full_height += height

#캔버스 설정. 배경은 흰색
canvas = PILImage.new('RGB', (full_width, full_height), 'white')

output_height = 0

#리스트에 있는 이미지를 캔버스에 덮어씌우기
for im in image_list:#이미지 하나하나, img_list는 im을 모아놓은 리스트
    #현재 이미지의 사이즈를 가로세로 변수에 넣는다
    width, height = im.size

    #캔버스에 현재 이미지를 붙여넣고(x축0, y축누적높이)
    canvas.paste(im, (0, output_height))

    #세로로 이미지를 붙이기 때문에 높이값을 누적시켜줘야 함
    output_height += height

#반복문을 돌면 저장!
canvas.save('merged.jpg')
