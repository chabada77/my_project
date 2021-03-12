import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.golfood


# DB에 저장할 골프장 정보를 Scrapping 후 DB에 저장합니다.
def scrap_golf():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('http://greensq.co.kr/page/golfcourse.html', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    trs = soup.select('.greensq_golfList table tbody tr')
    for tr in trs:
        a_tag = tr.select_one('.name a')
        name = a_tag.text.strip()
        url = a_tag['href']
        address = tr.select_one('.address').text.strip()
        print(name, address)
        try:
            lat, lng = address_to_latlng(address)
            print(name, url, address, lat, lng)
            doc = {
                'name': name,
                'url': url,
                'address': address,
                'lat': lat,
                'lng': lng
            }
            db.golf.insert_one(doc)
        except:
            print('skip')
            continue


# Scrapping 해서 가져온 골프장 정보의 주소로 위 경도 정보를 Scrapping 합니다.
def address_to_latlng(address):
    import requests
    headers = {
        'Authorization': 'KakaoAK 14e44457faa2e2f6e7c67e69b9d68832',
    }
    response = requests.get(f'https://dapi.kakao.com/v2/local/search/address.json?query={address}', headers=headers)
    result = response.json()
    lng = result['documents'][0]['address']['x']
    lat = result['documents'][0]['address']['y']
    return [lat, lng]


### DB를 삭제후 실행하기
db.golf.drop()
scrap_golf()
