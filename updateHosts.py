#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################
# name:updateHosts
# author:https://github.com/ladder1984
# version:1.3.1
# license:MIT
############################

import urllib2
import platform
from datetime import *
import re
import os
import shutil
import ConfigParser
import sys

# default setting
hosts_folder = ""
hosts_location = hosts_folder + "hosts"

source_list = ['https://raw.githubusercontent.com/vokins/simpleu/master/hosts']
not_block_sites = 0
# default setting

errorLog = open('errorLog.txt', 'a')


def get_cur_info():
    return(sys._getframe().f_back.f_code.co_name)


def check_system():
    global hosts_folder
    global hosts_location
    if platform.system() == 'Windows':
        hosts_folder = os.environ['SYSTEMROOT']+"\\System32\\drivers\\etc\\"
    elif platform.system() == 'Linux'or platform.system() == 'Darwin':
        hosts_folder = "/etc/"
    hosts_location = hosts_folder + "hosts"


def get_config():
    global source_list
    global not_block_sites
    if os.path.exists('config.ini'):
        try:
            # 清除Windows记事本自动添加的BOM
            content = open('config.ini').read()
            content = re.sub(r"\xfe\xff", "", content)
            content = re.sub(r"\xff\xfe", "", content)
            content = re.sub(r"\xef\xbb\xbf", "", content)
            open('config.ini', 'w').write(content)

            config = ConfigParser.ConfigParser()
            config.read('config.ini')
            source_id = config.get('source_select', 'source_id')
            source_list = source_id.split(",")
            for i in range(len(source_list)):
                source_list[i]=config.get('source_select', 'source'+str(i+1))

            not_block_sites = config.get("other", "not_block_sites")
        except BaseException, e:
            errorLog.write(str(datetime.now())+'\n'+'function:'+get_cur_info()+'\nerror:'+str(e)+'\n\n')


def backup_hosts():
    try:
        if (not os.path.isfile(hosts_folder + 'backup_hosts_original_by_updateHosts')) and \
                os.path.isfile(hosts_folder + 'hosts'):
            shutil.copy(hosts_folder+'hosts', hosts_folder+'backup_hosts_original_by_updateHosts')
        if os.path.isfile(hosts_folder + 'hosts'):
            shutil.copy(hosts_folder+'hosts', hosts_folder+'backup_hosts_last_by_updateHosts')
    except BaseException, e:
        errorLog.write(str(datetime.now())+'\n'+'function:'+get_cur_info()+'\nerror:'+str(e)+'\n\n')


def download_hosts():
    try:
        hosts_from_web = open("hosts_from_web","a")
        for x in source_list:
            data=urllib2.urlopen(x)
            hosts_from_web.write(data.read())
    except BaseException, e:
        errorLog.write(str(datetime.now())+'\n'+'function:'+get_cur_info()+'\nerror:'+str(e)+'\n\n')


def process_hosts():
    try:
        hosts_content = open('hosts', 'w')
        file_from_web = open('hosts_from_web')
        hosts_from_web = file_from_web.read()
        file_user_defined = open('hosts_user_defined.txt')
        hosts_user_defined = file_user_defined.read()
        hosts_content.write('#hosts_user_defined\n')
        hosts_content.write(hosts_user_defined)
        hosts_content.write('\n#hosts_user_defined\n')
        hosts_content.write('\n\n#hosts_by_hostsUpdate\n\n')
        if not_block_sites is "1":
            hosts_from_web = re.sub("127.0.0.1", "#not_block_sites", hosts_from_web)
        hosts_content.write(hosts_from_web)
        hosts_content.write('\n#hosts_by_hostsUpdate')
        hosts_content.close()
        file_from_web.close()
        file_user_defined.close()
        os.remove('hosts_from_web')
    except BaseException, e:
        errorLog.write(str(datetime.now())+'\n'+'function:'+get_cur_info()+'\nerror:'+str(e)+'\n\n')


def move_hosts():
    try:
        shutil.move("hosts", hosts_location)
    except BaseException, e:
        errorLog.write(str(datetime.now())+'\n'+'function:'+get_cur_info()+'\nerror:'+str(e)+'\n\n')


def main():
    check_system()
    get_config()
    backup_hosts()
    download_hosts()
    process_hosts()
    move_hosts()
    errorLog.close()


if __name__ == '__main__':
    main()