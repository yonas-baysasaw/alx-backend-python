from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response

import math

class LargeResultPagination(PageNumberPagination):
    
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 50
    
    def get_paginated_response(self, data):
        return Response({
            "count":self.page.paginator.count,
            "page_size": self.get_page_size(self.request),
            "current_page":self.page.number,
            "page_count":math.ceil(self.page.paginator.count/self.get_page_size(self.request)),
            "next": self.get_next_link(),
            "previous":self.get_previous_link(),
            "result" : data
            
        })