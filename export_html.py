import requests
from bs4 import BeautifulSoup

url = 'https://manage.searchad.naver.com/customers/2320771/tool/keyword-planner'
response = requests.get(url)
html = response.text

# 원하는 부분 파싱을 원하면 BeautifulSoup 사용
soup = BeautifulSoup(html, 'html.parser')

# 텍스트 파일로 HTML 저장
with open('output.txt', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())  # 전체 HTML을 파일에 기록

print("HTML 파일이 output.txt로 저장되었습니다.")
