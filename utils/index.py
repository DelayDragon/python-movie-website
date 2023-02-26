import re



# 得到链接中的数字编号
def get_number(value):
    number = re.compile(r'\d+').findall(value)[1]
    return number

# 字符串转base64
