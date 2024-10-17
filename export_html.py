import requests
from bs4 import BeautifulSoup

url = 'https://whereispost.com/seller/'
response = requests.get(url)
html = response.text

# 원하는 부분 파싱을 원하면 BeautifulSoup 사용
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())  # 전체 HTML 출력
