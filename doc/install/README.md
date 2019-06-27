## Docker部署
```
感谢留言区的小伙伴提供的Dockerfile
注意：使用Docker部署可能会导致某些功能不可用，可以尝试解决或在码云提交Issues
```

### Docker安装：
```
1、Docker要求CentOS系统的内核版本高于3.10，通过uname -r命令查看你当前的内核版本
uname -r

2、使用 root 权限登录Centos。确保yum包更新到最新。
yum update

3、卸载旧版本(如果安装过旧版本的话)
yum remove docker  docker-common docker-selinux docker-engine

4、安装需要的软件包，yum-util 提供yum-config-manager功能，另外两个是devicemapper驱动依赖的
yum install -y yum-utils device-mapper-persistent-data lvm2

5、设置yum源
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

6、安装docker
yum install docker-ce  #由于repo中默认只开启stable仓库，故这里安装的是最新稳定版

7、启动并加入开机启动
systemctl start docker
systemctl enable docker

8、验证安装是否成功(有client和service两部分表示docker安装启动都成功了)
```
### 构建镜像并启动：
```
1、进入到omms/omms目录，即settings.py文件所在目录
2、修改settings.py中数据库地址、账户、密码等信息
3、构建镜像
docker build -t omms:v1 .
4、启动omms程序
docker run -d --name omms -p 10000:10000 omms:v1
5、访问docker所在机器的10000端口即可，账密admin/admin
```

## Linux部署
### 版本须知：
Python版本：3.6.2

Django版本：2.1.7

MySQL版本：5.6.43

### Python升级
```

升级链接：https://www.cnblogs.com/tssc/p/7762998.html

注意：python升级编译命令需加上以下参数来支持ssl模块
./configure --enable-optimizations --with-ssl
```

### 创建虚拟环境

```
pip3 install --upgrade pip
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
```

### 安装依赖

```
git clone https://gitee.com/SmallMi/omms.git
cd omms
pip install -i https://pypi.douban.com/simple/  -r requirements.txt

# 如果中间出现mysql_conf这类错误需要执行以下命令：
yum -y install mysql-devel python-devel

# 如果安装python-ldap出现错误，需要执行以下命令：
yum -y install openldap-devel
```

### 修改配置


MySQL配置修改omms/settings.py:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'omms',
        'USER': 'root',
        'PASSWORD': 'xxxx',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

开启LDAP认证:
```
开启LDAP设置为True，并配置ladp的地址和端口号等信息
AUTH_LDAP = False
```

修改通知邮箱settings.py:

```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = 'service.smallmi.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'admin@service.smallmi.com'
EMAIL_HOST_PASSWORD = 'xxx'
DEFAULT_FROM_EMAIL = 'smallmi <admin@service.smallmi.com>'

```

### 初始化数据
```
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata default_user

```

### 登录

开发模式下启动（单线程）
```
python manage.py runserver 192.168.22.22:8000
http://192.168.22.22:8000
admin admin
```

使用uWSGI方式启动（支持多线程）:
```
如果使用uwsgi方式启动，需将DEBUG设置为False
DEBUG = False

进入到项目根目录运行以下命令：
uwsgi uwsgi.ini

注意：如果需要后台运行，需要修改uwsig.ini配置，去掉注释即可
;daemonize = /oriental/logs/ccms_uwsgi.log
```