# 목차

# 📖 API 명세서

---

# 📚 도서(Book/Category) API

## 📋 요약 표

| 기능 | 메서드/엔드포인트 | 인증 | 주요 파라미터/설명 |
| --- | --- | --- | --- |
| 📖 전체 도서 목록 | `GET /api/books/` | ❌ | 카테고리, 정렬, 페이지네이션 |
| 🔍 도서 상세 | `GET /api/books/{id}/` | ❌ | 도서 ID |
| 🗂️ 카테고리 목록 | `GET /api/books/categories/` | ❌ | 없음 |
| 👍 도서 좋아요 | `POST /api/books/{bookId}/like/` | ✅ | JWT 필요, bookId |
| 📝 도서 검색 | `GET /api/books/search/` | ❌ | q, field, pub_date_from 등 |
| ✨ 자동완성 | `GET /api/books/search/suggestions/` | ❌ | q |

---

## 📖 전체 도서 목록 조회

- **URL:** `GET /api/books/`
- **인증:** ❌ 불필요
- **쿼리 파라미터:**
    - `category`: 카테고리명
    - `ordering`: pub_date, -like_count, -thread_count
    - `page`, `page_size`

| 정렬 기준 | 호출 예시 |
| --- | --- |
| 최신 출판순 | `/api/books/?ordering=pub_date` |
| 좋아요 많은순 | `/api/books/?ordering=-like_count` |
| 쓰레드 많은순 | `/api/books/?ordering=-thread_count` |

| 설명 | 예시 호출 URL |
| --- | --- |
| 문학 카테고리 도서 2페이지 | `GET /api/books/?category=문학&page=2` |
| 좋아요 순 정렬 | `GET /api/books/?ordering=-like_count` |
| 도서 상세 | `GET /api/books/123/` |
| 카테고리 목록 | `GET /api/books/categories/`  |
- **성공 예시:**
    
    ```json
    {
      "count": 1000,
      "next": "<http://api/books/?page=2>",
      "previous": null,
      "results": [
        {
          "id": 1,
          "title": "책 제목",
          "author": "저자명",
          "cover": "http://...",
          "category_name": "문학",
          "like_count": 120,
          "thread_count": 45
        }
      ]
    }
    
    ```
    
- **에러:**
    - 400: 잘못된 파라미터
    - 404: 존재하지 않는 페이지

---

## 🔍 도서 상세 조회

- **URL:** `GET /api/books/{id}/`
- **인증:** ❌ 불필요
- **성공 예시:**
    
    ```json
    {
        "id": 1,
        "title": "도서 제목",
        "description": "도서 설명",
        "isbn": "1234567890",
        "cover": "도서_표지_이미지_URL",
        "publisher": "출판사",
        "pub_date": "2024-01-01",
        "author": "저자",
        "author_info": "저자 소개",
        "author_photo": "저자_사진_URL",
        "customer_review_rank": 4.5,
        "subTitle": "부제목",
        "category_name": "카테고리명",
        "like_count": 10,
        "thread_count": 5,
        "threads": [
            {
                "id": 1,
                "title": "스레드 제목"
            }
        ],
        "is_liked": false,
        "similar_books": [
            {
                "id": 2,
                "title": "유사 도서 제목",
                "author": "저자",
                "cover": "도서_표지_이미지_URL",
                "category_name": "카테고리명",
                "similarity_score": 0.95
            }
        ]
    }
    ```
    
- **에러:**
    - 404: 도서를 찾을 수 없음

---

## 🗂️ 카테고리 목록 조회

- **URL:** `GET /api/books/categories/`

| 카테고리명 |
| --- |
| 소설/시/희곡 |
| 경제/경영 |
| 자기계발 |
| 인문/교양 |
| 취미/실용 |
| 어린이/청소년 |
| 과학 |
- **성공 예시:**
    
    ```json
    {
      "categories": [
        {"id": 1, "name": "소설/시/희곡"},
        {"id": 2, "name": "경제/경영"},
        ...
      ]
    }
    ```
    

---

## 👍 도서 좋아요

- **URL:** `POST /api/books/{bookId}/like/`
- **인증:** ✅ JWT 필요
- **응답 예시:**
    
    ```json
    {
      "liked": true,
      "like_count": 121
    }
    ```
    

---

# 📝 도서 검색 & ✨ 자동완성

## 📋 요약 표

