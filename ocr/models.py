
from django.db import models

class FileModel(models.Model):
    name = models.CharField(max_length=50,unique=True,verbose_name="图片名称(查询时可用)")
    file = models.FileField(upload_to='upload',verbose_name='请选择上传的图片')
    content = models.CharField(max_length=200, verbose_name="解析后的字母")

