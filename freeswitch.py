#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
# Home	: https://www.netkiller.cn
# Author: Neo <netkiller@msn.com>
# Upgrade: 2025-04-10
# FreeSWITCH 用户管理工具
##############################################
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
    import string
    from xml.dom.minidom import Document, parse
    from lxml import etree

except ImportError as err:
    print("Import Error: %s" % (err))
    exit()


class FreeSWITCH():
    freeswitch = 'test'

    def __init__(self):
        self.basedir = os.path.dirname(os.path.abspath(__file__))

        logfile = os.path.join(self.basedir,
                               f"{os.path.splitext(os.path.basename(__file__))[0]}.{datetime.today().strftime('%Y-%m-%d')}.log")
        logging.basicConfig(filename=logfile, level=logging.DEBUG, encoding="utf-8",
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.logger = logging.getLogger()
        self.parser = argparse.ArgumentParser(description='FreeSWITCH 用户管理工具',
                                              epilog='Author: netkiller - https://www.netkiller.cn/linux/')

        self.parser.add_argument('-a', '--add', nargs='+', default=None, help='添加用户',
                                 metavar="<number> <callsign> <callgroup>")
        self.parser.add_argument('-r', '--remove', type=str, default=None, help='删除用户', metavar="1000")
        self.parser.add_argument('-l', '--list', action="store_true", default=False, help='列出用户')
        self.parser.add_argument('-s', '--show', type=str, default=None, help='查看用户', metavar="1000")
        self.parser.add_argument('-d', '--debug', action="store_true", default=False, help='调试模式')

        self.args = self.parser.parse_args()

    def password(self):
        # 定义所有可能的字符，包括大小写字母和数字
        all_characters = string.ascii_letters + string.digits

        # 生成 8 个长度为 8 的密码
        password = ''.join(random.choice(all_characters) for i in range(8))
        return password

    def password1(self):
        # 定义所有可能的字符，包括大小写字母和数字
        all_characters = string.digits

        # 生成 8 个长度为 8 的密码
        password = ''.join(random.choice(all_characters) for i in range(4))
        return password

    def add(self, args):

        number = args[0]
        callsign = args[1]
        password = self.password()
        vmpassword = self.password1()

        userfile = os.path.join(self.freeswitch, 'directory/default', f"{number}.xml")
        if os.path.isfile(userfile):
            confirm = input("用户已存在是否覆盖(Y/N): ")
            if confirm == 'n' or confirm == 'N':
                exit()

        doc = Document()
        include = doc.createElement('include')
        doc.appendChild(include)

        user = doc.createElement('user')
        user.setAttribute('id', number)
        include.appendChild(user)

        params = doc.createElement('params')
        user.appendChild(params)

        param1 = doc.createElement('param')
        param1.setAttribute('name', 'password')
        param1.setAttribute('value', password)
        params.appendChild(param1)

        param2 = doc.createElement('param')
        param2.setAttribute('name', 'vm-password')
        param2.setAttribute('value', vmpassword)
        params.appendChild(param2)

        variables = doc.createElement('variables')
        user.appendChild(variables)

        toll_allow = doc.createElement('variable')
        toll_allow.setAttribute('name', 'toll_allow')
        toll_allow.setAttribute('value', 'domestic,international,local')
        variables.appendChild(toll_allow)

        accountcode = doc.createElement('variable')
        accountcode.setAttribute('name', 'accountcode')
        accountcode.setAttribute('value', number)
        variables.appendChild(accountcode)

        user_context = doc.createElement('variable')
        user_context.setAttribute('name', 'user_context')
        user_context.setAttribute('value', 'default')
        variables.appendChild(user_context)

        effective_caller_id_name = doc.createElement('variable')
        effective_caller_id_name.setAttribute('name', 'effective_caller_id_name')
        effective_caller_id_name.setAttribute('value', callsign)
        variables.appendChild(effective_caller_id_name)

        effective_caller_id_number = doc.createElement('variable')
        effective_caller_id_number.setAttribute('name', 'effective_caller_id_number')
        effective_caller_id_number.setAttribute('value', number)
        variables.appendChild(effective_caller_id_number)

        outbound_caller_id_name = doc.createElement('variable')
        outbound_caller_id_name.setAttribute('name', 'outbound_caller_id_name')
        outbound_caller_id_name.setAttribute('value', '$${outbound_caller_name}')
        variables.appendChild(outbound_caller_id_name)

        outbound_caller_id_number = doc.createElement('variable')
        outbound_caller_id_number.setAttribute('name', 'outbound_caller_id_number')
        outbound_caller_id_number.setAttribute('value', '$${outbound_caller_id}')
        variables.appendChild(outbound_caller_id_number)

        if len(args) == 3:
            callgroup = doc.createElement('variable')
            callgroup.setAttribute('name', 'callgroup')
            callgroup.setAttribute('value', args[2])
            variables.appendChild(callgroup)

        xmlString = doc.childNodes[0].toprettyxml()
        if self.args.debug:
            print(xmlString)

        os.makedirs(os.path.dirname(userfile), exist_ok=True)
        with open(userfile, 'w') as file:
            #     # writexml(writer, indent="", addindent="", newl="", encoding=None)，
            #     doc.writexml(f, addindent='  ', newl='\n', encoding='utf-8')
            file.write(xmlString)
            message = f"Password: {password} Voicemail: {vmpassword}"
            self.logger.info(message)
            print(message)

    def list(self):
        userlists = [["电话号码", "呼号", "密码", "语音信箱", "呼叫组"]]

        directory = os.path.join(self.freeswitch, 'directory/default')
        for user in os.listdir(directory):
            tree = etree.parse(os.path.join(directory, user))
            params = tree.xpath('//include/user/params/param')
            # for param in params:
            #     # print(title)
            #     print(param.tag, param.get('name'), param.get('value'))
            password = params[0].get("value")
            vmpassword = params[1].get("value")

            variables = tree.xpath('//include/user/variables/variable')
            callgroup = ""
            for variable in variables:
                if variable.get("name") == 'accountcode':
                    number = variables[1].get("value")
                if variable.get("name") == 'effective_caller_id_name':
                    callsign = variables[3].get("value")
                if variable.get("name") == 'callgroup':
                    callgroup = variables[7].get("value")
            # number = variables[1].get("value")
            # number = variables[1].get("value")

            userlists.append([number, callsign, password, vmpassword, callgroup])

        table = Texttable(max_width=100)
        table.add_rows(userlists)
        print(table.draw())

    def show(self, number):
        # directory = os.path.join(self.freeswitch, 'directory/default')
        userfile = os.path.join(self.freeswitch, 'directory/default', f"{number}.xml")
        with open(userfile, 'r') as file:
            print(file.read())

    def remove(self, number):
        confirm = input(f"确认删除用户 {number} (Y/N): ")
        if confirm == 'n' or confirm == 'N':
            exit()
        userfile = os.path.join(self.freeswitch, 'directory/default', f"{number}.xml")
        if os.path.isfile(userfile):
            self.logger.info(f"REMOVE {number}")
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
