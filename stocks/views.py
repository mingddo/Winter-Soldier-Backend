from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import json
import xmltodict
import pandas as pd


@api_view(['GET'])
def stocks(request, companyname):
    stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0] 
    #stock_code.head()
    print(companyname)
    # 데이터에서 정렬이 따로 필요하지는 않지만 테스트겸 Pandas sort_values를 이용하여 정렬을 시도해봅니다.
    stock_code.sort_values(['상장일'], ascending=True)

    # 필요한 것은 "회사명"과 "종목코드" 이므로 필요없는 column들은 제외
    stock_code = stock_code[['회사명', '종목코드']] 

    # 한글 컬럼명을 영어로 변경 
    stock_code = stock_code.rename(columns={'회사명': 'company', '종목코드': 'code'}) 
    #stock_code.head()

    # 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌 
    stock_code.code = stock_code.code.map('{:06d}'.format) 
    print(companyname.strip())
    company = companyname
    code = stock_code[stock_code.company==company].code.values[0] ## strip() : 공백제거
    print(code)

    
    df = pd.DataFrame()
    for page in range(1, 5):
        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(
            code=code)
        url = '{url}&page={page}'.format(url=url, page=page)
        print(url)
        # print(pd.read_html(url, header=0)[0])
        df = df.append(pd.read_html(url, header=0)[0], ignore_index=True)

    # df.dropna()를 이용해 결측값 있는 행 제거
    df = df.dropna()
    # print('이게뭐지', df)
    # 한글로 된 컬럼명을 영어로 바꿔줌
    df = df.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff',
                            '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})
    # 데이터의 타입을 int형으로 바꿔줌
    df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[[
        'close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
    # 컬럼명 'date'의 타입을 date로 바꿔줌
    df['date'] = pd.to_datetime(df['date'])
    # 일자(date)를 기준으로 오름차순 정렬
    df = df.sort_values(by=['date'])
    df['date'] = df['date'].dt.strftime('%m/%d')

    df_price = df['close'].tolist()
    df_open = df['open'].tolist()
    df_high = df['high'].tolist()
    df_low = df['low'].tolist()
    df_date = df['date'].tolist()
    df_volume = df['volume'].tolist()
    context = []
    for i in range(len(df['date'].tolist())):
        context.append([df_open[i], df_high[i], df_low[i], df_price[i]])
    print([df_date, context, df_volume])
    return Response([df_date, context, df_volume])