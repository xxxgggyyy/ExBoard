# -*- coding: utf-8 -*-
import random
import string
from Crypto.Cipher import ChaCha20
import base64
import json


#加密算法密钥
key=b'\xd9[\x13\xcdGT\x87\x02\xf9\xd6\xd2\xce\x89\r\x86\xe43\xd0\x06\x14\x1dg\n5\xd8\xfc\xdc2\x93\xb63)'


#最好是处理utf-8的 另外数字加密会被变为数字字符串再加密
def encrypt(plaintext):
    if not isinstance(plaintext,str):
        plaintext=str(plaintext)
    ptext=bytes(plaintext,encoding='utf-8')
    cipher = ChaCha20.new(key= key)
    return cipher.nonce+cipher.encrypt(ptext)

def decrypt(secrettext):
    msg_nonce=secrettext[:8]
    ciphertext=secrettext[8:]
    cipher=ChaCha20.new(key=key,nonce=msg_nonce)
    return str(cipher.decrypt(ciphertext),encoding='utf-8')


#生成随机字符串
def randomStr(num):
    return ''.join(random.sample(string.ascii_letters + string.digits, num))


#此加密仅用于peach2中数据传输格式
#加密字典 json加密为"{'content:'密文'}" 此加密基于上面的加密
def encrypt_json(data):
    re={}
    data_json=json.dumps(data)
    sec=encrypt(data_json)
    b64code=base64.b64encode(sec)
    re['content']=str(b64code,encoding='utf-8')
    return json.dumps(re)

#解密上面加密的json为字典
def decrypt_json(se_data_json):
    data_json=json.loads(se_data_json)
    sec=data_json['content']
    b64plain=base64.b64decode(bytes(sec,encoding='utf-8'))
    return json.loads(decrypt(b64plain))


#用于解析收到的json
def ParseData(data):
    try:
        return ('success',decrypt_json(data))
    except json.decoder.JSONDecodeError:
        return ('failed','json格式错误')
