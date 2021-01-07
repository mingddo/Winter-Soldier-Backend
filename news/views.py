from rest_framework.decorators import api_view
from rest_framework.response import Response
from bs4 import BeautifulSoup
from datetime import datetime
import requests


@api_view(["GET"])
def crawler(request, query):
    title_text = []
    link_text = []
    source_text = []
    date_text = []
    contents_text = []
    img_lists = []
    result = {}

    url = "https://search.naver.com/search.naver?where=news&query=" + query

    response = requests.get(url)
    html = response.text

    # 뷰티풀소프의 인자값 지정
    soup = BeautifulSoup(html, "html.parser")

    news_lists = soup.select("li.bx")
    for (idx, t) in enumerate(news_lists):
        if idx == 10:
            break
        title_text.append(t.select(".news_tit")[0].text)
        link_text.append(t.select(".news_tit")[0]["href"])
        contents_text.append(t.select(".dsc_txt_wrap")[0].text)
        source_text.append(t.select(".info_group")[0].select(".press")[0].text)
        date_text.append(t.select(".info_group")[0].select("span")[1].text)
        if t.select(".thumb.api_get"):
            img_lists.append(t.select(".thumb.api_get")[0]["src"])
        else:
            img_lists.append("http://placehold.it/293x180")

    # 모든 리스트 딕셔너리형태로 저장
    temp = []
    for i in range(10):
        result = {
            "id": i,
            "date": date_text[i],
            "title": title_text[i],
            "source": source_text[i],
            "contents": contents_text[i],
            "link": link_text[i],
            "img_source": img_lists[i],
        }
        temp.append(result)
    # page += 10
    return Response(temp)


@api_view(["GET"])
def daymost(request):
    # 유저 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }

    # 네이버 메인이 아닌 DataLab 페이지
    url = "https://datalab.naver.com/keyword/realtimeList.naver?where=main"

    # User 설정
    res = requests.get(url, headers=headers)

    # res.content 주의
    soup = BeautifulSoup(res.content, "html.parser")

    # span.item_title 정보를 선택
    data = soup.select("span.item_title")

    result = []
    for item in data:
        result.append(item.get_text())
    return Response(result[:10])
