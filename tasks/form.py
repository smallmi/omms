#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''
from    django import forms
from .models import toolsscript, mavenJar


class ToolForm(forms.ModelForm):
    class Meta:
        model = toolsscript
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(
                attrs={'cols': 80, 'rows': 3}
            ),
            'tool_script': forms.Textarea(

            ),
            # 'product_line': forms.SelectMultiple(
            #     attrs={'class': 'select2',
            #            'data-placeholder': ('选择产品线')}),
            # 'admin_user': forms.Select(
            #     attrs={'class': 'select2',
            #            'data-placeholder': ('Select asset admin user')}),
        }
        help_texts = {
            # 'network_ip': '必填项目',
            'name': ('必填项目,名字不可以重复'),
        }


class JarForm(forms.ModelForm):

    class Meta:
        model = mavenJar
        exclude = ('author',)

        widgets = {
            'groupId': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '当前Maven项目隶属的实际项目'}),
            'artifactId': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '实际项目中的一个Maven项目或模块'}),
            'version': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Maven项目当前所处的版本'}),
            'classifier': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '构建输出的一些附属构件，如无输入no'}),
        }


