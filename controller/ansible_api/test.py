#!/usr/bin/env python
# coding:utf-8

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
import os, sys

# 在指定文件时，不能使用列表指定多个。
host_path = '/root/ansible/playbooks/hosts'
if not os.path.exists(host_path):
    print('[INFO] The [%s] inventory does not exist') % host_path
    sys.exit()

# 管理变量的类，包括主机，组，扩展等变量，之前版本是在 inventory中的
variable_manager = VariableManager()

# 用来加载解析yaml文件或JSON内容,并且支持vault的解密
loader = DataLoader()

# 初始化需要的对象
Options = namedtuple('Options',
                     ['connection',
                      'remote_user',
                      'ask_sudo_pass',
                      'verbosity',
                      'ack_pass',
                      'module_path',
                      'forks',
                      'become',
                      'become_method',
                      'become_user',
                      'check',
                      'listhosts',
                      'listtasks',
                      'listtags',
                      'syntax',
                      'sudo_user',
                      'sudo',
                      'private_key_file',
                      'ssh_common_args',
                      'sftp_extra_args',
                      'scp_extra_args',
                      'ssh_extra_args'])

# 定义连接远端的额方式为smart
options = Options(connection='smart',
                  remote_user='root',
                  ack_pass=None,
                  sudo_user='root',
                  forks=5,
                  sudo='yes',
                  ask_sudo_pass=False,
                  verbosity=5,
                  module_path=None,
                  become=True,
                  become_method='sudo',
                  become_user='root',
                  check=None,
                  listhosts=None,
                  listtasks=None,
                  listtags=None,
                  syntax=None,
                  private_key_file=None,
                  ssh_common_args=None,
                  sftp_extra_args=None,
                  scp_extra_args=None,
                  ssh_extra_args=None)

# 定义默认的密码连接，主机未定义密码的时候才生效，conn_pass指连接远端的密码，become_pass指提升权限的密码
passwords = dict(conn_pass='root1234', become_pass='root1234')

# create inventory and pass to var manager
# 创建inventory、并带进去参数
inventory = InventoryManager(loader=loader, variable_manager=variable_manager, host_list='/root/ansible/playbooks/hosts')

# 把inventory传递给variable_manager管理
variable_manager.set_inventory(inventory)

# 多个yaml文件则以列表形式
playbook_path = ['/root/ansible/playbooks/mysql.yml',
                 '/root/ansible/playbooks/test_result.yml']
for playbook in playbook_path:
    if not os.path.exists(playbook):
        print('[INFO] The [%s] playbook does not exist') % playbook
        sys.exit()

playbook = PlaybookExecutor(playbooks=playbook_path,
                            inventory=inventory,
                            variable_manager=variable_manager,
                            loader=loader,
                            options=options,
                            passwords=passwords)
# 执行playbook
result = playbook.run()

print('执行结果: %s') % (result)