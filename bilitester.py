#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 16:52
# @Author  : Miyouzi
# @File    : akamTester.py
# @Software: PyCharm

from pythonping import ping
from ColorPrinter import color_print
from GlobalDNS import GlobalDNS
import sys, os, argparse
import concurrent.futures
import requests

working_dir = os.path.dirname(os.path.realpath(__file__))
# working_dir = os.path.dirname(sys.executable)  # 使用 pyinstaller 编译时，打开此项
ip_list_path = os.path.join(working_dir, 'ip_list.txt')
version = 114.514


def ping_test(ip):
    result = ping(ip, count=5)
    delay = result.rtt_avg_ms
    msg = ip + '\t平均延迟: ' + str(delay) + ' ms'
    if delay<100:
        color_print(msg)
    else:
        color_print(msg)
    return delay

def ip_location(ip):
	url = f'https://api.asilu.com/ip/?ip={ip}'
	info = requests.get(url)
	info = info.json()
	dz = info['dz']
	wl = info['wl']
	if wl == '':
		msg = f'{dz}'
		return msg
	else:
		msg = f'{dz} {wl}'
		return msg
		
def myip_location():
	url = f'http://ip-api.com/json/?lang=zh-CN'
	info = requests.get(url)
	info = info.json()
	country = info['country']
	city = info['city']
	isp = info['isp']
	as_info = info['as']
	query = info['query']
	msg = f'\n您的IP为 {query}, 所在地区为 {country} {city},所使用的运营商为 {isp}, ASN信息 {as_info}\n'
	return msg
    	
	

version_msg = '当前BiliTester版本: ' + str(version)
color_print(version_msg, 2)
host = 'live-push.bilivideo.com'
ip_list_add = {}
# 支持命令行, 允许用户通过参数指定测试域名
if len(sys.argv) > 1:
    parser = argparse.ArgumentParser()
    parser.add_argument('--user_host', '-u', type=str, help='指定测试域名', default=host, required=True)
    arg = parser.parse_args()
    if arg.user_host:
        host = arg.user_host

try:
    akam = GlobalDNS(host)
    color_print('第一次解析:')
    ip_list = akam.get_ip_list()
    print()
    color_print('第二次解析:')
    akam.renew()
    ip_list = ip_list | akam.get_ip_list()
    print()
    color_print('第三次解析:')
    akam.renew()
    ip_list = ip_list | akam.get_ip_list()
    with open(ip_list_path, 'r', encoding='utf-8') as f:
            ip_list_add = f.read().split(",")
            for x in ip_list_add:
            	ip_list.add(x)

except BaseException as e:
    color_print('进行全球解析时遇到未知错误: '+str(e), status=1)
    if os.path.exists(ip_list_path):
        color_print('将读取本地保存的ip列表', status=1)
    else:
        color_print('没有本地保存的ip列表！程序终止！', status=1)
        print()
        input('按回车退出')
        sys.exit(0)
print()
color_print('共取得 '+str(len(ip_list))+' 个 IP, 开始测试延迟')
print()

ip_info = []
good_ips = []

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(ping_test, ip) for ip in ip_list]
    delays = [f.result() for f in futures]

for delay, ip in zip(delays, ip_list):
    ip_info.append({'ip': ip, 'delay': delay})
    if delay < 100:
        good_ips.append({'ip': ip, 'delay': delay})

print()

if len(good_ips) > 0:
    color_print(myip_location(), status=2)
    color_print('基于当前网络环境, 以下为延迟低于100ms的IP', status=2)
    good_ips.sort(key=lambda x:x['delay'])
    for ip in good_ips:
        msg = f"{ip['ip']} 平均延迟: {ip['delay']} ms {ip_location(ip['ip'])}"
        color_print(msg)
else:
    ip_info.sort(key=lambda x:x['delay'])
    num = len(ip_info)  # 要显示的节点数
    if num > 8:  # 如果解析的节点数超过 3 个, 那么显示 3 个就行
        num = 8
    color_print(myip_location(), status=2)
    color_print('本次测试未能找到延迟低于100ms的IP! 以下为延迟最低的 ' + str(num) + ' 个节点', status=2)
    for i in range(0,num):
        ip = ip_info[i]['ip']
        msg = f"{ip_info[i]['ip']} 平均延迟: {ip_info[i]['delay']} ms {ip_location(ip)}"
        color_print(msg)

print()
input('按回车退出')
sys.exit(0)