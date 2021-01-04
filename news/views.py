from rest_framework.decorators import api_view
from rest_framework.response import Response
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re


@api_view(["GET"])
def crawler(request, query):
    title_text = []
    link_text = []
    source_text = []
    date_text = []
    contents_text = []
    result = {}

    url = "https://search.naver.com/search.naver?where=news&query=" + query

    response = requests.get(url)
    html = response.text

    # 뷰티풀소프의 인자값 지정
    soup = BeautifulSoup(html, "html.parser")
    # <a>태그에서 제목과 링크주소 추출
    # print(soup)
    atags = soup.select(".news_tit")
    # print(atags)
    for atag in atags:
        # print(atag)
        title_text.append(atag.text)  # 제목
        link_text.append(atag["href"])  # 링크주소

    # 신문사 추출
    source_lists = soup.select(".info_group")
    for source_list in source_lists:
        source_text.append(source_list.select(".press")[0].text)

    # 작성시간 추출
    for source_list in source_lists:
        date_text.append(source_list.select("span")[1].text)

    # # 본문요약본
    contents_lists = soup.select(".dsc_txt_wrap")
    for contents_list in contents_lists:
        contents_text.append(contents_list.text)

    # 모든 리스트 딕셔너리형태로 저장
    temp = []
    for i in range(10):
        result = {
            "date": date_text[i],
            "title": title_text[i],
            "source": source_text[i],
            "contents": contents_text[i],
            "link": link_text[i],
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
