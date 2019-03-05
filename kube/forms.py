# -*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''

from django import forms
from kube.models import KubeNode, KubeVars


class KubeNodeForm(forms.ModelForm):
    class Meta:
        model = KubeNode
        exclude = ('created_by',)

        widgets = {
            'ip': forms.Select(attrs={'class': 'form-control', 'placeholder': '输入节点IP'}),
            'role': forms.Select(attrs={'class': 'form-control', 'placeholder': '选择节点角色'}),
            'LB_ROLE': forms.Select(attrs={'class': 'form-control', 'placeholder': '选择节点类型'}),
        }


class KubeVarsForm(forms.ModelForm):
    class Meta:
        model = KubeVars
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
