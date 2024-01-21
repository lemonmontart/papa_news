from django.http import HttpResponse
from django.conf import settings
import requests
from urllib.parse import urlparse
import datetime
from bs4 import BeautifulSoup  # BeautifulSoup 임포트
from .models import NewsData

# 네이버 API 설정
NAVER_CLIENT_ID = settings.NAVER_CLIENT_ID
NAVER_CLIENT_SECRET = settings.NAVER_CLIENT_SECRET

# 네이버 API로부터 데이터 가져오는 함수
def get_naver_data(srcText):
    base = "https://openapi.naver.com/v1/search/news.json"
    params = {
        'query': srcText,
        'display': 100
    }
    headers = {
        'X-Naver-Client-Id': NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': NAVER_CLIENT_SECRET
    }

    try:
        response = requests.get(base, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.datetime.now()}] Error: {e}")
        return None

# HTML 태그를 제거하는 함수
def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.get_text()

# 도메인 체크 및 데이터 저장 함수
def save_if_allowed_domain(item, srcText, allowed_domains):
    link = item['link']
    press = urlparse(link).netloc

    if any(domain in link for domain in allowed_domains):
        title = clean_html(item['title'])  # HTML 태그 제거
        pub_date = item['pubDate']
        pDate = datetime.datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S +0900')
        current_time = datetime.datetime.now()
        time_difference = current_time - pDate

        if time_difference.total_seconds() <= 86400:
            NewsData.objects.create(
                keyword=srcText,
                title=title,
                url=link,
                timestamp=pDate,
                press=press
            )

# 뉴스 크롤링 및 저장 뷰 함수
def index(request):
    keywords = ['농식품 시장', '유통 스타트업', '식자재 시장', '기업형 슈퍼마켓',
                '개인 슈퍼마켓', 'K-푸드', '지방 소멸', '몽골 시장']
    allowed_domains = ['aflnews.co.kr', 'amnews.co.kr', 'hankyung.com',
                       'mk.co.kr', 'chosun.com', 'joongang.co.kr', 'donga.com',
                       'yna.co.kr', 'thebell.co.kr']

    for srcText in keywords:
        response_data = get_naver_data(srcText)
        if response_data is None:
            continue

        for item in response_data.get('items', []):
            save_if_allowed_domain(item, srcText, allowed_domains)

    return HttpResponse('뉴스 데이터 저장 완료')
