import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 엑셀 파일 경로
file_path = 'search_keywords.xlsx'
keywords_df = pd.read_excel(file_path)

# 결과 저장 리스트
results = []

# 네이버 쇼핑 기본 URL
base_url = "https://search.shopping.naver.com/search/all?query="

for keyword in keywords_df['검색어']:
    search_url = base_url + keyword
    response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        count_element = soup.find("span", class_="subFilter_num__S9sle")
        product_count = int(count_element.text.replace(',', '')) if count_element else 0
    else:
        product_count = None

    # 터미널에 출력
    print(f"키워드: {keyword}, 상품 수: {product_count}")

    # 결과 리스트에 추가
    results.append({"검색어": keyword, "상품 수": product_count})

    # 네이버 요청 제한을 피하기 위해 잠시 대기
    time.sleep(1)

# 결과를 엑셀 파일로 저장
output_df = pd.DataFrame(results)
output_df.to_excel('naver_shopping_results.xlsx', index=False)
