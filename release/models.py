#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''

from __future__ import unicode_literals

from django.db import models
from accounts.models import User


# Create your models here.


class Platform(models.Model):
    # 平台信息
    name = models.CharField(max_length=64, unique=True, verbose_name=u'平台名')
    owner = models.CharField(max_length=64, null=True, verbose_name=u'负责人')
    phone = models.CharField(max_length=64, null=True, verbose_name=u'手机号')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name=u'创建者')
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name=u'创建时间')
    comment = models.TextField(blank=True, verbose_name=u'描述')

    def __unicode__(self):
        return self.name

    __str__ = __unicode__

    class Meta:
        permissions = (
            ("view_platform", ("查看平台")),
            ("add_platform", ("添加平台")),
            ("change_platform", ("编辑平台")),
            ("delete_platform", ("删除平台")),
        )
        default_permissions = ()


class AppProject(models.Model):
    # 应用信息
    java_version = (
        (1, u"version 1.6"),
        (2, u"version 1.7"),
        (3, u"version 1.8"),
    )

    app_name_en = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'英文名称')
    app_name_cn = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'中文名称')
    app_type = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'应用类型')
    platform = models.ForeignKey(Platform, blank=True, null=True, related_name='servers', on_delete=models.SET_NULL,
                                 verbose_name=u'所属平台')

    git_url = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'Git 地址')
    # git_branch = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'Git分支')
    git_properties = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'配置文件')
    java_version = models.IntegerField(choices=java_version, null=True, verbose_name=u'Java版本')

    ctime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name=u'创建者')
    comment = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __unicode__(self):
        return '%s（%s）' % (self.app_name_cn, self.app_name_en)

    __str__ = __unicode__

    class Meta:
        permissions = (
            ("view_appProject", ("查看应用信息")),
            ("add_appProject", ("添加应用")),
            ("change_appProject", ("编辑应用")),
            ("delete_appProject", ("删除应用")),
        )
        default_permissions = ()


class ReleasePlan(models.Model):
    # 发布计划
    app = models.ForeignKey(AppProject, blank=True, null=True, related_name='apps', on_delete=models.SET_NULL,
                            verbose_name=u'发布应用')
    git_branch = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'代码版本')
    app_version = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'应用版本')

    plan_status = models.NullBooleanField(default=False, null=True, blank=True, verbose_name=u'发布状态')

    ctime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name=u'创建者')
    comment = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __unicode__(self):
        return '%s - %s' % (self.git_branch, self.app_version)

    class Meta:
        permissions = (
            ("view_releasePlan", ("查看发布计划")),
            ("add_releasePlan", ("添加发布计划")),
            ("change_releasePlan", ("编辑发布计划")),
            ("delete_releasePlan", ("删除发布计划")),
        )
        default_permissions = ()