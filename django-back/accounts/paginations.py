from rest_framework.pagination import PageNumberPagination

class UserListPagination(PageNumberPagination):
    """팔로잉/팔로워 목록 페이지네이션"""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100
