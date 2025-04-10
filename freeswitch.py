#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Home	: https://www.netkiller.cn
# Author: Neo <netkiller@msn.com>
# Upgrade: 2025-03-29
# FreeSWITCH 用户管理工具
##############################################
import string

try:
    import argparse
    import glob
    import logging
    import os
    import random
    import sys
    import uuid
    import hashlib
    from datetime import datetime
    from texttable import Texttable
    from tqdm import tqdm

    from xml.dom.minidom import Document, parse

except ImportError as err:
    print("Import Error: %s" % (err))
    exit()


class FreeSWITCH():

    freeswitch = 'test'

    def __init__(self):
        self.basedir = os.path.dirname(os.path.abspath(__file__))

        logfile = os.path.join(self.basedir,
                               f"{os.path.splitext(os.path.basename(__file__))[0]}.{datetime.today().strftime('%Y-%m-%d')}.log")
        logging.basicConfig(filename=logfile, level=logging.DEBUG, encoding="utf-8",format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.parser  = argparse.ArgumentParser(description='FreeSWITCH 用户管理工具',epilog='Author: netkiller - https://www.netkiller.cn/linux/')

        self.parser.add_argument('-a','--add', nargs='+', default=None, help='添加用户', metavar="<number> <callsign> <callgroup>")
        self.parser.add_argument('-r','--remove', type=str, default=None, help='删除用户', metavar="1000")
        self.parser.add_argument('-l','--list', action="store_true", default=False, help='列出用户')
        self.parser.add_argument('-s','--show', type=str, default=None, help='查看用户', metavar="1000")
        self.parser.add_argument('-d','--debug', action="store_true", default=False, help='调试模式')

        self.args = self.parser.parse_args()

    def password(self):
        # 定义所有可能的字符，包括大小写字母和数字
        all_characters = string.ascii_letters + string.digits

        # 生成 8 个长度为 8 的密码
        password = ''.join(random.choice(all_characters) for i in range(8))
        return password

    def add(self,args):

        doc = Document()
        include = doc.createElement('include')
        doc.appendChild(include)

        user = doc.createElement('user')
        user.setAttribute('id', args[0])
        include.appendChild(user)

        params = doc.createElement('params')
        user.appendChild(params)

        param1 = doc.createElement('param')
        param1.setAttribute('name', 'password')
        param1.setAttribute('value', self.password())
        params.appendChild(param1)

        param2 = doc.createElement('param')
        param2.setAttribute('name', 'vm-password')
        param2.setAttribute('value', '1000')
        params.appendChild(param2)

        # 在子元素中添加文本内容
        variables = doc.createElement('variables')
        user.appendChild(variables)

        toll_allow = doc.createElement('variable')
        toll_allow.setAttribute('name', 'toll_allow')
        toll_allow.setAttribute('value', 'domestic,international,local')
        variables.appendChild(toll_allow)

        accountcode = doc.createElement('variable')
        accountcode.setAttribute('name', 'accountcode')
        accountcode.setAttribute('value', '1000')
        variables.appendChild(accountcode)

        user_context = doc.createElement('variable')
        user_context.setAttribute('name', 'user_context')
        user_context.setAttribute('value', 'default')
        variables.appendChild(user_context)

        effective_caller_id_name = doc.createElement('variable')
        effective_caller_id_name.setAttribute('name', 'effective_caller_id_name')
        effective_caller_id_name.setAttribute('value', args[1])
        variables.appendChild(effective_caller_id_name)

        effective_caller_id_number = doc.createElement('variable')
        effective_caller_id_number.setAttribute('name', 'effective_caller_id_number')
        effective_caller_id_number.setAttribute('value', '1000')
        variables.appendChild(effective_caller_id_number)

        outbound_caller_id_name = doc.createElement('variable')
        outbound_caller_id_name.setAttribute('name', 'outbound_caller_id_name')
        outbound_caller_id_name.setAttribute('value', '$${outbound_caller_name}')
        variables.appendChild(outbound_caller_id_name)

        outbound_caller_id_number = doc.createElement('variable')
        outbound_caller_id_number.setAttribute('name', 'outbound_caller_id_number')
        outbound_caller_id_number.setAttribute('value', '$${outbound_caller_id}')
        variables.appendChild(outbound_caller_id_number)

        if len(args) ==3:
            callgroup = doc.createElement('variable')
            callgroup.setAttribute('name', 'callgroup')
            callgroup.setAttribute('value', args[2])
            variables.appendChild(callgroup)

        xmlString = doc.childNodes[0].toprettyxml()
        if self.args.debug :
            print(xmlString)
        userfile = os.path.join(self.freeswitch,'directory/default',f"{args[0]}.xml")
        os.makedirs(os.path.dirname(userfile),exist_ok=True)
        with open(userfile, 'w') as file:
        #     # writexml(writer, indent="", addindent="", newl="", encoding=None)，
        #     doc.writexml(f, addindent='  ', newl='\n', encoding='utf-8')
            file.write(xmlString)

    def list(self):
        directory = os.path.join(self.freeswitch, 'directory/default')
        for user in os.listdir(directory):
            print(user)

    def show(self,number):
        # directory = os.path.join(self.freeswitch, 'directory/default')
        userfile = os.path.join(self.freeswitch, 'directory/default', f"{number}.xml")
        with open(userfile, 'r') as file:
            print(file.read())

    def remove(self, number):
        userfile = os.path.join(self.freeswitch, 'directory/default', f"{number}.xml")
        if os.path.isfile(userfile):
            os.remove(userfile)
    def main(self):

        # print(args, args.subcommand)
        if self.args.add and len(self.args.add) >= 2:
            self.add(self.args.add)
        elif self.args.list:
            self.list()
        elif self.args.show:
            self.show(self.args.show)
        elif self.args.remove:
            self.remove(self.args.remove)
        else:
            self.parser.print_help()
            exit()


if __name__ == "__main__":
    try:
        freeswitch = FreeSWITCH()
        freeswitch.main()
    except KeyboardInterrupt as e:
        print(e)
