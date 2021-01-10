from rest_framework import serializers
from ocr.models import FileModel

# 序列化
class FileSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    def get_content(self,obj):
        strs = [i for i in obj.content]
        return strs

    class Meta:
        model = FileModel
        fields = ['name','file','content']


