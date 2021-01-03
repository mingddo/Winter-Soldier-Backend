from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from urllib import request, parse
import urllib

import json
import requests


@api_view(["GET"])
def weatherGetInfo(request, base_date, base_time, nx, ny):
    serviceKey = "9UEpXZkDz1BLQmUlXrmpuD6ETz9%2BxfjDKCRHvMMOkeU7iTCu3QSRmtBphVpP6FxjoQoy88%2BXir9f67c13mYSug%3D%3D"
    url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?serviceKey={serviceKey}&pageNo=1&numOfRows=100&dataType=JSON&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    print(response)

    if rescode == 200:
        response_body = response.read()
        # print(response_body.decode("utf-8"))
        dict = json.loads(response_body.decode("utf-8"))
        return Response(dict)
    else:
        # print("Error Code:" + rescode)
        return Response({"err": "Error Code:" + rescode})