import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 엑셀 파일에서 검색어 목록 불러오기
excel_file = 'search_keywords.xlsx'  # 엑셀 파일 경로
df = pd.read_excel(excel_file)

# 검색어가 있는 열을 지정 (예: '검색어' 열이 있을 경우)
search_keywords = df['검색어'].tolist()


def open_browser_and_search(keywords, start_index):
    # Chrome WebDriver 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # 사이트 열기
    url = 'https://whereispost.com/seller'
    driver.get(url)

    # 검색어 입력 및 검색 실행
    for index, keyword in enumerate(keywords, start=start_index):
        # 검색창 찾기 및 키워드 입력
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'keyword'))
        )
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)  # Enter 키 입력

        # 검색 결과가 로드될 때까지 대기 (로딩이 끝나는 조건은 필요시 수정)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'excel'))
        )

        time.sleep(3)  # 검색 결과가 로드되었으므로 잠깐 대기

        # 10개의 검색어 처리 후 엑셀 다운로드 및 브라우저 종료
        if (index + 1) % 10 == 0 or index == len(search_keywords) - 1:  # 10개마다 또는 마지막 검색어일 때
            try:
                # 엑셀 다운로드 버튼이 활성화될 때까지 기다림
                excel_download_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'excel'))
                )
                # 스크롤을 통해 다운로드 버튼이 화면에 보이도록 이동
                driver.execute_script("arguments[0].scrollIntoView();", excel_download_button)
                excel_download_button.click()
                time.sleep(5)  # 파일 다운로드를 기다리기 위한 대기 시간 설정
            except Exception as e:
                print(f"엑셀 다운로드 버튼을 클릭하는 중 오류 발생: {e}")
            finally:
                driver.quit()  # 브라우저 종료
                return index + 1  # 현재 처리된 마지막 검색어 인덱스 반환


# 10개씩 처리하여 엑셀 다운로드 후, 다시 새로운 브라우저 세션에서 이어서 처리
start_index = 0
while start_index < len(search_keywords):
    start_index = open_browser_and_search(search_keywords[start_index:start_index + 10], start_index)
