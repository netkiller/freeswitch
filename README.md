# freeswitch 用户管理

## 安装依赖

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

## 帮助信息

```shell
PS D:\GitHub\freeswitch> python.exe .\freeswitch.py -h
usage: freeswitch.py [-h] [-a <number> <callsign> <callgroup> [<number> <callsign> <callgroup> ...]] [-r 1000] [-l] [-s 1000] [-d]

FreeSWITCH 用户管理工具

options:
  -h, --help            show this help message and exit
  -a <number> <callsign> <callgroup> [<number> <callsign> <callgroup> ...], --add <number> <callsign> <callgroup> [<number> <callsign> <callgroup> ...]
                        添加用户
  -r 1000, --remove 1000
                        删除用户
  -l, --list            列出用户
  -s 1000, --show 1000  查看用户
  -d, --debug           调试模式

Author: netkiller - https://www.netkiller.cn/linux/

```

## 添加用户

```shell
PS D:\GitHub\freeswitch> python.exe .\freeswitch.py -a 1000 BG7NYT admin 
```

## 查看用于

```shell
PS D:\GitHub\freeswitch> python.exe .\freeswitch.py -s 1000             
<include>
        <user id="1000">
                <params>
                        <param name="password" value="B5AbNCYj"/>
                        <param name="vm-password" value="1000"/>
                </params>
                <variables>
                        <variable name="toll_allow" value="domestic,international,local"/>
                        <variable name="accountcode" value="1000"/>
                        <variable name="user_context" value="default"/>
                        <variable name="effective_caller_id_name" value="BG7NYT"/>
                        <variable name="effective_caller_id_number" value="1000"/>
                        <variable name="outbound_caller_id_name" value="$${outbound_caller_name}"/>
                        <variable name="outbound_caller_id_number" value="$${outbound_caller_id}"/>
                        <variable name="callgroup" value="admin"/>
                </variables>
        </user>
</include>
```

## 列出所有用户

```shell
PS D:\GitHub\freeswitch> python.exe .\freeswitch.py -l                  
+----------+--------+----------+----------+--------+
| 电话号码 |  呼号  |   密码   | 语音信箱 | 呼叫组 |
+==========+========+==========+==========+========+
| 1000     | BG7NYT | HbM3imgb | 2031     | admin  |
+----------+--------+----------+----------+--------+
| 1003     | BG7NYT | 1u3Fc6t4 | 5927     | 33333  |
+----------+--------+----------+----------+--------+

```

## 删除用户

```shell
PS D:\GitHub\freeswitch> python.exe .\freeswitch.py -r 1000
```