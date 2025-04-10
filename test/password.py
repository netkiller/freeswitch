import random
import string

# 定义所有可能的字符，包括大小写字母和数字
all_characters = string.ascii_letters + string.digits

# 生成 8 个长度为 8 的密码

password = ''.join(random.choice(all_characters) for i in range(8))
print(password)
