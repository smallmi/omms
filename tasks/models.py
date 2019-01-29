#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''
from django.db import models

from accounts.models import User


class history(models.Model):
    root = models.CharField(max_length=32, verbose_name='用户', null=True)
    ip = models.GenericIPAddressField(verbose_name='IP', null=True)
    port = models.CharField(max_length=32, verbose_name='端口', null=True)
    cmd = models.CharField(max_length=128, verbose_name='命令', null=True)
    user = models.CharField(max_length=32, verbose_name='操作者', null=True)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    # class Meta:
    #     db_table = "history"
    #     verbose_name = "历史命令"
    #     verbose_name_plural = '历史命令'

    class Meta:
        permissions = (
            ("rview_histoy", ("查看历史命令")),
            ("view_cmd", ("查看命令行列表")),
            ("change_cmd", ("更新执行命令")),
        )
        default_permissions = ()

    def __str__(self):
        return self.ip


class toolsscript(models.Model):
    TOOL_RUN_TYPE = (
        (0, 'shell'),
        (1, 'python'),
        (2, 'yml'),
    )

    name = models.CharField(max_length=100, verbose_name='工具名称', unique=True)
    tool_script = models.TextField(verbose_name='脚本', null=True, blank=True)
    tool_run_type = models.IntegerField(choices=TOOL_RUN_TYPE, verbose_name='脚本类型', default=0)
    comment = models.TextField(verbose_name='工具说明', null=True, blank=True)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    utime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    # class Meta:
    #     db_table = "toolsscript"
    #     verbose_name = "工具"
    #     verbose_name_plural = verbose_name
    class Meta:
        permissions = (
            ("view_toolsScript", ("查看脚本工具列表")),
            ("add_toolsScript", ("新增工具脚本")),
            ("change_toolsScript", ("编辑工具脚本")),
            ("delete_toolsScript", ("删除工具脚本")),
        )
        default_permissions = ()


class mavenJar(models.Model):
    groupId = models.CharField(max_length=128, verbose_name='groupId', null=True)
    artifactId = models.CharField(max_length=128, verbose_name='artifactId', null=True)
    version = models.CharField(max_length=32, verbose_name='version', null=True)
    classifier = models.CharField(max_length=128, verbose_name='classifier', null=True)
    deployStatus = models.NullBooleanField(default=True, null=True, blank=True, verbose_name=u'上传状态')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name=u'操作者')
    ctime = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        # db_table = "mavenJar"
        # verbose_name = "Jar包信息"
        # verbose_name_plural = 'Jar包信息'

        permissions = (
            ("view_mavenJar", ("查看上传Jar列表")),
            ("add_mavenJar", ("上传Jar")),
        )
        default_permissions = ()

    def __str__(self):
        return self.groupId