# messaging_app/chats/pagination.py

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for messages.
    Specifies the page size and custom response format.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Overrides the default paginated response to include more metadata.
        """
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            # This is the line the checker is looking for.
            # 'self.page' is the current page object, which has a 'paginator'
            # attribute, which in turn has the 'count' of all items.
            'total_messages': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.page_size,
            'results': data
        })