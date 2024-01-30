# [어터 - Toodat] 백엔드 과제

## 1. 환경 및 스택

- Server

  - Django==5.0.1
  - djangorestframework==3.14.
  - django-environ==0.11.2
  - django-cors-headers==4.3.1
  - gunicorn==21.2.0

<br>

- DB
  - sqlite3

<br><br>

## 2. API

<br>

### Account App

| METHOD | PATH             | 설명                          |
| ------ | ---------------- | ----------------------------- |
| POST   | /account/signup/ | 회원가입 API                  |
| POST   | /account/login/  | 로그인 API, Session 인증 방식 |
| POST   | /account/logout/ | 로그아웃 API                  |

<br>

### Coupon App

| METHOD | PATH         | 설명          |
| ------ | ------------ | ------------- |
| POST   | /couponuser/ | 쿠폰 발급 API |

<br>

이외 작품(Work), 쿠폰(Coupon) CRUD API도 있습니다.

<br><br>

## 3. Template

<br>

### /event/

쿠폰 이벤트 페이지, 이번 프로젝트 메인 페이지, 작품 확인 및 쿠폰 발급



| PATH          | 설명            |
| ------------- | --------------- |
| /event/       |                 |
| /login-page/  | 로그인 페이지   |
| /signup-page/ | 회원가입 페이지 |

<br><br>

## 4. Model

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

<br><br>

## 5. Test
