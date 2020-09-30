import os
import requests
from bs4 import BeautifulSoup
from IPython.display import Image
from PIL import Image as PILImage
import re
import uuid
import rsa
import lzstring
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# 출처: https://rednooby.tistory.com/101 [개발자의 취미생활]

## PublicKey 받는곳 변경 ###
"""
이전
http://static.nid.naver.com/enclogin/keys.nhn

현재(2020. 3. 16 기준)
https://nid.naver.com/login/ext/keys.nhn
"""

# 전역변수
img_dir = './img'
sub_dir = ''
result_img_dir = './result'

result_name = 'blood'
url = 'https://comic.naver.com/webtoon/detail.nhn?titleId=730148&no=1&weekday=tue'


file_list = []

ep_start_num = 1
ep_last_num = 61
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
def run_crawler(ep_url, sub_dir, session):
    # html 파싱
    # ep_url = 'https://comic.naver.com/webtoon/detail.nhn?titleId=662774&no=179&weekday=wed'
    html = session.get(ep_url).text # 로그인 필요없을땐, session > requests(변경)
    soup = BeautifulSoup(html, 'html.parser')
    img_num = 0

    # DOM에서 크롤링할 이미지 식별자 넣기
    for tag in soup.select('.wt_viewer img'):
        img_url = tag['src']
        headers = {'Referer': ep_url}
        img_data = session.get(img_url, headers=headers).content # 해더 추가해서 리퀘스트 보내기 # 로그인 필요없을땐, session > requests(변경)
        # 파일 넘버링
        img_num = img_num + 1
        img_name = sub_dir + '/' + str(img_num).zfill(4) + '.jpg'

        with open(img_name, 'wb') as f:
            f.write(img_data)

### Log In ###
def encrypt(key_str, uid, upw):
    def naver_style_join(l):
        return ''.join([chr(len(s)) + s for s in l])

    sessionkey, keyname, e_str, n_str = key_str.split(',')
    e, n = int(e_str, 16), int(n_str, 16)

    message = naver_style_join([sessionkey, uid, upw]).encode()

    pubkey = rsa.PublicKey(e, n)
    encrypted = rsa.encrypt(message, pubkey)

    return keyname, encrypted.hex()


def encrypt_account(uid, upw):
    key_str = requests.get('https://nid.naver.com/login/ext/keys.nhn').content.decode("utf-8")
    return encrypt(key_str, uid, upw)


def naver_session(nid, npw):
    encnm, encpw = encrypt_account(nid, npw)

    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504]
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    request_headers = {
        'User-agent': 'Mozilla/5.0'
    }

    bvsd_uuid = uuid.uuid4()
    encData = '{"a":"%s-4","b":"1.3.4","d":[{"i":"id","b":{"a":["0,%s"]},"d":"%s","e":false,"f":false},{"i":"%s","e":true,"f":false}],"h":"1f","i":{"a":"Mozilla/5.0"}}' % (bvsd_uuid, nid, nid, npw)
    bvsd = '{"uuid":"%s","encData":"%s"}' % (bvsd_uuid, lzstring.LZString.compressToEncodedURIComponent(encData))

    resp = session.post('https://nid.naver.com/nidlogin.login', data={
        'svctype': '0',
        'enctp': '1',
        'encnm': encnm,
        'enc_url': 'http0X0.0000000000001P-10220.0000000.000000www.naver.com',
        'url': 'www.naver.com',
        'smart_level': '1',
        'encpw': encpw,
        'bvsd': bvsd
    }, headers=request_headers)

    finalize_url = re.search(r'location\.replace\("([^"]+)"\)', resp.content.decode("utf-8")).group(1)
    session.get(finalize_url)

    return session
###

### controller ###
if __name__ == "__main__":

    # 디렉토리 만들고
    check_dir()

    ### 로그인 세션받아오기 ###
    session = naver_session('idid', 'pwpw') # 아이디 비번 하드코딩

    for ep_num in ep_num_list:
        # 디렉토리 만들고
        sub_dir = './img/' + str(ep_num).zfill(4)
        check_sub_dir(sub_dir)

        # 주소 정하고
        ep_url = url.split('&')[0] + '&' + 'no=' + str(ep_num) + '&' + url.split('&')[2]
        print(ep_url)
        print('크롤링 시작 ep:' + str(ep_num))
        # 크롤링
        run_crawler(ep_url, sub_dir, session)
