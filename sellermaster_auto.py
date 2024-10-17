import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

# 엑셀 파일에서 검색어 목록 불러오기
excel_file = 'search_keywords.xlsx'  # 엑셀 파일 경로
df = pd.read_excel(excel_file)

# 검색어가 있는 열을 지정 (예: '검색어' 열이 있을 경우)
search_keywords = df['검색어'].tolist()

# Chrome WebDriver 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 사이트 열기
url = 'https://whereispost.com/seller/'
driver.get(url)

# 검색어 입력 및 검색 실행
for index, keyword in enumerate(search_keywords):
    search_box = driver.find_element('name', 'keyword')
    search_box.clear()
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)  # Enter 키 입력
    time.sleep(3)  # 검색 결과 로딩 대기

    # 마지막 검색어일 때만 엑셀 다운로드 버튼 클릭
    if index == len(search_keywords) - 1:
        excel_download_button = driver.find_element('id', 'excel')  # 엑셀 다운로드 버튼의 id 속성 사용
        excel_download_button.click()
        time.sleep(5)  # 파일 다운로드를 기다리기 위한 대기 시간 설정

# 브라우저 닫기
driver.quit()
