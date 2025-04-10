# freeswitch 用户管理

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
1000.xml
```

## 删除用户

```shell
PS D:\GitHub\freeswitch> python.exe .\freeswitch.py -r 1000
```