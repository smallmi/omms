#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''
from django.db import models
from accounts.models import User
from cmdb.models import Server


class KubeNode(models.Model):
    kube_role = (
        (0, u"deploy"),
        (1, u"etcd"),
        (2, u"kube-master"),
        (3, u"kube-node"),
        (4, u"lb"),
    )

    lb_role = (
        (0, '非lb角色选此项'),
        (1, 'master'),
        (2, 'backup'),
    )
    # K8S集群部署信息
    # ip = models.CharField(max_length=64, blank=True, unique=True, verbose_name=u'节点IP')
    ip = models.ForeignKey(Server, blank=True, null=True, on_delete=models.SET_NULL,
                                    verbose_name=u'节点IP')
    role = models.IntegerField(choices=kube_role, verbose_name=u'节点角色')
    LB_ROLE = models.IntegerField(choices=lb_role, verbose_name=u'节点类型')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name=u'创建者')
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name=u'创建时间')

    def __unicode__(self):
        return self.ip

    __str__ = __unicode__

    class Meta:
        permissions = (
            ("view_kubeNode", "查看K8S节点"),
            ("add_kubeNode", "添加K8S节点"),
            ("change_kubeNode", "编辑K8S节点"),
            ("delete_kubeNode", "删除K8S节点"),
        )
        default_permissions = ()


class KubeVars(models.Model):
    HARBOR_DOMAIN = models.CharField(max_length=64, null=True, blank=True, verbose_name=u'harbor域名')
    NTP_ENABLED = models.CharField(max_length=64, null=True, blank=True, default='no', verbose_name=u'是否时间同步')
    NEW_INSTALL = models.CharField(max_length=64, null=True, blank=True, default='no', verbose_name=u'是否新建')
    EX_VIP = models.CharField(max_length=64, null=True, blank=True, verbose_name=u'外部负载均衡')

    DEPLOY_MODE = models.CharField(max_length=64, blank=True, verbose_name=u'集群部署模式')
    K8S_VER = models.CharField(max_length=64, blank=True, verbose_name=u'集群主版本号')
    MASTER_IP = models.CharField(max_length=64, blank=True, verbose_name=u'LB节点VIP')
    KUBE_APISERVER = models.CharField(max_length=64, blank=True, verbose_name=u'APISERVER')
    CLUSTER_NETWORK = models.CharField(max_length=64, blank=True, verbose_name=u'集群网络插件')
    SERVICE_CIDR = models.CharField(max_length=64, blank=True, verbose_name=u'服务网段')
    CLUSTER_CIDR = models.CharField(max_length=64, blank=True, verbose_name=u'POD网段')
    NODE_PORT_RANGE = models.CharField(max_length=64, blank=True, verbose_name=u'服务端口范围')
    CLUSTER_KUBERNETES_SVC_IP = models.CharField(max_length=64, blank=True, verbose_name=u'kubernetes服务IP')
    CLUSTER_DNS_SVC_IP = models.CharField(max_length=64, blank=True, verbose_name=u'集群DNS服务IP')
    CLUSTER_DNS_DOMAIN = models.CharField(max_length=64, blank=True, verbose_name=u'集群DNS域名')
    BASIC_AUTH_USER = models.CharField(max_length=64, blank=True, verbose_name=u'集群BasicAuth用户名')
    BASIC_AUTH_PASS = models.CharField(max_length=64, blank=True, verbose_name=u'集群BasicAuth密码')
    bin_dir = models.CharField(max_length=64, blank=True, verbose_name=u'二进制文件目录')
    ca_dir = models.CharField(max_length=64, blank=True, verbose_name=u'证书目录')
    base_dir = models.CharField(max_length=64, blank=True, verbose_name=u'部署目录')


    def __unicode__(self):
        return self.K8S_VER

    __str__ = __unicode__

    class Meta:
        permissions = (
            ("view_kubeCluster", "查看K8S集群参数模板"),
            ("add_kubeCluster", "添加K8S集群参数模板"),
            ("change_kubeCluster", "编辑K8S集群参数模板"),
            ("delete_kubeCluster", "删除K8S集群参数模板"),
        )
        default_permissions = ()