| 기능 | 메서드/엔드포인트 | 인증 | 설명 |
| --- | --- | --- | --- |
| 🔍 검색 | `GET /api/accounts/registration/` | ❌ | 검색 기능 |
| 🏷️ 자동완성 | `GET /api/books/search/suggestions/?q=` | ❌ | 자동완성 기능 |

## 🔎 도서 검색

- **URL:** `GET /api/books/search/?q=`
- **주요 파라미터:**
    - `q`: 검색어 (필수)
    - `field`: all, title, author
    - `pub_date_from`, `pub_date_to`, `page`, `page_size`

## 📝 요청 파라미터

| 🏷️ 파라미터 | 🗂️ 타입 | ✅ 필수 | ⚙️ 기본값 | 📖 설명 |
| --- | --- | --- | --- | --- |
| 🔍 q | string | ✔️ | - | 검색어 |
| 🏷️ field | string |  | all | 검색 필드-  all: 전체-  title: 제목-  author: 저자 |
| 📅 pub_date_from | string |  | - | 출판일 시작 (YYYY-MM-DD) |
| 📅 pub_date_to | string |  | - | 출판일 종료 (YYYY-MM-DD) |
| 🔢 page | integer |  | 1 | 페이지 번호 |
| 📄 page_size | integer |  | 25 (최대 100) | 페이지당 결과 수 |

요청 예시

```json
GET /api/books/search/?q=파이썬

*(선택사항)
&field=title&pub_date_from=2023-01-01&pub_date_to=2023-12-31&page=1&page_size=25
```

- **성공 예시:**
    
    ```json
    {
      "count": 42,
      "next": "http://api/books/search/?page=2",
      "previous": null,
      "results": [
        {
          "id": 1,
          "title": "파이썬 프로그래밍",
          "author": "홍길동",
          "publisher": "좋은출판사",
          "pub_date": "2023-01-01",
          "description": "파이썬 프로그래밍 입문서",
          "category": {
            "id": 1,
            "name": "프로그래밍"
          },
          "like_count": 15,
          "thread_count": 5
        },
        ...
      ],
      "search_info": {
        "query": "파이썬",
        "tokens": ["파이썬"],
        "field": "all"
      }
    }
    ```
    
- **에러:**
    - 429: 요청 제한 초과

## ✨ 자동완성

- **URL:** `GET /api/books/search/suggestions/?q=`
- **주요 파라미터:**
    - `q`: 검색어 (필수)

## 📝 요청 파라미터

| 🏷️ 파라미터 | 🗂️ 타입 | ✅ 필수 | 📖 설명 |
| --- | --- | --- | --- |
| 🔍 q | string | ✔️ | 검색어 |

요청 예시

```json
GET /api/books/search/suggestions/?q=파이썬

*(선택사항)
Authorization: Bearer {access_token}
```

- **성공 예시:**
    
    ```json
    [
      {
        "text": "파이썬 프로그래밍",
        "type": "title",
        "popularity": 20,
        "match_type": "starts_with"
      },
      {
        "text": "파이썬 데이터 분석",
        "type": "title",
        "popularity": 15,
        "match_type": "contains"
      }
    ]
    ```
    
- **에러:**
    - 429: 요청 제한 초과
    
    ## 요청 제한
    
    | 👤 사용자 유형 | ⏱️ 요청 제한 (1분) |
    | --- | --- |
    | 🔒 인증 사용자 | 60회 |
    | 🔓 비인증 사용자 | 30회 |

---

# 👤 회원(Accounts) API

## 📋 요약 표

| 기능 | 메서드/엔드포인트 | 인증 | 설명 |
| --- | --- | --- | --- |
| 📝 회원가입 | POST `/api/accounts/registration/` | ❌ | 신규 회원 등록 |
| 🔑 로그인 | POST `/api/accounts/login/` | ❌ | JWT 발급 |
| 🚪 로그아웃 | POST `/api/accounts/logout/` | ✅ | 토큰 블랙리스트 |
| 🔄 비밀번호 변경 | POST `/api/accounts/password/change/` | ✅ | 로그인 필요 |
| 🔑 비밀번호 재설정 | POST `/api/accounts/password/reset/` | ❌ | 이메일로 재설정 |
| 🧑‍💼 프로필 조회/수정 | GET/PUT `/api/accounts/profile/` | ✅ | 본인 정보 수정시 |
| 🔍 중복검사 | GET `/api/accounts/check-username/` 등 | ❌ | 아이디/이메일/닉네임 |

---

## 📝 회원가입

