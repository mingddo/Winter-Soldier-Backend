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

    

11. `pip freeze > requirements.txt`

# 의문

## 왜 rest_framework를 사용하는가?

- front에서 요청을 보냈을 때, 

  서버에 있는 DB에서 원하는 데이터를 JSON 형식으로 보내는 것을 편리하게 하기 위해 사용



