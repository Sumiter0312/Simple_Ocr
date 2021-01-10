# 从仓库拉取 带有 python 3.6 的 Linux 环境
FROM python:3.6
#MAINTAINER
# 设置环境变量
ENV PYTHONUNBUFFERED 1

#清空源
RUN echo -n "" > /etc/apt/sources.list
#更换源
RUN echo "deb http://mirrors.aliyun.com/debian/ stretch main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian/ stretch main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security stretch/updates main" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian-security stretch/updates main" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib" >> /etc/apt/sources.list
#apt
RUN apt-get update && \
    apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-chi-sim -y&& \
    apt-get install default-libmysqlclient-dev python3-pip -y && \
    apt-get clean


# 在根目录新建一个code文件夹放代码
RUN mkdir /code

# 工作目录切换到code目录下
WORKDIR /code

# 升级pip
RUN pip install pip -U
# 依赖文件从宿主机加载到docker容器中
ADD requirements.txt /code/

# 安装依赖的python包
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
# 把本目录所有的文件拷到容器中
ADD . /code/