- **URL:** `POST /api/accounts/registration/`
- **요청 필드:** username, email, password1, password2, profile_image, interested_categories, nickname, bio
    
    ```json
    {
      "username": "testuser",
      "email": "testuser@example.com",
      "password1": "TestPassword123!",
      "password2": "TestPassword123!",
      "profile_image": "<이미지 파일>",
      "interested_categories":[],
      "nickname": "testnickname",
      "bio": "testintroduction",
    }
    
    ```
    
    | 필드명 | 타입 | 필수 | 설명 |
    | --- | --- | --- | --- |
    | username | string | O | 사용자 이름 |
    | email | string | O | 이메일 |
    | password1 | string | O | 비밀번호 |
    | password2 | string | O | 비밀번호 확인 |
    | profile_image | file | X | 프로필 이미지 |
    | interested_categories | integer[] | X | 관심 카테고리 PK 리스트 |
    | nickname | string | O | 닉네임 설정 |
    | bio | string | O | 자기 소개 설명 |
- **성공 예시:**
    
    ```json
    {
      "user": {
    	  "pk": 1,
    	  "username": "testuser",
    	  "email": "testuser@example.com",
    	  "nickname": "test",
    	  "profile_image": "imgurl",
    	},
      "access_token": "JWT_ACCESS_TOKEN",
      "refresh_token": "JWT_REFRESH_TOKEN"
    }
    ```
    

---

## 🔑 로그인

- **URL:** `POST /api/accounts/login/`
- **요청 필드:** email, password
    
    ```json
    {
      "username": "testuser@example.com",
      "password": "TestPassword123!"
    }
    
    ```
    
- **성공 예시:**
    
    ```json
    {
      "user": {
    	  "pk": 1,
    	  "username": "testuser",
    	  "email": "testuser@example.com",
    	  "nickname": "test",
    	  "profile_image": "imgurl",
    	},
      "access_token": "JWT_ACCESS_TOKEN",
      "refresh_token": "JWT_REFRESH_TOKEN"
    }
    ```
    

---

## 🚪 로그아웃

- **URL:** `POST /api/accounts/logout/`

**로그아웃 요청**

- 클라이언트가 로그아웃할 때, 사용 중인 "refresh token"을 서버로 전송

**클라이언트 처리**

- 클라이언트에서는 access token, refresh token을 모두 삭제해야 합니다.
- **요청:** refresh 토큰 필요

```json
POST /api/accounts/logout/
Content-Type: application/json

{
  "refresh": "<REFRESH_TOKEN>"
}

```

---

## 🔄 비밀번호 변경/재설정

- **URL:**
    - 변경: `POST /api/accounts/password/change/`
    - 재설정: `POST /api/accounts/password/reset/`
- **요청 필드:** new_password1, new_password2

```json
{
  "new_password1": "NewPassword123!",
  "new_password2": "NewPassword123!"
}
```

---

## 🧑‍💼 프로필 조회/수정

- **URL:** `GET, PUT /api/accounts/profile/`
- **성공 예시:**
    
    ```json
    {
        "id": 1,
        "username": "user123",
        "nickname": "사용자닉네임",
        "profile_image": "http://localhost:8000/media/users/images/profile.jpg",
        "bio": "자기소개",
        "follower_count": 10,
        "following_count": 5,
        "is_following": false,
        "interested_categories": [
            {
                "id": 1,
                "name": "소설"
            }
            // 전체 관심 카테고리
        ]
    }
    ```
    

---

## 🔍 중복검사

- **URL:**
    - `/api/accounts/check-username/?username=...`
    - `/api/accounts/check-email/?email=...`
    - `/api/accounts/check-nickname/?nickname=...`
- **응답:**

```json
{ "exists": true } 
```

---

# 🤝 팔로우/프로필 관련 API

## 📋 요약 표

| 기능 | 메서드/엔드포인트 | 인증 | 설명 |
| --- | --- | --- | --- |
| ➕ 팔로우/언팔로우 | POST `/api/accounts/{user_id}/follow/` | ✅ | 팔로우 토글 |
| 👥 팔로잉 목록 | GET `/api/accounts/{user_id}/following/` | ❌ | 팔로우하는 사용자 목록 |
| 👤 팔로워 목록 | GET `/api/accounts/{user_id}/followers/` | ❌ | 나를 팔로우하는 목록 |
| 🧑‍💼 프로필 상세 | GET `/api/accounts/{user_id}/profile/` | ❌ | 타인 프로필 |
| 👍 좋아요 도서 | GET `/api/accounts/{user_id}/liked-books/` | ❌ | 좋아요한 도서 |

