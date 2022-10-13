from rest_framework.pagination import PageNumberPagination


class PageNumberCustomPaginator(PageNumberPagination):
    '''Класс для паджинации.'''

    page_size_query_param = 'limit'
