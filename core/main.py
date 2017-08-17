#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket,json
import requests
import urllib.parse
import random
import string
import re
from conf import settings
from core import reqheaders
from core import db_handler

open_file = db_handler.read
# socket conf
ip_port = settings.ip_port
link_num = settings.link_num
coding = settings.CODING

url_head = 'https://buluo.qq.com/cgi-bin/bar/extra/gen_short_url?urls='

# 自定义请求头


# 请求头 json 序列化
# json_headers = json.dumps(headers)


def change(change_url,id=None):
    '''
    对 buluo.qq.com 发送 get 请求并返回响应的结果
    :param change_url: 需要转换的 url
    :return:    把转换后的结果返回
    '''
    headers, cookies = reqheaders.headers()
    meso_url = reqheaders.meso_url(id)
    print(meso_url)
    splice_url = ''.join(('["',meso_url['url'], change_url, '"]'))  # 拼接传送给 buluo.qq.com 的需要转换网址
    print(splice_url)
    encode_url = urllib.parse.quote(splice_url,coding)  # 把参数进行 url 编码
    url = ''.join((url_head, encode_url))  # 拼接 get 请求 url
    print(url)
    print(cookies)
    req = requests.get(url, cookies=cookies, headers=headers)  # 发送 get 请求并 赋值给 req
    url = req.json()  # 获取响应的 json
    deal_url = retMsg(url)
    return deal_url

# 转换成功返回的信息
f = {"result": {"ls": [{"url_code": "http://url.cn/2KG1QIG",
                             "url": "http://htdata2.qq.com/cgi-bin/httpconn?htcmd=0x6ff0080&u=http://www.baidu.com"}]},
          "retcode": 0}


def retMsg(info):
    url = {}
    if info['retcode'] == 0:
        url['retcode'] = 0
        url['url_code'] = info['result']['ls'][0]['url_code']
        return url
    else:
        return info

def run():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(ip_port)
    sock.listen((link_num))

    while True:
        conn, addr = sock.accept()
        request = conn.recv(1024)
        info= split_request(request,conn) # 分割请求函数分割请求，并获取请求方式（get/post），url ，参数
        if info[0]['status'] == False:
            conn.close()
            continue
        else:
            # url 处理逻辑
            # if info[2].startswith("/setcookie/"):
            if info[2] == '/setcookie.html':
                res=setcookie(request,conn,info)
                send(conn,res)
            if info[2].startswith('/?url='):
                url = info[2][6:]
                dict_url = change(url)
                json_url = json.dumps(dict_url)
                send(conn,json_url)
            if info[2] == '/url.html':
                res = diy_url(request,conn,info)
                # if res == False:
                #     continue
                #     conn.close()
                # else:
                send(conn,res)
            else:
                # conn.send(b'HTTP/1.1 404 no\r\n\r\n')  # 响应头
                # conn.send(b'404')  # 响应内容
                conn.close()

def diy_url(request,conn,req_head):
    info = {}
    info['url'] = req_head[2]
    status, method, url, protocal,bodys=split_request(request,conn)
    if method == "GET" and url == '/url.html':
        meso_url = reqheaders.meso_url()
        info['meso_url'] = meso_url
        temp_html = open_file('templates/url.html')
        return render_hrml(temp_html,info)
    else:
        print(request)
        temp = re.split('[&]',bodys,1)
        if len(temp) > 1:
            tmp_id,tmp_url = temp
            tmp,id = re.split('[=]',tmp_id,1)
            tmp,url = re.split('[=]',tmp_url,1)
            url = urllib.parse.unquote(url)
            if url.startswith("http"):
                dict_url =change(url,id)
                print(dict_url)
                if dict_url['retcode'] == 0:
                    status['url'] = dict_url['url_code']
                    return json.dumps(status)
                else:
                    status['status'] = False
                    status['msg']   = dict_url
                    return json.dumps(dict_url)
            else:
                status['status'] = False
                status['msg']   = 'URL 必须以 http:// 开头!'
                return json.dumps(status)
        else:
            status['status'] = False
            status['msg'] = '服务器未收到URL...'
            return json.dumps(status)



def split_request(request,conn):
    status = {'status': True, 'msg': None}
    try:
        tmp_request = str(request, encoding=coding)
        heads, bodys = tmp_request.split('\r\n\r\n')  # 分割请求头
        tmp_list = heads.split('\r\n')  # 分割请求体
        method, url, protocal = tmp_list[0].split(' ')  # 分割请求，并获取请求方式（get/post），url ，参数
        return status,method,url,protocal,bodys
    except Exception as e:
        print('split_request',e)
        status['status'] = False
        status['msg'] = e
        return (status)

def send(conn,info):
    try:
        conn.send(b'HTTP/1.1 200 OK\r\n\r\n')  # 响应头
        conn.send(bytes(info,encoding=coding))  # 响应内容
        # conn.send(info)  # 响应内容
        conn.close()
        return (True)
    except Exception as e:
        conn.close()
        print('send',e)
        return (False,e)

def setcookie(request,conn,req_head):
    info = {}
    info['url'] = req_head[2]
    status, method, url, protocal,bodys=req_head
    if method == 'GET' and url == "/setcookie.html":   #  设置 cookies.json 页面
        cookie = reqheaders.cookies()
        info['cookie'] = cookie
        # 渲染 html
        tmp_html = open_file('templates/setcookie.html')
        return render_hrml(tmp_html,info)
    else:   # 收到客户端的post请求更改 cookie
        # print('setcookie',status, method, url, protocal,bodys)
        tmp_key,tmp_cookie = re.split('[&]',bodys,1)
        kname,key = re.split('[=]',tmp_key,1)
        cname,cookie = re.split('[=]',tmp_cookie,1)
        # print(key,cookie)
        if len(key) > 0 and cookie != None and key == 'qweasdzxc':
            # 更改 cookie
            reqheaders.set_cookie(cookie)
            status['status'] = True
            status['msg'] = cookie
            return json.dumps(status)
        else:
            status['status'] = True
            status['msg'] = 'key or cookie Not empty! or key error'
            return json.dumps(status)

def render_hrml(html,info):
    '''
    渲染网页
    :param html: 需要渲染的网页
    :param info: 渲染的内容
    :return: 返回渲染后的 html 
    '''
    from jinja2 import Template  # 导入模版渲染模块
    template = Template(html)
    html = template.render(info=info)  # 模版渲染
    return html


def random_letter(length=20):
    # 产生随机字符串 作为认证key   后续可以加md5 salt
    name=''.join([random.choice(string.ascii_lowercase+string.digits+string.ascii_uppercase) for i in range(length)])
    return name

# print(random_letter())