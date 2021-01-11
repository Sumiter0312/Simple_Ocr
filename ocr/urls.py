
from django.conf.urls import url
from ocr.views import UploadView,QueryView


urlpatterns = [
    url('upload', UploadView.as_view(),name='upload'),
    url('query', QueryView.as_view(),name='query'),
]

