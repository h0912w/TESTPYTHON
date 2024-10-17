def get_search_results_naver(keyword):
    search_url = f"https://search.naver.com/search.naver?query={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve data for {keyword}. Status code: {response.status_code}")
            return 0

        # 페이지의 HTML 텍스트 출력
        print(response.text)  # 디버깅을 위해 HTML 전체를 출력

        soup = BeautifulSoup(response.text, "html.parser")
        result_stats = soup.find("span", {"class": "title_num"})
        if result_stats:
            results_text = result_stats.get_text()
            print(f"Results text for {keyword}: {results_text}")  # 디버깅을 위해 출력
            num_results = re.findall(r'\d+', results_text.replace(',', ''))
            num_results = ''.join(num_results)
        else:
            print(f"No results found for keyword {keyword}")
            num_results = 0

        time.sleep(random.uniform(1, 3))  # 1에서 3초 사이의 랜덤한 지연 추가
    except Exception as e:
        num_results = 0
        print(f"Error occurred for keyword {keyword}: {e}")
    return int(num_results)
