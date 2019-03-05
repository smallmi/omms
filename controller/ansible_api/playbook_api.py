#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''


from controller.ansible_api.inventory import BaseInventory
from controller.ansible_api.runner import PlayBookRunner
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager


def init(assets, playbook_path):
    inventory = BaseInventory(assets)
    runner = PlayBookRunner(playbook_path, inventory=inventory)
    return runner


def exePlaybook(assets, playbook_path):
    runner = init(assets, playbook_path)
    ret = runner.run()

    return ret


def hostsPlaybook(hosts_path, playbook_path):
    # 用来加载解析yaml文件或JSON内容,并且支持vault的解密
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=hosts_path)
    # 管理变量的类，包括主机，组，扩展等变量，之前版本是在 inventory中的
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    # 把inventory传递给variable_manager管理
    variable_manager.set_inventory(inventory)

    runner = PlayBookRunner(playbook_path, inventory=inventory)

    ret = runner.run()
    return ret