---

## ➕ 팔로우/언팔로우

- URL : POST `/api/accounts/{user_id}/follow/`
- 인증 필요 (JWT)
- 응답 200 OK

```json
{
    "id": 2,
    "is_following": true,
    "follower_count": 5,
    "following_count": 3
}
```

## 👥 팔로잉 목록

- URL : `GET /api/accounts/{user_id}/following/`
- 권한 : all

쿼리 파라미터

| 파라미터 | 기본값 | 최대값 | 설명 |
| --- | --- | --- | --- |
| page | 1 | - | 페이지 번호 |
| page_size | 50 | 100 | 페이지당 항목 수 |

응답 (200 OK)

```json
{
    "count": 42,
    "next": "http://api/accounts/{user_id}/following/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "nickname": "사용자1",
            "profile_image": "http://...",
            "bio": "자기소개",
            "is_following": true
        }
    ]
}
```

## 👤 팔로워 목록

- URL : `GET /api/accounts/{user_id}/followers/`
- 권한 : all

쿼리 파라미터

| 파라미터 | 기본값 | 최대값 | 설명 |
| --- | --- | --- | --- |
| page | 1 | - | 페이지 번호 |
| page_size | 50 | 100 | 페이지당 항목 수 |

응답 (200 OK)

```json
{
    "count": 42,
    "next": "http://api/accounts/{user_id}/followers/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "nickname": "사용자1",
            "profile_image": "http://...",
            "bio": "자기소개",
            "is_following": true
        }
    ]
}
```

## 🧑‍💼 프로필 상세

- URL : `GET /api/accounts/{user_id}/profile/`
- 권한 : all

응답 (200 OK)

```json
{
    "id": 1,
    "username": "user1",
    "nickname": "사용자1",
    "profile_image": "http://...",
    "bio": "자기소개",
    "follower_count": 42,
    "following_count": 38,
    "is_following": true,
    "interested_categories": [
        {
            "id": 1,
            "name": "소설"
        }
        // 전체 관심 카테고리
    ]
}
```

- URL : `GET /api/accounts/{user_id}/liked-books/`
- 권한 : all

쿼리 파라미터

| 파라미터 | 기본값 | 최대값 | 설명 |
| --- | --- | --- | --- |
| page | 1 | - | 페이지 번호 |
| page_size | 50 | 100 | 페이지당 항목 수 |

응답 (200 OK)

```json
{
    "count": 42,
    "next": "http://api/accounts/{user_id}/liked-books/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "도서제목",
            "author": "저자",
            "cover": "http://..."
        }
    ]
}
```

## ⚠️ 오류 코드

| 코드 | 설명 |
| --- | --- |
| 400 | 자기 자신 팔로우 불가 |
| 401 | 인증 실패 |
| 404 | 사용자를 찾을 수 없음 |
- **공통:** 페이지네이션, JWT 필요시 명시, 이미지 URL 절대경로, JSON 응답

---

# 🧵 쓰레드(Threads) API

## 📋 요약 표

| 기능 | 메서드/엔드포인트 | 인증 | 설명 |
| --- | --- | --- | --- |
| ➕ 쓰레드 생성 | POST `/api/threads/books/{book_pk}/create/` | ✅ | 도서에 새 쓰레드 작성 |
| 🔍 상세 조회 | GET `/api/threads/{pk}/` | ❌ | 쓰레드 상세 |
| ✏️ 수정/삭제 | PUT/DELETE `/api/threads/{pk}/update-delete/` | ✅ | 본인만 가능 |
| 👍 좋아요 | POST `/api/threads/{pk}/like/` | ✅ | 쓰레드 좋아요 |
| 📃 전체 목록 | GET `/api/threads/` | ❌ | 전체 쓰레드 |
| 🏆 인기 쓰레드 | GET `/api/threads/popular/` | ❌ | 상위 5개, 좋아요순 |
| 👥 팔로잉 쓰레드 | GET `/api/threads/following/` | ✅ | 팔로잉 최신 5개 |

## ➕ 쓰레드 생성

`POST /api/threads/books/{book_pk}/create/`

요청 예시

```json
textHeaders:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Body:
{
  "title": "서평 제목",
  "content": "상세 내용",
  "rating": 4
}
```

응답 (201 Created)

