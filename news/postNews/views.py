import json
from django.http import JsonResponse
from getNews.models import NewsData
from django.views.decorators.csrf import csrf_exempt
import datetime

@csrf_exempt
def format_news_text(news_items):
    print("텍스트 생성중")
    return "\n".join(f"{item.title}\n{item.url}" for item in news_items)

def send_news_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Received data: {data}")  # 요청 데이터 출력

            # 'key word'가 뉴스 관련 키워드인지 확인
            keyword = data.get('action', {}).get('params', {}).get('key_word', '')
            if keyword.lower() in ['뉴스', 'news']:
                print(f"Extracted keyword: {keyword}")  # 추출된 키워드 출력

                # 지난 24시간 이내의 뉴스 필터링
                time_threshold = datetime.datetime.now() - datetime.timedelta(days=1)
                news_items = NewsData.objects.filter(timestamp__gte=time_threshold)
                news_text = format_news_text(news_items)

                response_data = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "simpleText": {
                                    "text": news_text
                                }
                            }
                        ]
                    }
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({"error": "Invalid keyword"}, status=400)

        except Exception as e:
            print(f"Error in processing the request: {e}")  # 오류 출력
            return JsonResponse({'error': 'Error in processing the request'}, status=500)

    print("Received non-POST request")  # 비POST 요청 출력
    return JsonResponse({'error': 'Invalid request'}, status=400)
