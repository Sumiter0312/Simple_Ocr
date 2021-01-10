# *前置步骤*

```python
Step-1.本机需要安装好 docker + docker-compose
Step-2.开启docker服务
Step-3.确保宿主机的 3306端口 以及 3031端口未被占用
Step-4.本机docker更换国内镜像源加速.
  "registry-mirrors": [
      "http://f1361db2.m.daocloud.io",
      "https://docker.mirrors.ustc.edu.cn"
    ]
```

# *Usage*

```python
1.进入Ocr_demo项目目录
2.执行docker-compose up
3.浏览器输入 http://0.0.0.0:3031/api/update  or  http://0.0.0.0:3031/api/query？name=xxx 进入api页面
# 本机运行docker 直接访问 http://0.0.0.0:3031/api/
# 局域网内其他主机运行docker http://主机ip:3031/api/
```

# *技术栈*

- `框架 : Django 3 + Restframework(API)`
- `DB : Mysql`
- `文字识别 : pytesseract`
- `开发环境 : Mac/linux + docker-compose`

# *Api*

## *接口说明*

### *Upload接口*

- `POST请求地址 :  http://x.x.x.x:3031/upload/`

  ```python
  form_data:
          name:上传的图片名称
          file:上传文件
  ```

- `return`

  ```python
  {
    "name": "haha",
    "file": "http://192.168.1.6:3031/upload/haha.jpeg",
    "content":[ 'Letter1', 'Letter2'...]  #解析出来的字母列表
  }
  ```

### *Query接口*

- `GET请求地址 : `

  ```python
  http://0.0.0.0:3031/api/query?name='上传图片时填写的图片名称'
  ```

- `return`

  ```python
  {
    "name": "haha",
    "file": "http://192.168.1.6:3031/upload/haha.jpeg",
    "content":[ 'Letter1', 'Letter2'...]  #目标数据
  }
  ```

## *设计方案*

```python
根据需求,项目分为上传和查询两个接口
1.upload api : 将 img_name & 文件路径 & 文件解析过后的letters 写入mysql
2.query api : 通过图片name查询 mysql中保存 的letters

# 结合DRF框架业务代码总计不超过40行(except dockerfile & docker-compose)
```



### *Models*

```python
class FileModel(models.Model):
    name = models.CharField(max_length=50,unique=True,verbose_name="图片名称(查询时可用)")
    file = models.FileField(upload_to='upload',verbose_name='请选择上传的图片')  #上传的图片保存在 当前目录upload/
    content = models.CharField(max_length=200, verbose_name="解析后的字母")
```

### *Views*

- `视图采用Django-restframework框架 CreateAPIView && ListAPIView, restframework自带接口调试页面`

#### *UploadView*

```python
#序列化
class FileSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    
    def get_content(self,obj):
      """
      	自定义方法返回目标数据 {"content": [ 'Letter1', 'Letter2'...]}
      """
        strs = [i for i in obj.content]
        return strs

    class Meta:
        model = FileModel
        #返回前端的字段
        fields = ['name','file','content'] 


#上传图片视图
class UploadView(CreateAPIView):
    queryset = FileModel.objects.all()  #获取查询集
    serializer_class = FileSerializer   #序列化

    def ocr(self,path):
        ''' 调用pytesseract解析图片中字母'''
        text = pytesseract.image_to_string(Image.open(path))
        return text

    def perform_create(self, serializer):
      """
      	这里需要重写父类方法，因为目前只有 name && file 两个字段数据,content(目标数据)为空
      	serializer.save()方法保存之后,图片才会被上传到本项目下的 => upload/xxx.png
      	通过 pytesseract库解析 upload/xxx.png 获得content字段值,然后赋给对象并且保存
      """
        obj = serializer.save()
        content = self.ocr(obj.file)
        obj.content = content
        obj.save()

 


#执行流程
#CreateAPIView.create为入口,源码主要执行
def create(self, request, *args, **kwargs):
  			#将post数据传入serializer中
        serializer = self.get_serializer(data=request.data)
      	#验证数据的合法性
        serializer.is_valid(raise_exception=True)
        #保存数据
        self.perform_create(serializer)
        #将验证后合法的数据返回给前端
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
```



#### *QueryView*

```python
#filter过滤
from rest_framework.filters import BaseFilterBackend
class Filter(BaseFilterBackend):
  """
  	返回过滤后的queryset or none ！
  """
    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params.get('name') #获取查询参数
        if query_params:
            query_set = queryset.filter(name=query_params) #根据参数再次过滤
            return query_set
# 查询
class QueryView(ListAPIView):
    queryset = FileModel.objects.all()
    filter_backends = [Filter]
    serializer_class = FileSerializer 


    
    
#执行流程
#ListAPIView.list方法入口,源码主要执行
def list(self, request, *args, **kwargs):
  	#1.获取queryset = > 根据filter过滤条件
    queryset = self.filter_queryset(self.get_queryset())
    ...
    #2.将queryset传入 serializer验证
    serializer = self.get_serializer(queryset, many=True)
    #3.返回数据
    return Response(serializer.data)
```







