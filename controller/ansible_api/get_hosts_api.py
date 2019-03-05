#-*- coding: utf-8 -*-
'''
    Author: smallmi
    Blog: http://www.smallmi.com
'''


from controller.ansible_api.inventory import BaseInventory
from controller.ansible_api.runner import AdHocRunner
import logging

logger = logging.getLogger('omms')


def init(assets):
    inventory = BaseInventory(assets)
    runner = AdHocRunner(inventory)
    return runner


def get_ulimit(assets):
    # 最大文件打开数
    runner = init(assets)

    tasks = [
        {"action": {"module": "shell", "args": "ulimit -n"}, "name": "run_ulimit"},
    ]
    ret = runner.run(tasks, "all")
    infoList = []
    for i in assets:
        result = {}
        try:
            result['ulimit'] = ret.results_raw['ok'][i['hostname']]['run_ulimit']['stdout']
            result['host_ip'] = i['hostname']
            infoList.append(result)
        except:
            print('检测 ' + i['hostname'] + ' 此主机网络不可达...')

    return infoList


def get_uptime(assets):
    # 运行时间
    runner = init(assets)

    tasks = [
        {"action": {"module": "shell", "args": "uptime"}, "name": "run_uptime"},
    ]
    ret = runner.run(tasks, "all")

    infoList = []
    for i in assets:
        result = {}
        try:
            result['uptime'] = int(
                ret.results_raw['ok'][i['hostname']]['run_uptime']['stdout'].split('up')[1].split('days')[0])
            result['host_ip'] = i['hostname']
            infoList.append(result)
        except:
            logger.error('检测 ' + i['hostname'] + ' 此主机网络不可达...')

    return infoList


def get_host_info(assets):
    runner = init(assets)
    tasks = [
        {"action": {"module": "setup", "args": " "}, "name": "run_setup"},
    ]
    ret = runner.run(tasks, "all")

    print(ret.results_raw)
    infoList = []
    for i in assets:
        try:
            data = ret.results_raw['ok'][i['hostname']]['run_setup']['ansible_facts']
            sn = data['ansible_product_serial']
            host_name = data['ansible_hostname']

            # description = datastructure['contacted'][ip][0]['ansible_facts']['ansible_lsb']['description']
            ansible_machine = data['ansible_machine']
            # sysinfo = '%s %s' % (description, ansible_machine)
            sysinfo = '%s' % (ansible_machine)

            os_kernel = data['ansible_kernel']

            cpu = data['ansible_processor'][2]
            cpu_count = data['ansible_processor_count']
            cpu_cores = data['ansible_processor_cores']
            mem = data['ansible_memtotal_mb']

            # ipadd_in = data['ansible_all_ipv4_addresses'][0]
            ipadd_in = data['ansible_default_ipv4']['address']
            # disk = data['ansible_devices']['sda']['size']
            try:
                disk = data['ansible_devices']['sda']['size']
            except Exception as a:
                logger.info(i['hostname'] + ' 主机不存在{}类型磁盘，开始获取vda'.format(a))
                disk = data['ansible_devices']['vda']['size']

            ansible_mounts = data['ansible_mounts']
            ansible_memory_mb_nocache = data['ansible_memory_mb']['nocache']
            ansible_memory_mb_real = data['ansible_memory_mb']['real']
            ansible_memory_mb_swap = data['ansible_memory_mb']['swap']

            mem_total = ansible_memory_mb_real['total']
            mem_free = ansible_memory_mb_nocache['free']
            swap_total = ansible_memory_mb_swap['total']
            swap_free = ansible_memory_mb_swap['free']
            for am in ansible_mounts:
                if am['mount'] == '/':
                    disk_total = am['size_total']/1024/1024
                    disk_free = am['size_available']/1024/1024
                else:
                    pass

            mem_rate = "%.1f" % ((1 - (mem_free/mem_total))*100)
            if swap_total != 0:
                swap_rate = "%.1f" % ((1 - (swap_free / swap_total))*100)
            else:
                swap_rate = 0
            disk_rate = "%.1f" % ((1 - (disk_free / disk_total))*100)

            # print sysinfo
            data['sn'] = sn
            data['sysinfo'] = sysinfo
            data['cpu'] = cpu
            data['cpu_count'] = cpu_count
            data['cpu_cores'] = cpu_cores
            data['mem'] = mem
            data['disk'] = disk
            data['ipadd_in'] = ipadd_in
            data['os_kernel'] = os_kernel
            data['host_name'] = host_name
            data['status'] = True

            data['mem_rate'] = mem_rate
            data['swap_rate'] = swap_rate
            data['disk_rate'] = disk_rate
            data['mem_total'] = mem_total
            data['mem_free'] = mem_free
            data['swap_total'] = swap_total
            data['swap_free'] = swap_free
            data['disk_total'] = disk_total
            data['disk_free'] = disk_free

            infoList.append(data)
        except Exception as e:
            logger.error('信息采集出现错误error:{}'.format(e))
            unreachable_dic = {'ipadd_in': i['hostname'], 'status': False}
            logger.error('检测 {} 此主机网络不可达...'.format(i['hostname']))
            infoList.append(unreachable_dic)

    return infoList
