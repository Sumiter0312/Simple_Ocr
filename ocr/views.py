import pytesseract

from PIL import Image
from ocr.models import FileModel
from ocr.serializer.serializer import FileSerializer
from ocr.filter.filter import Filter
from rest_framework.generics import ListAPIView,CreateAPIView


# 上传
class UploadView(CreateAPIView):
    queryset = FileModel.objects.all()
    serializer_class = FileSerializer

    def ocr(self,path):
        ''' 解析图片内容'''
        text = pytesseract.image_to_string(Image.open(path))
        return text

    def perform_create(self, serializer):
        obj = serializer.save()
        content = self.ocr(obj.file)
        obj.content = content
        obj.save()

# 查询
class QueryView(ListAPIView):
    queryset = FileModel.objects.all()
    filter_backends = [Filter]
    serializer_class = FileSerializer