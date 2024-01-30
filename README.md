# [어터 - Toodat] 백엔드 과제

## 1. 환경 및 스택

- Server

  - Django==5.0.1
  - djangorestframework==3.14.
  - django-environ==0.11.2
  - gunicorn==21.2.0

  <br>

  - nginx
  - docker

<br>

- DB
  - sqlite3

<br><br>

## 2. 실행 방법

1. github 다운로드 혹은 압축파일 압축 풀기

2. `.env` 파일 생성 및 작성

   ```python
   SECRET_KEY= Django-SecretKey 만들어서 넣기
   DEBUG=False

   # admin 계정
   DJANGO_SUPERUSER_EMAIL=admin@admin.com
   DJANGO_SUPERUSER_PASSWORD=1234
   ```

3. `/server`에서 다음을 실행

   ```bash
   python manage.py collectstatic
   ```

4. `docker-compose.yml` 파일이 있는 디렉토리에서 실행

   ```bash
   docker-compose up --build
   ```

5. <http://localhost:8000/admin/> 접속

   `.env`에 적었던 `DJANGO_SUPERUSER_EMAIL`과 `DJANGO_SUPERUSER_PASSWORD`로 로그인

   Work와 Coupon을 관리하는 별도의 페이지가 없기 때문에 관리자 페이지에서 관리한다

6. <http://localhost:8000/event/> 접속

   관리자 계정으로 로그인 가능

<br><br>

## 3. API

<br>

### Account App

| METHOD | PATH             | 설명                          |
| ------ | ---------------- | ----------------------------- |
| POST   | /account/signup/ | 회원가입 API                  |
| POST   | /account/login/  | 로그인 API, Session 인증 방식 |
| POST   | /account/logout/ | 로그아웃 API                  |

<br>

### Coupon App

| METHOD | PATH         | 설명                                           |
| ------ | ------------ | ---------------------------------------------- |
| POST   | /couponuser/ | 쿠폰 발급 API, 발급에 성공하면 coupon.count -1 |

<br>

이외 작품(Work), 쿠폰(Coupon) CRUD API도 있습니다.

<br><br>

## 4. Template

<br>

### - 쿠폰 이벤트 페이지

Path : /event/

이번 프로젝트 메인 페이지, 작품 확인 및 쿠폰 발급

<br>

이벤트 진행 중

![image](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fcgdg3x%2FbtsD6uhVhr5%2FFCNDsRY0W5ZuvsK9hy2qf1%2Fimg.png)

이벤트 비활성화

![image](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcBePzU%2FbtsEdBzQEm4%2FdqaSUnrhKefc7gyAJesI2K%2Fimg.png)

<br>

### - 로그인 페이지

Path : /login-page/

![image](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FQxzez%2FbtsEco1Okfg%2F159iDZTUzCBgXd44Mkkn30%2Fimg.png)

<br>

### - 회원가입 페이지

Path : /signup-page/

![image](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbOT9au%2FbtsD8A3knFc%2FgHEYgNSfWBGrvHCuDP3Jk1%2Fimg.png)

<br><br>

## 5. Model

간단하기 때문에 ERD가 아닌 테이블로 설명하겠습니다.

<br>

### User(사용자)

| Field    | 설명            |
| -------- | --------------- |
| email    | 이메일, ID 역할 |
| password | 비밀번호        |
| is_admin | superuser 여부  |

<br>

### Work(작품)

| Field | 설명      |
| ----- | --------- |
| title | 작품 제목 |

<br>

### Coupon(쿠폰)

| Field           | 설명      |
| --------------- | --------- |
| name            | 쿠폰 이름 |
| discount_amount | 할인 금액 |
| discount_rate   | 할인 비율 |
| count           | 남은 수량 |

Work와 Coupon을 관리하는 별도의 페이지가 없기 때문에 관리자 페이지에서 관리한다

<br>

### CouponUser(발급된 쿠폰)

| Field   | 설명                                    |
| ------- | --------------------------------------- |
| coupon  | Coupon 외래키                           |
| work    | Work 외래키                             |
| user    | User 외래키                             |
| code    | 쿠폰 코드, 8자리 무작위 영어, 숫자 조합 |
| is_used | 쿠폰 사용 여부                          |

coupon, work, user 외래키 3개를 묶어서 unique 속성 부여(UniqueConstraint)

-> 같은 작품, 같은 사용자가 중복해서 쿠폰 발급 받는 것을 막기 위해

<br><br>

## 6. Test

### 실행 방법

```bash
# /server에서 실행
python manage.py test
```

### 설명

Account 관련 8개

- 회원가입 성공
- 회원가입 실패 - 중복 이메일
- 회원가입 실패 - 비밀번호와 비밀번호 확인 불일치

<br>

- 로그인 성공
- 로그인 실패 - 잘못된 비밀번호
- 로그인 실패 - 등록되지 않은 사용자

<br>

- 로그아웃 성공
- 로그아웃 실패 - 로그인 되지 않은 상태

<br>

Coupon 관련 3개

- 쿠폰 발급 성공
- 쿠폰 발급 실패 - 쿠폰 소진
- 쿠폰 발급 실패 - 이미 발행된 쿠폰
