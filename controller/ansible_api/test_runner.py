# -*- coding: utf-8 -*-

from .runner import AdHocRunner, CommandRunner
from .inventory import BaseInventory


def TestAdHocRunner():
    """
     以yml的形式 执行多个命令
    :return:
    """

    host_data = [
        {
            "hostname": "testserver",
            "ip": "192.168.203.29",
            "port": 22,
            "username": "oriental",
            "password": "456!@#",
        },
    ]
    inventory = BaseInventory(host_data)
    runner = AdHocRunner(inventory)

    tasks = [
        {"action": {"module": "shell", "args": "whoami"}, "name": "run_whoami"},
    ]
    ret = runner.run(tasks, "all")
    print(ret.results_summary)
    print(ret.results_raw)


def TestCommandRunner():
    """
    执行单个命令，返回结果
    :return:
    """

    host_data = [
        {
            "hostname": "testserver",
            "ip": "192.168.10.100",
            "port": 22,
            "username": "root",
            "password": "123456",
        },
    ]
    inventory = BaseInventory(host_data)
    runner = CommandRunner(inventory)

    res = runner.execute('pwd', 'all')
    print(res.results_command)
    print(res.results_raw)
    print(res.results_command['testserver']['stdout'])


if __name__ == "__main__":
    TestAdHocRunner()
# TestCommandRunner()
