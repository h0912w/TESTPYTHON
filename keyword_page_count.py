import requests
import pandas as pd
from openpyxl import Workbook

# 네이버 API 정보
client_id = 'tSi5SK8FWnuywUE7zN92'  # 발급받은 Client ID
client_secret = 'M0sTjhNfrO'  # 발급받은 Client Secret

# 엑셀 파일에서 키워드를 읽기
file_path = 'search_keywords.xlsx'
keywords_df = pd.read_excel(file_path)

# 검색할 키워드 범위 설정 (예: 10번째 행부터 100번째 행까지)
start_row = 30001  # 원하는 시작 행 (1번째 행은 0번째 인덱스이므로, 실제 행 번호에 -1을 해줘야 함)
end_row = 50000  # 원하는 종료 행
keywords = keywords_df.iloc[start_row - 1:end_row, 0]  # 첫 번째 열에서 해당 행 범위의 키워드 추출

# 결과 저장을 위한 엑셀 파일 생성
wb = Workbook()
ws = wb.active
ws.append(['Keyword', 'Total Products'])  # 헤더 추가

# 네이버 쇼핑 API로 각 키워드 검색
for keyword in keywords:
    url = f'https://openapi.naver.com/v1/search/shop.json?query={keyword}'
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }

    # API 요청
    response = requests.get(url, headers=headers)
    result = response.json()

    # 검색된 상품 수 추출
    total_products = result.get('total', 0)
    print(f"'{keyword}'에 대한 네이버 쇼핑의 총 상품 수: {total_products}")

    # 엑셀 파일에 결과 추가
    ws.append([keyword, total_products])

# 결과를 엑셀 파일로 저장
output_path = 'results_30001_50000.xlsx'
wb.save(output_path)

print(f"모든 키워드에 대한 검색이 완료되었습니다. 결과는 '{output_path}'에 저장되었습니다.")
