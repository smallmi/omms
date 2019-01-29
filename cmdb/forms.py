#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''

from django import forms
from cmdb.models import Server, SystemUser


class ServerForm(forms.ModelForm):

    class Meta:
        model = Server
        exclude = ('author',)
        # ProjectName_description = '输入项目名称，如：运营系统',
        # ServiceName_description = '输入服务名称，如：redis、app',
        # InIp_description = '输入内网IP',
        # ExIp_description = '输入外网IP',

        widgets = {
            # 'project_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入项目名称，如：运营系统'}),
            # 'service_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入服务名称，如：redis、app'}),
            'in_ip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入内网IP'}),
            'ex_ip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入外网IP'}),
            'idc': forms.Select(attrs={'class': 'form-control'}),
            'system_user': forms.Select(attrs={'class': 'form-control'}),
            'app_project': forms.Select(attrs={'class': 'form-control'}),
        }


class SystemUserForm(forms.ModelForm):
    class Meta:
        model = SystemUser
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入名称，如：测试用户'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入登录用户名，如：root'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '输入密码'}),
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'class': 'form-control', 'placeholder': '输入描述信息'}),
        }

