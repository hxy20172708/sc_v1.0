from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # 默认每页10条
    page_size_query_param = 'page_size'  # 允许前端通过 ?page_size=xx 自定义每页数量
    max_page_size = 100  # 最大每页数量限制