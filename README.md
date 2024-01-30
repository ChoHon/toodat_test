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

2. `/server`에 `.env` 파일 생성 및 작성

   ```python
   SECRET_KEY= Django-SecretKey 만들어서 넣기
   DEBUG=False
   ALLOWED_HOSTS=localhost,

   # admin 계정
   DJANGO_SUPERUSER_EMAIL=admin@admin.com
   DJANGO_SUPERUSER_PASSWORD=1234
   ```

3. `docker-compose.yml` 파일이 있는 디렉토리에서 실행

   ```bash
   docker-compose up --build
   ```

4. <http://localhost/admin/> 접속

   `.env`에 적었던 `DJANGO_SUPERUSER_EMAIL`과 `DJANGO_SUPERUSER_PASSWORD`로 로그인

   Work와 Coupon을 관리하는 별도의 페이지가 없기 때문에 관리자 페이지에서 관리한다

5. <http://localhost/event/> 접속

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

### Work App

| METHOD | PATH   | 설명                            |
| ------ | ------ | ------------------------------- |
| GET    | /work/ | Work(작품) 전체 리스트 Read API |

<br>

### Coupon App

| METHOD | PATH         | 설명                                           |
| ------ | ------------ | ---------------------------------------------- |
| POST   | /couponuser/ | 쿠폰 발급 API, 발급에 성공하면 coupon.count -1 |

<br><br>

## 4. Template

<br>

### - 쿠폰 이벤트 페이지

Path : /event/

이번 프로젝트 메인 페이지, 작품 확인 및 쿠폰 발급

ID가 1인 Coupon을 대상으로 페이지 구성

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

<br><br>

## 7. 순간적으로 증가하는 트래픽 대응

트래픽이 순간적으로 증가할 때 고려해야하는 것은 2가지이다.

첫번째는 증가하는 트래픽에 따른 부하를 감당할 수 있어야한다는 것이다.

두번째는 많은 요청을 처리하는 과정에서 동시성이 보장되어야 한다는 것이다.

<br>

### 부하 감당

순간적으로 높은 부하를 감당하기 위해서 Scale up 혹은 Scale out 방법을 고민할 수 있다

Scale up은 서버의 성능 자체를 늘려서 부하를 감당하는 방식이다

Scale out은 여러 일을 동시에 처리할 수 있도록해서 부하를 분산시키는 방식이다

여러 일 을 동시에 처리하기 위해서는 하나의 일을 처리하는 Worker의 갯수가 많아져야하고

주로 멀티프로세싱이나 서버의 갯수를 증가시키는 방식이 선택된다

그리고 Worker들 앞에서 들어오는 일들을 적절한 Worker에게 분배하는 것이 로드 밸런싱이다

해당 프로젝트의 경우 Nginx, Gunicorn의 설정을 통해 CPU를 최대한 활용하는 방식으로 부하 분산을 하려고 했다

Django 내에서 가능한 해결 방식이 아니기 때문에 과제에서 요구한 방법이 아닌 것 같다

<br>

Scale up이나 Scale out이 아니라 일 자체의 부하는 줄이는 방식도 있다

대표적인 방법이 부하를 주는 곳에 캐싱을 적용하는 방법이다

캐싱하기 위해서는 Read와 Write 빈도 등에 따라 적절한 전략을 선택해야하고 잘못 선택하면 오히려 성능이 저하될 수도 있다

보통 캐싱은 Redis와 같은 별도의 서버를 통해 동작한다

해당 프로젝트에서는 Work(작품) 리스트가 캐싱하기 가장 좋은 부분이라고 생각했지만 구현하지는 못했다

<br>

### 동시성 보장

부하 감당을 위해서 Scale out을 하면 여러 일이 동시에 진행되고 동시성 문제가 생길 수 있다

동시성 문제는 RDBMS에서 트랜잭션 격리수준을 조정하거나 Row Lock을 통해 해결할 수 있다

동시성에 대한 너무 엄격한 해결책은 동시 처리 성능이 떨어져서 결국 부하와 레이턴시가 증가한다

결국 성능과 동시성 사이에서 밸런스를 맞춰야 한다

해당 프로젝트의 경우 트래픽이 증가할 때 동시성 문제가 생길만한 부분은 쿠폰 발행하면서 쿠폰의 잔량을 하나 줄이는 부분이다

```python
with transaction.atomic():
   coupon = Coupon.objects.select_for_update().get(id=request.data['coupon'])
   self.perform_create(serializer)
   coupon.count -= 1
   coupon.save()
```

`transaction.atomic()`을 사용해서 해당 부분을 하나의 트랜잭션으로 만들었다

그리고 `select_for_update()`를 사용해서 대상 쿠폰에 Row Lock을 걸어서 동시성 보장하고자 했다
