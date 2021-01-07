from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
import requests
import json
import xmltodict
import pandas as pd


@api_view(["GET"])
def stocks(request, companycode, period):
    date = []
    price = []
    volume = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }

    for page in range(1, period):
        url = "http://finance.naver.com/item/sise_day.nhn?code={companycode}".format(
            companycode=companycode
        )
        url = "{url}&page={page}".format(url=url, page=page)

        response = requests.get(url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        for t in soup.select(".tah.p10"):
            date.append(t.text[5:])

        temp = []
        for tt in soup.select(".tah.p11"):
            # print(tt.text)
            temp.append(tt.text)
        # print(temp)

        for i in range(10):
            price.append(int("".join(temp[6 * i].split(","))))
            volume.append(int("".join(temp[6 * i + 5].split(","))))

    context = {
        "date": date,
        "price": price,
        "volume": volume,
    }
    return Response(context)