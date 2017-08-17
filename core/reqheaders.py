from core import db_handler
import json

# split


# cookies.json
 # 数据库

# cookies.json = (sqlheper.get_one("select cookie from cookies.json where id = %s",(1)))[0]     # 返回的是列表所以取 0
# cookies.json = (sqlheper.get_one("select cookie from cookies.json where id = %s",(1)))[0]     # 返回的是列表所以取 0
# sqlheper.off()

def meso_url(id = None):
    # url = db_handler.read('./db/meso.json',True)
    if id == None:
        sqlheper=db_handler.Sqlheper()
        url = sqlheper.get_list("select id,url from meso_url",())
        sqlheper.off()
        return url
    else:
        sqlheper=db_handler.Sqlheper()
        url = sqlheper.get_one("select id,url from meso_url where id = %s",(id))
        sqlheper.off()
        return url


def cookies():
    # sqlheper = db_handler.Sqlheper()
    cookie_dict = db_handler.read('./conf/cookies.json',True)
    cookie = cookie_dict['cookie']
    # cookie_dict = json.dumps(cookie_json)
    # print(cookie_json,cookie_dict)
    # cookie = cookie_dict['cookie']
    # cookie = (sqlheper.get_one("select cookie from cookies.json where id = %s", (1)))[0]
    return cookie

def set_cookie(cookie):
    try:
        cookie_dict={'cookie':cookie}
        db_handler.write('./conf/cookies.json',cookie_dict,True)
        return True
    except Exception as e:
        print(e)
        return False

# 请求头
def headers():
    header={}
    header['Host']='buluo.qq.com'
    header['User-Agent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0'
    header['Accept']='application/json, text/plain, */*'
    header['Accept-Language']= 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    header['Accept-Encoding']= 'gzip, deflate, br'
    header['Referer']= 'https://buluo.qq.com/buluoadmin/home.html'
    header['Connection']= 'keep-alive'
    header['Pragma'] = 'no-cache'
    header['Cache-Control'] ='no-cache'
    cookie = dict(cookies_are=cookies())
    return header,cookie


if __name__ == '__main__':
    print(cookies())
    print(headers())
print(meso_url())