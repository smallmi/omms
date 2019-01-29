OMMS 运维监控管理系统
=======================

[![Python Version](https://img.shields.io/badge/Python--3.6-paasing-green.svg)](https://img.shields.io/badge/Python--3.6-paasing-green.svg)
[![Django Version](https://img.shields.io/badge/Django--1.11.0-paasing-green.svg)](https://img.shields.io/badge/Django--1.11.0-paasing-green.svg)

项目作者：小瓶盖

> OMMS现有功能: （QQ交流群：374506612）

- Dashboard
- 资产管理
- 应用管理
- 执行任务
- 监控管理
- 权限管理

特别说明：本系统是基于开源运维管理系统PFMS进行的二次开发，感谢该作者的开源精神。OMMS是在此基础上增加了监控管理，优化了其他模块功能。


## 界面预览：
![资产页面](https://gitee.com/uploads/images/2017/1103/163547_29bfb40b_1521920.png "1.png")

![资产组页面](https://gitee.com/uploads/images/2017/1103/163605_b696ec54_1521920.png "2.png")

![登录用户页面](https://gitee.com/uploads/images/2017/1103/163642_d9e5b600_1521920.png "3.png")

![监控页面1](https://images.gitee.com/uploads/images/2019/0129/164022_60343dd9_1521920.jpeg)

![监控页面2](https://images.gitee.com/uploads/images/2019/0129/164112_7780e34b_1521920.png)



## 部署须知：
Python版本：3.6.2
Django版本：2.1.5

Python升级：https://www.cnblogs.com/tssc/p/7762998.html

### 创建虚拟环境

```
pip3 install --upgrade pip
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

### 安装依赖

```
git clone https://gitee.com/SmallMi/omms.git
cd omms
pip install -i https://pypi.douban.com/simple/  -r requirements.txt

# 如果中间出现mysql_conf这类错误需要执行一下命令：
yum -y install mysql-devel python-devel

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

撩一下
=========================
写开源是我的业余爱好，单纯运维才是主业，无论哪个都欢迎交流。  
人脉也是一项重要能力，请备注姓名@公司，谢谢：）

<img src="https://images.gitee.com/uploads/images/2019/0129/172228_8aabccd0_1521920.jpeg" width="244" height="314" alt="小瓶盖微信" align=left />


<br><br><br><br><br><br><br><br><br><br><br><br><br><br>

打赏作者杯咖啡
=========================
不一定要你给赞赏，芸芸众生，相遇相识是一种缘份。不过可以给点个star，或者加个好友吼

<img src="https://images.gitee.com/uploads/images/2019/0129/171904_f6efc3e7_1521920.jpeg" width="220" height="220" alt="微信赞赏码" style="float: left;"/>

<img src="https://images.gitee.com/uploads/images/2019/0129/172138_4a5aa6bc_1521920.jpeg" width="220" height="220" alt="支付宝赞赏码" style="float: left;"/>


可以通过主站搜索淘宝优惠券领券购物，可以省不少钱哦！主站：http://www.smallmi.com 

项目演示：http://demo.smallmi.com