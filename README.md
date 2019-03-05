OMMS 运维监控管理系统
=======================

[![Python Version](https://img.shields.io/badge/Python--3.6.2-paasing-green.svg)](https://img.shields.io/badge/Python--3.6.2-paasing-green.svg)
[![Django Version](https://img.shields.io/badge/Django--2.1.7-paasing-green.svg)](https://img.shields.io/badge/Django--2.1.7-paasing-green.svg)

项目作者：小瓶盖

> OMMS现有功能: （扫描下方微信邀请入群，请备注姓名@公司）

- Dashboard
- 资产管理
- 应用管理
- 运维工具
- 监控管理
- 权限管理

特别说明：本系统是基于开源运维管理系统PFMS进行的二次开发，感谢该作者的开源精神。OMMS是在此基础上增加了监控管理，优化了其他模块功能。

运维工具功能中K8S安装目前还是验证测试环境，用于生产部署需谨慎。此安装脚本是采用一位大神所写的playbook，GitHub：[https://github.com/gjmzj/kubeasz.git]


## 界面预览：
![资产页面](https://gitee.com/uploads/images/2017/1103/163547_29bfb40b_1521920.png "1.png")

![资产组页面](https://gitee.com/uploads/images/2017/1103/163605_b696ec54_1521920.png "2.png")

![登录用户页面](https://gitee.com/uploads/images/2017/1103/163642_d9e5b600_1521920.png "3.png")

![监控页面1](https://images.gitee.com/uploads/images/2019/0129/164022_60343dd9_1521920.jpeg)

![监控页面2](https://images.gitee.com/uploads/images/2019/0129/164112_7780e34b_1521920.png)

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

```
python manage.py runserver 192.168.22.22:8000
http://192.168.22.22:8000
admin admin
```

沟通交流
=========================
写Python代码是我的业余爱好，单纯运维才是主业，无论哪个都欢迎交流。  
人脉也是一项重要能力，请备注姓名@公司，谢谢：）

<img src="https://images.gitee.com/uploads/images/2019/0129/172228_8aabccd0_1521920.jpeg" width="244" height="314" alt="小瓶盖微信" align=left />


<br><br><br><br><br><br><br><br><br><br><br><br><br><br>

打赏作者杯果汁
=========================
不一定要你给赞赏，芸芸众生，相遇相识是一种缘份。不过可以给点个star，或者加个好友吼

<img src="https://images.gitee.com/uploads/images/2019/0129/171904_f6efc3e7_1521920.jpeg" width="220" height="220" alt="微信赞赏码" style="float: left;"/>

<img src="https://images.gitee.com/uploads/images/2019/0129/172138_4a5aa6bc_1521920.jpeg" width="220" height="220" alt="支付宝赞赏码" style="float: left;"/>


可以通过主站搜索淘宝优惠券领券购物，可以省不少钱哦！主站：http://www.smallmi.com

项目演示：https://demo.smallmi.com


致谢
=========================
感谢所有为项目提出问题的贡献者！感谢捐赠鼓励！