import requests
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.golfood

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    food = request.args.get('food')
    return render_template('search_main.html', lat=lat, lng=lng, food=food)

# 검색버튼 클릭시 골프장 리스트 보여주는 API 역할을 하는 부분
@app.route('/golf/list', methods=['GET'])
def show_golf():
    # name_receive = request.form['name_golf']
    name_receive = request.args.get('name_golf')
    golfs = list(db.golf.find({'name': {'$regex': name_receive}}, {'_id': False}))
    # 2. 성공하면 success 메시지와 함께 golf_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'golf_list': golfs})

# 맛집찾기 버튼 클릭시 맛집 리스트 보여주는 API 역할을 하는 부분
@app.route('/golfood/list', methods=['GET'])
def golfood_list():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    food = request.args.get('food')
    headers = {
        'Authorization': 'KakaoAK 14e44457faa2e2f6e7c67e69b9d68832',
    }
    params = {
        'y': lat,
        'x': lng,
        'radius': '20000',
        'query': food
    }
    response = requests.get('https://dapi.kakao.com/v2/local/search/keyword.json', headers=headers, params=params)
    data = response.json()
    print(data)
    return jsonify(data)
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)