from bs4 import BeautifulSoup
import urllib.request

def get(max_count = 1):
    base_url = "http://10000img.com/"
    url = "http://10000img.com/ran.php"

    count = 1
    while count <= max_count:
        print("+---------[ %d번 째 이미지 ]---------+" % count)

        html = urllib.request.urlopen(url)
        source = html.read()

        soup = BeautifulSoup(source, "html.parser")

        img = soup.find("img")  # 이미지 태그
        img_src = img.get("src") # 이미지 경로
        img_url = base_url + img_src # 다운로드를 위해 base_url과 합침
        img_name = img_src.replace("/", "") # 이미지 src에서 / 없애기

        urllib.request.urlretrieve(img_url, "./img/" + img_name)

        print("이미지 src:", img_src)
        print("이미지 url:", img_url)
        print("이미지 명:", img_name)
        print("\n")
        count += 1 # 갯수 1 증가
    else:
        print("크롤링 종료")

get(1)
