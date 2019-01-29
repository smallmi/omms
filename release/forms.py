#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''

from django import forms
from release.models import AppProject, ReleasePlan


class AppProjectForm(forms.ModelForm):

    class Meta:
        model = AppProject
        exclude = ('author',)

        widgets = {
            'app_name_cn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入应用中文名称，如：运营系统'}),
            'app_name_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入应用英文名称，如：manager'}),
            'app_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入应用类型，如：web，DB，中间件'}),
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'java_version': forms.Select(attrs={'class': 'form-control'}),
            'git_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入Git完整地址'}),
            'git_properties': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入配置文件信息'}),
        }


class ReleasePlanForm(forms.ModelForm):

    class Meta:
        model = ReleasePlan
        exclude = ('author',)

        widgets = {
            'app': forms.Select(attrs={'class': 'form-control'}),
            'git_branch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入封板ID或分支，如：master'}),
            'app_version': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入应用tag版本，如：V1.0.0'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '输入应用此次上线升级内容'}),
        }

