from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view


# 네이버 영화 api
import urllib.request
import json
import requests
import random
from pprint import pprint

# Create your views here.


@api_view(["GET"])
def getInfo(request):
    ServiceKey = "c08adfb007952cbd674e7ee0df7109c33"
    url = f"https://api.corona-19.kr/korea/?serviceKey={ServiceKey}"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        # print(response_body.decode("utf-8"))
        dict = json.loads(response_body.decode("utf-8"))
        # pprint(dict)
        return Response(dict)
    else:
        # print("Error Code:" + rescode)
        return Response({"err": "Error Code:" + rescode})


@api_view(["GET"])
def getcityInfo(request):
    ServiceKey = "c08adfb007952cbd674e7ee0df7109c33"
    url = f"https://api.corona-19.kr/korea/country/new/?serviceKey={ServiceKey}"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        # print(response_body.decode("utf-8"))
        dict = json.loads(response_body.decode("utf-8"))
        # pprint(dict)
        return Response(dict)
    else:
        # print("Error Code:" + rescode)
        return Response({"err": "Error Code:" + rescode})