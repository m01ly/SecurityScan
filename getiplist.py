# -*- coding: utf-8 -*
# filename: lan_ip_scan.py
#import netifaces
#通过网段扫描得到所有存活IP
import nmap
import os
import time
subnetlist = [{'env': 'dev', 'subnet': '192.168.100.1'}, {'env': 'dev', 'subnet': '192.168.101.1'},{'env': 'dev', 'subnet': '192.168.102.1'},
              {'env': 'beta', 'subnet': '192.168.92.1'}, {'env': 'beta', 'subnet': '192.168.93.1'},{'env': 'beta', 'subnet': '192.168.94.1'}
              ]
# 拼接 IP 列表
def get_ip_lists(subnetlist):
    # 拼接 IP 列表
    ip_lists = []
    for subnet in subnetlist:
        subnetip = subnet['subnet']
        env = subnet['env']
        for i in range(1,255):
            ip = '{}{}'.format(subnetip[:-1], i)
            dict = {"env": env, "ip": ip}
            ip_lists.append(dict)
    print(ip_lists)
    return ip_lists
def scan_ip_survial(ip,env):
    nmScan = nmap.PortScanner()
    result = nmScan.scan(hosts=ip, arguments='-sP')
    isup = result['nmap']['scanstats']['uphosts']
    if isup=='1':
        hostname = result['scan'][ip]['hostnames'][0]['name']
        return env+","+ip+","+hostname
    else:
        return None
def get_all_survial_hosts():
    survial_hosts = []
    ip_lists = get_ip_lists(subnetlist)
    for ipdict in ip_lists:
        ip=ipdict['ip']
        env=ipdict['env']
        scan_rst = scan_ip_survial(ip,env)
        if scan_rst:
            survial_hosts.append(scan_rst)
            print(scan_rst)
    return survial_hosts
def writetotxt(hostslist):
    if os.path.exists("survialhosts.txt"):
        os.remove("survialhosts.txt")
    st = time.strftime("%Y%m%d", time.localtime())
    # 以写的方式打开文件，如果文件不存在，就会自动创建
    file_write_obj = open("survialhosts" + st + ".txt", 'w')
    for var in hostslist:
        json_str = str(var)  # dumps
        file_write_obj.writelines(json_str)
        file_write_obj.write('\n')
    file_write_obj.close()
if __name__ == '__main__':
    survial_hosts=get_all_survial_hosts()
    writetotxt(survial_hosts)
