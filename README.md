# 순서

1. `python -m venv venv`

2. `source venv/Scripts/activate`

3. `pip install django`

4. `django-admin startproject Myproject`

5. `python manage.py startapp Myapp`

6. settings.py에 app 추가

7. `pip install djangorestframework`

8. settings.py에 `rest_framework` app 등록

9. `pip install djangorestframework djangorestframework-jwt`

10. settings.py에 하단

    ```python
    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        ),
    }
    ```

    

11. `pip install django-cors-headers`

12. settings.py에 `'corsheaders'` app 등록

13. `MIDDLEWARE`에 `'corsheaders.middleware.CorsMiddleware',` 추가

14. `pip freeze > requirements.txt`

# 의문

## 왜 rest_framework를 사용하는가?

- front에서 요청을 보냈을 때, 

  서버에 있는 DB에서 원하는 데이터를 JSON 형식으로 보내는 것을 편리하게 하기 위해 사용



## REST, API <a href="https://gmlwjd9405.github.io/2018/09/21/rest-and-restful.html" target="_blank">(참고)</a>

- `REST(Repersentational State Transfer)`
  - 각 요청이 어떠한 동작&정보를 위한 것인지 <b><u>요청 형식 자체(주소)로 파악이 가능</u></b>한 것
  - 자원의 표현에 의한 상태 전달
  - HTTP URI를 통해 자원을 명시하고, HTTP Method를 통해 해당 자원에 대한 CRUD Operation을 적용하는 것
- `API(Application Programming Interface)`
  - 데이터와 기능의 집합을 제공하여 컴퓨터 프로그램간 상호작용을 촉진하며, 서로 정보를 교환 가능하도록 하는 것
- `REST API`
  - REST 기반으로 서비스 API를 구현한 것
  - 최근 Open API, 마이크로 서비스 등을 제공하는 업체 대부분은 REST API를 제공한다.





## JWT(JSON Web Token) <a href="https://jwt.io/" target="_blank">(공식홈페이지)</a>

#### (1) JWT 구조 - `xxxx.yyyy.zzzz`

- `xxxx` : 헤더(header), `yyyy` : 내용(payload), `zzzz` : 서명(signature)
- Header : token의 type과 사용된 알고리즘, 여기서 정의한 알고리즘은 시그니처에서 다시 사용된다.
- Payload : 토큰에 담길 정보가 들어있는 곳(claim - key:value)
- Signature : 헤더와 payload를 기반으로 이 둘을 조합해서 만든 비밀키로 hashing

---

:heavy_check_mark: <b>정보(Payload)</b>

- registered claim (등록된 클레임)
  - 토큰에 대한 정보들을 담기 위해 이름이 이미 정해진 클레임들.
  - 클레임의 사용은 모두 선택적이다.

- public claim
  - 공개 클레임은 충돌이 되지 않는 이름을 가지고 있어야 함.
  - 보통 충돌을 방지하기 위해 key 값을 URI 형태로 만든다.
  - ex) `apple` (X), `'https://test.co.kr/jwt_token': true` (O)

- private claim
  - 등록된 클레임도 아니고 공개 클레임도 아님.
  - 클라이언트와 서버간에 협의하에 사용되는 클레임들.
  - key 값이 중복되서 충돌이 될 수 있으니 유의해서 사용.
  - ex) `{"username": "admin"}` (Django에서 사용되는 field 값들과 같은 경우)

---

:heavy_check_mark: <b>서명(signature)</b>

- HEADER의 인코딩 값과, PAYLOAD의 인코딩 값을 합친 후 주어진 비밀키로 해시(hash)를 생성한 값

---

<br>

#### (2) JWT의 특징

- 정보를 안전하게 JSON 객체로 전송하기 위한 간결하고 독립적인 방법
- 서로 다른 웹 프레임워크 간 데이터를 주고 받을 때 검증을 위해 사용
- JWT 용도 : `Authorization`(회원 인증), `Information Exchanges`(정보 교환)

- 세션/쿠키와 함께 모바일과 웹의 인증을 책임지는 대표 기술 중 하나.
- 세션/쿠키의 정보 전달 방식과 유사하게 사용자는 Access Token (JWT Token) 을 HTTP header 에 실어서 서버로 요청을 보냄.
- 세션/쿠키 방식과 가장 큰 차이점은 세션/쿠키는 세션 저장소에 유저의 정보를 넣지만, JWT 는 토큰 안에 유저의 정보를 넣는다.

- <b>Client 의 입장에서는 HTTP header에 세션ID와 토큰을 실어서 보낸다는 점은 동일하지만, Server 입장에서는 인증을 위해 암호화(JWT 방식) 를 하냐 혹은 별도의 저장소(세션/쿠키 방식)를 이용하느냐의 차이</b>

<br>

#### (3) JWT 사용 상황

- 회원 인증(Authorization)
  - 서버가 유저 정보에 기반한 토큰(JWT)을 발급해 유저에게 전달하고, 유저는 서버에 요청을 보낼 때마다 JWT를 포함하여 전달.
  - 서버는 세션을 유지할 필요 없이 유저의 요청정보 안에 있는 JWT 만 확인하면 된다. (서버 자원 아낄 수 있음)
- 정보 교환(Information Exchanges)
  - 정보가 서명되어 있기 때문에 정보를 보낸 사람의 정보 혹은 정보가 조작여부 확인 등이 가능

<br>

---

:spiral_notepad: <b>요약</b>

- 두 개체에서 JSON 객체를 사용하여 가볍고 자가 수용적인(self-contained; 필요한 모든 정보를 자체적으로 지님) 방식으로 정보를안정성 있게 전달.
- 세션 상태를 저장하는 것이 아니라 필요한 정보를 JWT에 저장해서 사용자가 가지고 있게 하고, 해당 JWT를 증명서처럼 사용하는 방식.(즉, 매번 주민등록증을 내는 것과 같다고 생각하면 된다.)
- JWT 장점
  - 세션/쿠키처럼 별도의 저장소 관리가 필요 없고 발급한 이후에 검증만 하면 된다.
  - 토큰을 기반으로 한 다른 인증시스템에 접근이 용이하기 때문에 확장성이 뛰어나다.
  - 모바일 환경에 적합 (쿠키와 같은 데이터로 인증할 필요가 없기 때문) (세션/쿠키 방식은 모바일 환경에서 부적합)
  - Python, JS, Ruby, Go 등 주류 프로그래밍 언어에서 대부분 지원된다.
- JWT 단점
  - 이미 발급된 JWT는 유효기간이 완료될 때까지 계속 사용하기 때문에 악용될 가능성이 있다.(한 번 발급된 토큰은 값을 수정하거나 폐기할 수 없으므로 계속 같은것을 사용하는 것이다.)
    - 그래서 이 문제는 Access Token의 유효기간(expire time) 을 짧게하고 Refresh Token 등을 이용해서 중간중간 새로운 토큰을 재발행 해줌으로써 해결할 수 있다.
  - 세션/쿠키 방식에 비해 claim 데이터(payload)가 많아진다면 JWT 토큰의 길이가 길어지기 때문에 인증 요청이 많아 질수록 네트워크의 대역폭이 낭비될 수 있다.(= 요청량이 너무 많아 네트워크에 과부하가 걸릴 수 있다는 의미)
    - API 호출 시 매 호출마다 헤더에 붙여서 전달하기 때문이다.