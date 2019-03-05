FROM cyourai/python
MAINTAINER ctsi <ctsidr@qq.com>

# ENV 设置环境变量
ENV PATH /usr/bin;/usr/sbin:$PATH

# 下载源码
RUN rm -rf /workspaces/ && mkdir -p /workspaces && git clone https://gitee.com/SmallMi/omms.git /workspaces/omms
WORKDIR /workspaces/omms

# 修改源码中数据库连接
COPY settings.py omms
#RUN grep 'HOST' omms/settings.py

# 安装系统工具及源码依赖
RUN yum -y install sshpass && pip install -i https://pypi.douban.com/simple/  -r requirements.txt

# 数据初始化
RUN python manage.py makemigrations && python manage.py migrate && python manage.py loaddata default_user

# EXPOSE 映射端口
EXPOSE 10000

# 容器启动后时执行
CMD ["python3", "/workspaces/omms/manage.py", "runserver", "0.0.0.0:10000"]