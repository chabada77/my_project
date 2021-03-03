import requests
from flask import Flask, render_template


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/golf/list', methods=['POST'])


headers = {
    'X-Naver-Client-Id': 'dJgbOeSXBCSZZCUvfYuA',
    'X-Naver-Client-Secret': '9Up9AVQHKl',
}

params = {
    'query': '검색어',
    'display': '10',
    'start': '1',
    'sort': 'sim',
}

response = requests.get('https://openapi.naver.com/v1/search/blog.json', headers=headers, params=params)
data = response.json()
print(data)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