```json
{
    "id": 3,
    "title": "test update",
    "content": "test comment34",
    "rating": 4,
    "created_at": "2025-05-25T10:38:11.067039Z",
    "updated_at": "2025-05-25T10:42:14.458332Z",
    "user": {
        "id": 2,
        "username": "tester1",
        "profile_image": null,
        "nickname": "tester",
        "bio": "test hi"
    },
    "book": {
        "id": 1,
        "title": "소년이 온다",
        "author": "한강",
        "cover": "https://image.aladin.co.kr/product/4086/97/cover500/8936434128_2.jpg"
    },
    "comments": [],
    "is_liked": false,
    "like_count": 0
}
```

---

## 🔍 상세 조회

`GET /api/threads/{pk}/`

요청 예시

```json
textHeaders: None
```

성공 응답 (200 OK)

```json
{
    "id": 3,
    "title": "test update",
    "content": "test comment34",
    "rating": 4,
    "created_at": "2025-05-25T10:38:11.067039Z",
    "updated_at": "2025-05-25T10:42:14.458332Z",
    "user": {
        "id": 2,
        "username": "tester1",
        "profile_image": null,
        "nickname": "tester",
        "bio": "test hi"
    },
    "book": {
        "id": 1,
        "title": "소년이 온다",
        "author": "한강",
        "cover": "https://image.aladin.co.kr/product/4086/97/cover500/8936434128_2.jpg"
    },
    "comments": [],
    "is_liked": false,
    "is_followed": false,
    "like_count": 0
}
```

---

## **스레드 수정**

`PUT /api/threads/{pk}/update-delete/`

요청 예시

```json
textHeaders:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Body:
{
  "title": "수정된 제목",
  "content": "업데이트 내용"
}
```

성공 응답 (200 OK)

```json
{
  "id": 12,
  "title": "수정된 제목",
  "content": "업데이트 내용",
  ...
}
```

---

## **스레드 삭제**

`DELETE /api/threads/{pk}/update-delete/`

요청 예시

```json
textHeaders:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

성공 응답 (204 No Content)

```json
{
  "message": "성공적으로 삭제하였습니다"
}
```

---

## 👍 좋아요

`POST /api/threads/{pk}/like/`

요청 예시

```json
textHeaders:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

성공 응답 (204 No Content)

```json
{
    "liked": true,
    "like_count": 1
}
```

## 📃 전체 목록

`GET /api/threads/`

요청 파라미터

| 🏷️ 파라미터 | 🗂️ 타입 | ✅ 필수 | ⚙️ 기본값 | 📖 설명 |
| --- | --- | --- | --- | --- |
| page | integer |  | 1 | 페이지 번호 |
| page_size | integer |  | 20 (최대 100) | 페이지당 항목 수 |

---

응답 예시

```json
{
    "count": 42,
    "next": "http://api/threads/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "쓰레드 제목",
            "created_at": "2025-05-25T14:30:00Z",
            "user": {
                "id": 1,
                "username": "사용자명",
                "profile_image": "프로필이미지URL",
                "nickname": "닉네임",
                "bio": "자기소개"
            },
            "book": {
                "id": 1,
                "title": "도서제목",
                "author": "저자",
                "cover": "표지이미지URL"
            },
            "like_count": 5,
            "comment_count": 3
        }
        *// ... 추가 쓰레드*
    ]
}
```

---

응답 필드 설명

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| count | integer | 전체 쓰레드 수 |
| next | string | 다음 페이지 URL |
| previous | string | 이전 페이지 URL |
| results | array | 쓰레드 객체 배열 |
| └ id | integer | 쓰레드 ID |
| └ title | string | 쓰레드 제목 |
| └ created_at | string | 생성일시 (ISO 8601) |
| └ user | object | 작성자 정보 |
| └ book | object | 관련 도서 정보 |
| └ like_count | integer | 좋아요 수 |
| └ comment_count | integer | 댓글 수 |

## 🏆 인기 쓰레드

`GET /api/threads/popular/`

응답 예시 

```json
[
    {
        "id": 1,
        "title": "스레드 제목",
        "created_at": "2025-05-26T10:00:00Z",
        "user": {
            "id": 1,
            "username": "사용자아이디",
            "nickname": "닉네임",
            "profile_image": "프로필이미지URL",
            "bio": "자기소개"
        },
        "book": {
            "id": 1,
            "title": "도서제목",
            "author": "저자",
            "cover": "표지이미지URL"
        },
        "like_count": 42,
        "comment_count": 5
    }
    *// ... 최대 5개 항목*
]
```

