import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import random

def get_search_results(keyword):
    search_url = f"https://www.google.com/search?q={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        result_stats = soup.find(id="result-stats")
        if result_stats:
            results_text = result_stats.text
            num_results = re.findall(r'\d+', results_text.replace(',', ''))
            num_results = ''.join(num_results)
        else:
            num_results = 0
        time.sleep(random.uniform(1, 3))  # 1에서 3초 사이의 랜덤한 지연 추가
    except Exception as e:
        num_results = 0
        print(f"Error occurred for keyword {keyword}: {e}")
    return int(num_results)

# 엑셀 파일에서 키워드 목록 불러오기
input_file = 'keywords.xlsx'
keywords_df = pd.read_excel(input_file)

print(f"Loaded keywords: {keywords_df.shape[0]} rows")

# 검색 결과 수집
results = []
for index, row in keywords_df.iterrows():
    keyword = row['Keyword']
    print(f"Processing keyword {index + 1}/{keywords_df.shape[0]}: {keyword}")
    num_results = get_search_results(keyword)
    results.append({
        'Keyword': keyword,
        'Search Results': num_results
    })

# 결과를 데이터프레임으로 변환 및 저장
results_df = pd.DataFrame(results)
output_file = 'keyword_search_results.xlsx'
results_df.to_excel(output_file, index=False)

print(f"검색 결과가 {output_file} 파일에 저장되었습니다.")
