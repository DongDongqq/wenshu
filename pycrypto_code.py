# -*- coding: utf-8 -*-
"""
    @author: 王帅帅
    @project: huijiyunAPP
    @file: pycrypto_code.py
    @time: 2019/8/20/020 11:31
    @desc:
"""
# TODO pip install pycryptodome

from binascii import b2a_base64, a2b_base64
from Crypto.Cipher import DES3
import base64
from urllib.parse import unquote_plus, quote
import re
BS = DES3.block_size
import json
import requests
import re


def pad(s):
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

#加密

def encrypt(text,key,ivs):
    text = pad(text).encode('utf-8')
    iv = ivs.encode('utf-8')
    cryptor = DES3.new(key, DES3.MODE_CBC, iv)
    # self.iv 为 IV 即偏移量
    x = len(text) % 8
    if x != 0:
        text = text + '\0' * (8 - x)  # 不满16，32，64位补0
    # print(text)
    ciphertext = cryptor.encrypt(text)
    return base64.standard_b64encode(ciphertext).decode("utf-8")
    # return ciphertext.decode('utf-8')

Key = "FkD8RAPXoAxb3iSTISKbFLty"# TODO 秘钥
iv = '20190930'.encode('utf-8')
# 解密
def decrypt_des(text,Key):  # TODO DES参数解密
    generator = DES3.new(Key, DES3.MODE_CBC,iv)
    de_text = base64.standard_b64decode(text)
    plain_text = generator.decrypt(de_text)
    # print(plain_text.decode('gbk'))
    # plain_text = str(plain_text).replace(r'\x07','').replace(r'\x06', '').replace(r'\x05', '').replace(r'\x04', '').replace(r'\x03', '').replace(r'\x02', '').replace(r'\x01', '').replace(r'\x08', '').replace(r'\x09', '')
    # print(eval(plain_text))
    return plain_text.decode('utf-8')


if __name__ == '__main__':
    result= "lnUUa8WgglNXOC8zGm7NBILXRpzKp4TymGtSLbtbNi2bpwk7sx7IFe34ZDVtQcb596pX6SK2zmZB/n+khsP+ke+dY01NznbCkSVGtHef2QdajOu6YNeElyccFzBweV7kgMiq5DlyGTL7r6Vn5GIR4Ja7YmLF+Y+j/6ylq9016LSJ+WAzoR3VBOWmvHhuYeG03/Nk3GgRVXWgd3HkQylKY4ww1KJkPe9l7i+OjBPk1JVd1hHFt4SZyFQqwv6BoLJDOJfFKIGRldPRlAdqlNp3MoJz5K0Nvr5AilgRTc9UlTsafvyKiZzL2i2H9+KNugJZSu7ffK30OWrbqUsDwWKXwvrat18yfrzEWpCR9jvOAJrwHF07nkz5aGVSh8Yrr9jhgkszCGNvZwxMx02Roz4ecI17YmRf68bGUtY0M4hygKITqKcR2Elda83qGjrvtnkQnhLbKkbEFN4Y9ha4sCS5rAajaE9f+abbgtPJfdBIwzMbo7d+fJ9QeqmJk9OH99f5"
    data = decrypt_des(result,'4orQqB7pqShAFtvIhAIxv6qL')
    print(data)
