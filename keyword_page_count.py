import requests
import pandas as pd
from openpyxl import Workbook
import hmac
import hashlib
import base64
import time

# 네이버 API 정보 (쇼핑 API)
client_id = 'tSi5SK8FWnuywUE7zN92'  # 발급받은 Client ID
client_secret = 'M0sTjhNfrO'  # 발급받은 Client Secret

# 네이버 검색광고 API 정보
customer_id = '2320771'
api_key = '010000000080abaaa776a0f5f434b44bcc132246740144a33bea6b24464af83ad019627b64'
secret_key = 'AQAAAACAq6qndqD19DS0S8wTIkZ01Nxyac07ihqvxukGn7vhYQ=='

# 엑셀 파일에서 키워드를 읽기
file_path = 'search_keywords.xlsx'
keywords_df = pd.read_excel(file_path)

# 검색할 키워드 범위 설정
start_row = 90001  # 원하는 시작 행
end_row = 90010  # 원하는 종료 행
keywords = keywords_df.iloc[start_row - 1:end_row, 0]  # 첫 번째 열에서 해당 행 범위의 키워드 추출

# 결과 저장을 위한 엑셀 파일 생성
wb = Workbook()
ws = wb.active
ws.append(['Keyword', 'Total Products', 'Total Search Results', 'Product + Search Results', 'Monthly PC Searches',
           'Monthly Mobile Searches', 'Total Monthly Searches', 'Ratio', 'Ratio2'])  # 헤더 추가

# 네이버 쇼핑 API와 일반 검색 API로 각 키워드 검색
for keyword in keywords:
    # 네이버 쇼핑 API 호출
    shopping_url = f'https://openapi.naver.com/v1/search/shop.json?query={keyword}'
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    shopping_response = requests.get(shopping_url, headers=headers)
    shopping_result = shopping_response.json()

    # 검색 결과의 총 상품 수
    total_products = shopping_result.get('total', 0)

    # 네이버 일반 검색 API 호출
    search_url = f'https://openapi.naver.com/v1/search/blog.json?query={keyword}'
    search_response = requests.get(search_url, headers=headers)
    search_result = search_response.json()

    # 일반 검색 결과의 총 검색 수
    total_search_results = search_result.get('total', 0)

    # Total Products와 Total Search Results의 합
    product_search_sum = total_products + total_search_results

    # 네이버 검색광고 API로 검색량 조회
    timestamp = str(int(time.time() * 1000))
    uri = '/keywordstool'
    method = 'GET'
    base_url = 'https://api.naver.com'


    # 시그니처 생성 함수
    def generate_signature(timestamp, method, uri, secret_key):
        message = f"{timestamp}.{method}.{uri}"
        hash = hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256)
        return base64.b64encode(hash.digest()).decode('utf-8')


    # 검색광고 API 헤더 생성
    signature = generate_signature(timestamp, method, uri, secret_key)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Timestamp': timestamp,
        'X-API-KEY': api_key,
        'X-Customer': customer_id,
        'X-Signature': signature,
    }

    # 검색광고 API 요청
    searchad_url = f'{base_url}{uri}?hintKeywords={keyword}&showDetail=1'
    searchad_response = requests.get(searchad_url, headers=headers)
    searchad_result = searchad_response.json()

    # 검색량 데이터 추출
    if 'keywordList' in searchad_result and searchad_result['keywordList']:
        # PC 검색량과 모바일 검색량이 '<'를 포함할 경우 0으로 처리
        monthly_pc_searches = searchad_result['keywordList'][0].get('monthlyPcQcCnt', 0)
        monthly_mobile_searches = searchad_result['keywordList'][0].get('monthlyMobileQcCnt', 0)

        if isinstance(monthly_pc_searches, str) and "<" in monthly_pc_searches:
            monthly_pc_searches = 0
        if isinstance(monthly_mobile_searches, str) and "<" in monthly_mobile_searches:
            monthly_mobile_searches = 0
    else:
        monthly_pc_searches = 0
        monthly_mobile_searches = 0

    # PC와 모바일 검색량 합산
    total_monthly_searches = monthly_pc_searches + monthly_mobile_searches

    # Ratio 계산 (Total Monthly Searches / Total Products)
    if total_products == 0 and total_monthly_searches == 0:
        ratio = -1  # 두 값 모두 0인 경우 -1로 표기
    elif total_products == 0 and total_monthly_searches != 0:
        ratio = round(total_monthly_searches / 0.001, 3)  # total_products가 0일 때 0.001로 나눔
    else:
        ratio = round(total_monthly_searches / total_products, 3)  # 소수점 셋째 자리까지 표시

    # Ratio2 계산 (Total Monthly Searches / Product + Search Results)
    if product_search_sum == 0 and total_monthly_searches == 0:
        ratio2 = -1  # 두 값 모두 0인 경우 -1로 표기
    elif product_search_sum == 0 and total_monthly_searches != 0:
        ratio2 = round(total_monthly_searches / 0.001, 3)  # product_search_sum이 0일 때 0.001로 나눔
    else:
        ratio2 = round(total_monthly_searches / product_search_sum, 3)  # 소수점 셋째 자리까지 표시

    print(
        f"'{keyword}'에 대한 네이버 쇼핑 총 상품 수: {total_products}, 일반 검색 결과 수: {total_search_results}, 총 합: {product_search_sum}, 월간 PC 검색량: {monthly_pc_searches}, 월간 모바일 검색량: {monthly_mobile_searches}, 총 월간 검색량: {total_monthly_searches}, 비율: {ratio}, 비율2: {ratio2}")

    # 엑셀 파일에 결과 추가
    ws.append([keyword, total_products, total_search_results, product_search_sum, monthly_pc_searches,
               monthly_mobile_searches, total_monthly_searches, ratio, ratio2])

# 결과를 엑셀 파일로 저장
output_path = 'test.xlsx'
wb.save(output_path)

print(f"모든 키워드에 대한 검색이 완료되었습니다. 결과는 '{output_path}'에 저장되었습니다.")
