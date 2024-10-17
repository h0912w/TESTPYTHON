from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys  # Keys 모듈 임포트
import time

# Chrome WebDriver 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 사이트 열기
url = 'https://whereispost.com/seller/'
driver.get(url)

# 검색어 목록
search_keywords = ['검색어1', '검색어2', '검색어3']

for keyword in search_keywords:
    search_box = driver.find_element('name', 'keyword')
    search_box.clear()
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)  # Enter 키 입력
    time.sleep(3)

driver.quit()