응답 필드 설명

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | Integer | 쓰레드 고유 ID |
| title | String | 쓰레드 제목 |
| created_at | String | 생성 일시 (ISO 8601) |
| user | Object | 작성자 정보 |
| └ id | Integer | 작성자 ID |
| └ username | String | 작성자 아이디 |
| └ nickname | String | 작성자 닉네임 |
| └ profile_image | String | 프로필 이미지 URL |
| └ bio | String | 자기소개 |
| book | Object | 도서 정보 |
| └ id | Integer | 도서 ID |
| └ title | String | 도서 제목 |
| └ author | String | 저자 |
| └ cover | String | 도서 표지 이미지 URL |
| like_count | Integer | 좋아요 수 |
| comment_count | Integer | 댓글 수 |

## 👥 팔로잉 쓰레드

URL : GET /api/threads/following/

- **인증**: 필수 (Token Authentication)
- **권한**: 로그인한 사용자만 접근 가능

응답 예시

```json
[
  {
    "id": 1,
    "title": "쓰레드 제목",
    "created_at": "2024-01-01T12:00:00Z",
    "user": {
        "id": 2,
        "username": "user123",
        "profile_image": "http://example.com/media/users/images/profile.jpg",
        "nickname": "닉네임",
        "bio": "자기소개"
    },
    "book": {
        "id": 1,
        "title": "책제목",
        "author": "저자",
        "cover": "http://example.com/media/books/cover.jpg"
    },
    "like_count": 5,
    "comment_count": 3
  },
  // ... 최대 5개의 쓰레드
]
```

---

- **공통:** 페이지네이션, select_related 최적화, 캐싱, JSON 응답

---

# 💬 댓글(Comments) API

## 📋 요약 표

| 기능 | 메서드/엔드포인트 | 인증 | 설명 |
| --- | --- | --- | --- |
| ➕ 댓글 생성 | POST `/api/threads/{thread_pk}/comments/create/` | ✅ | 쓰레드에 댓글 작성 |
| 🔍 댓글 조회 | GET `/api/threads/comments/{comment_pk}/` | ✅ | 댓글 상세 |
| ✏️ 수정/삭제 | PUT/DELETE `/api/threads/comments/{comment_pk}/` | ✅ | 본인 댓글만 가능 |

## 1️⃣ **댓글 생성**

`POST /api/threads/{thread_pk}/comments/create/`

요청 예시

```json
textHeaders:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Body:
{
  "content": "훌륭한 서평이네요!"
}
```

성공 응답 (201 Created)

```json
{
  "id": 23,
  "content": "훌륭한 서평이네요!",
  "created_at": "2025-05-25T03:00:00Z",
  "user": {
    "id": 5,
    "username": "booklover",
    "profile_image": "/media/profiles/booklover.jpg"
  }
}
```

---

## 2️⃣ **댓글 조회**

`GET /api/threads/comments/{comment_pk}/`

요청 예시

```json
textHeaders:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

성공 응답 (200 OK)

```json
{
  "id": 23,
  "content": "훌륭한 서평이네요!",
  "created_at": "2025-05-25T03:00:00Z",
  "user": { ... }
}
```

---

## 3️⃣ **댓글 수정**

`PUT /api/threads/comments/{comment_pk}/`

요청 예시

```json
textHeaders:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Body:
{
  "content": "수정된 댓글 내용"
}
```

성공 응답 (200 OK)

```json
{
  "id": 23,
  "content": "수정된 댓글 내용",
  ...
}
```

---

## 4️⃣ **댓글 삭제**

`DELETE /api/threads/comments/{comment_pk}/`

요청 예시

```json
textHeaders:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

성공 응답 (204 No Content)

```json
{
  "message": "성공적으로 삭제되었습니다"
}
```

---

- **공통:** 본인만 수정/삭제, 인증 필요, JSON 응답

---

# 🖥️AI기반 추천 도서

`GET /api/accounts/recommended-books/`

- 로그인한 사용자의 메타데이터 임베딩 값을 통해 코사인 유사도가 가장 높은 5권의 책 추천

---

# ⚠️ 공통 정책 및 참고

- **인증:** JWT 필요시 `Authorization: Bearer <token>`
- **상태 코드:** 200, 201, 204, 400, 401, 403, 404, 405, 429 등
- **페이지네이션:** 대부분 `page`, `page_size` 지원(최대 100)
- **응답 포맷:** JSON, 이미지/커버 URL은 절대경로
- **캐싱:** 일부 API(예: 자동완성, 쓰레드 목록) 1~5분 캐싱 적용