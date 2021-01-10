from rest_framework.filters import BaseFilterBackend
class Filter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params.get('name')
        if query_params:
            query_set = queryset.filter(name=query_params)
            return query_set