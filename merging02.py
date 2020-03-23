import os
import requests
from bs4 import BeautifulSoup
from IPython.display import Image
from PIL import Image as PILImage

path = "./img/"
file_list = os.listdir(path)
file_list.sort() # str타입인 이름을 순서대로 정렬
# for file in file_list:
#
#     print(file)

# Maximum supported image dimension is 65500 pixels
# JPG 이미지 한계임


def calc_size(file_list):

    cnt = 0
    #차례대로 이미지를 저장할 리스트 생성
    image_list = []

    #반복문이 돌때마다 값을 누적시킬 변수
    full_width, full_height = 0, 0

    for file in file_list:

        cnt += 1
        if cnt == 20:
            break

        #지금 이미지를 im에 넣기
        im = PILImage.open(path + file)

        #가로, 세로 size를 지금 들러온 im에 맞춘다
        width, height = im.size
        # print(width, height)

        #작업을 마친 이미지를 미리선언한 list에 차례대로 저장
        image_list.append(im)

        #최대 가로길이 설정. 가로의 x축0, y축은 im.size에서 수정한 가로너비
        full_width = max(full_width, width)

        #세로길이는 이미지가 누적될수록 계속 길어지므로 길이를 기존길이에서 더함
        full_height += height


    # print(str(full_width) + '!!!' + str(full_height))
    return full_width, full_height, image_list

fianl_full_width, final_full_height, final_image_list = calc_size(file_list)

#캔버스 설정. 배경은 흰색 캔버스 설정을 위해서 최대 크기를 먼저 알아야함 jpg 압축 한계 때문에 높이 65500 넘지 말것
canvas = PILImage.new('RGB', (fianl_full_width, final_full_height), 'white')

output_height = 0

#리스트에 있는 이미지를 캔버스에 덮어씌우기
for im in final_image_list:#이미지 하나하나, final_image_list는 im을 모아놓은 리스트
    #현재 이미지의 사이즈를 가로세로 변수에 넣는다
    width, height = im.size

    if output_height + height >= 65500 :
        break
    #캔버스에 현재 이미지를 붙여넣고(x축0, y축누적높이)
    canvas.paste(im, (0, output_height))

    #세로로 이미지를 붙이기 때문에 높이값을 누적시켜줘야 함
    output_height += height


#반복문을 돌면 저장!
canvas.save( './result/' + 'merged01.jpg')
