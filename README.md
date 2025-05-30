# 🖥️SSAFY Final Project

부울경 1반<br>
박진호, 박희재

### 🔗[Notion WorkSpace](https://periodic-nova-973.notion.site/Final-PJT-1fbb41fd54f48009b039e537314ca5dd?pvs=4)


### 🔗[Git hub](https://github.com/PPPP98/BookRecommendationPJT.git)

<hr>

>박진호 : 장고 백엔드 / 명세서 작성 / ERD 설계 / Vue front / <br>

>박희재 :  뷰 프론트 / 명세서 작성 / 기타 디자인

## 🎯 기획 목표
- 실시간 도서 정보 제공

- 도서 토론을 위한 쓰레드 CRUD 기능

- 임베딩 벡터 기반 맞춤형 도서 추천

- 근처 도서관/대여소 위치 정보 제공

- 소셜 로그인 지원

## ERD 설계

![image](/documents/ERD.png)

## 핵심 기능 소개
1. 도서 추천 알고리즘
> - OpenAI의 embedding모델 text-embedding-3-small을 사용하여 도서 메타 데이터 (title, author, desc, category)를 벡터화 하였습니다.
> - 사용자의 메타 데이터 (interested_categories, bio, liked_book)를 벡터화 하였습니다.
> - Faiss(Facebook AI Similarity Search)라이브러리 사용. 해당 라이브러리는 대용량 벡터 데이터의 유사도 검색에 최적화된 라이브러리
> - 사용자가 자기소개나 관심 장르를 변경하거나 책을 좋아요 한다면 메타데이터의 벡터값이 변경되어 더 유사한 도서를 추천해주도록 구현하였습니다.

2. 실시간 검색어 자동 완성
> - 검색어 전처리 db_index=true를 통해 제목과 작가 정보 인덱스를 만들어 빠르게 검색할 수 있도록 하였습니다.
> - 캐싱을 사용해 5분간 동일 검색어를 입력할 경우 캐싱된 데이터를 response하도록 구현하였습니다.

3. 쓰레드 CRUD
> - 도서 정보에 대해 작성할 수 있는 쓰레드 CRUD 구현

4. 사용자간 팔로우 팔로잉 및 내 서재
> - 사용자간 팔로잉 팔로우 가능
> - 내 서재에서 좋아요 한 책들과 팔로우 팔로잉 관리 가능

## 프로젝트를 진행하면서
최종 프로젝트를 하면서 문서화에 집중해야겠다는 생각을 가지고 시작하였습니다. 요구사항 명세서부터 시작하여 기능 명세서, API 명세서 등 하루를 꼬박 사용하면서 문서화 작업을 하였습니다. 그러다 보니 생각보다 시간이 부족해져 원했던 기능을 전부 구현하지 못했습니다.

[문서화를 위한 노력](https://periodic-nova-973.notion.site/Final-PJT-1fbb41fd54f48009b039e537314ca5dd?pvs=4)

[documents](/documents/)


백엔드 API 개발이 26일에 먼저 끝나 프론트엔드 개발에도 같이 참여하였는데, 디자인 컨벤션을 정하지 않고 개발을 하다 보니 문제가 많이 발생하였습니다. 계속해서 코드를 수정하게 되어 시간이 많이 소요되었고, 완벽한 결과물을 내지는 못하였습니다.

프론트엔드 개발에 시간이 오래 소요되어 백엔드 개발자가 프론트 작업에 함께 참여하게 되었으나, 프로젝트 전체에 대한 이해가 부족해 완벽한 결과물을 만들지 못하였습니다.

### 프로젝트가 끝난 후
추가하고 싶었던 기능들을 더 발전시켜서 추가할 예정입니다. 코드 리팩토링을 통해 개선 작업을 이룰 것이고, 여기서 끝내지 않고 다른 기술들과 기능들을 추가로 학습하여 더욱 발전시켜 볼 생각입니다.

프론트엔드 개발을 진행하면서 백엔드의 구조와 동작 원리를 충분히 이해하는 것이 중요하다는 점을 깨달았습니다. 특히 API 연동 과정에서 백엔드에 대한 이해가 부족하면 오류 발생 시 원인 파악과 해결이 어렵다는 것을 경험했습니다. 앞으로는 미완성된 기능을 보완하고, 백엔드와의 연동에 대한 이해도를 높여 프로젝트를 더욱 발전시킬 계획입니다.