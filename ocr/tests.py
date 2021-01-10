
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from ocr.views import QueryView,UploadView
from rest_framework.test import APIClient
from django.conf import settings

class ApiTest(APITestCase):
    def setUp(self):
        # 设置初始化的值
        self.factory = APIRequestFactory()
        self.view = QueryView.as_view()
        self.client = APIClient()

    def test_list(self):
        request = self.factory.get(
            path = 'http://127.0.0.1:9000/api/query',
            data={'name':'haha'}
        )
        print(settings.BASE_DIR)
        response = self.view(request)
        self.assertEqual(
            response.status_code,
            200,
            '预期200状态的响应，但响应码为{}.'.format(response.status_code)
        )

    def test_create(self):
        params = {
            'name': 'heihei',
            'file': settings.BASE_DIR + 'haha1.jpeg'
        }
        response = self.client.post('http://127.0.0.1:9000/api/upload' , params)
        self.assertEqual(
            response.status_code,
            201,
            '预期201状态的响应，但响应码为{}.'.format(response.status_code)
        )  # 注意post成功的状态码不是200，而是201