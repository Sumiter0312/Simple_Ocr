
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from ocr.views import QueryView
from rest_framework.test import APIClient
from django.urls import reverse

from ocr.models import FileModel

class GetApiTest(APITestCase):
    def setUp(self):
        # 设置初始化的值
        self.factory = APIRequestFactory()
        self.view = QueryView.as_view()
        self.client = APIClient()
        self.file = FileModel.objects.create(name="haha", file='/upload/haha.jpg')

    def test_list(self):
        request = self.factory.get(
            path = reverse('query'),
            data={'name':'haha'}
        )
        response = self.view(request)

        self.assertEqual(
            response.status_code,
            200,
            '预期200状态的响应，但响应码为{}.'.format(response.status_code)
        )


class CreateUserTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {'username': 'mike', 'first_name': 'Mike', 'last_name': 'Tyson'}


    # def test_create(self):
    #     params = {
    #         'name': 'heihei',
    #         'file': 'haha1.jpeg'
    #     }
    #     response = self.client.post(self.url, params)
    #     self.assertEqual(
    #         response.status_code,
    #         201,
    #         '预期201状态的响应，但响应码为{}.'.format(response.status_code)
    #     )  # 注意post成功的状态码不是200，而是201