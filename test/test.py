from xml.dom.minidom import Document

doc = Document()
include=doc.createElement('include')
doc.appendChild(include)

user = doc.createElement('user')
user.setAttribute('id', '1000')
include.appendChild(user)

params = doc.createElement('params')
user.appendChild(params)

param1 = doc.createElement('param')
param1.setAttribute('name', 'password')
param1.setAttribute('value', '1000')
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
effective_caller_id_name.setAttribute('value', 'Extension 1000')
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

callgroup = doc.createElement('variable')
callgroup.setAttribute('name', 'callgroup')
callgroup.setAttribute('value', 'techsupport')
variables.appendChild(callgroup)

xmlString = doc.childNodes[0].toprettyxml()
print(xmlString)

xmlfile = '1000.xml'

with open(xmlfile, 'w') as file:
            # writexml(writer, indent="", addindent="", newl="", encoding=None)，
            # writer是文件对象, 必写参数，其余为可选参数
            # indent是每个tag前填充的字符，如：' '，则表示每个tag前有两个空格
            # addindent是每个子结点的缩近字符
            # newl是每个tag后填充的字符，如：'\n'，则表示每个tag后面有一个回车
    # doc.writexml(file, addindent='  ', newl='\n', encoding='utf-8',standalone=True)
    doc.version = ""
    doc.writexml(file, addindent='\t', newl='\n', encoding='')