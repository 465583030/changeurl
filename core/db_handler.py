import pymysql
import json
from sqlalchemy.ext.declarative import declarative_base
#              导入的数据类型        String = char + varchar
from sqlalchemy import Column, SmallInteger, String, ForeignKey, UniqueConstraint, Index,Table,MetaData
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from conf import settings

host = settings.host
user = settings.user
pwd  = settings.password
db_dir = settings.database
coding = settings.CODING
db_port = settings.db_port


def read(path,json_data = False):
    '''
    打开文件
    :param path: 文件的路径
    :return: 返回文件内容
    '''
    f = open(path,'r',encoding=coding)
    if json_data:
        json_data = f.read()
        f.close()
        return json.loads(json_data)
    else:
        data = f.read()
        f.close()
        return data


def write(path,data,json_data = False):
    try:
        f = open(path, 'w', encoding=coding)
        if json_data:
            f.write(json.dumps(data))
            f.flush()

        else:
            f.close()
    except Exception as e :
        print(e)
        return False


'''
mysql 创建cookies 表 

create table cookies.json(
    id tinyint unsigned AUTO_INCREMENT PRIMARY KEY,cookie varchar(700) not null unique
    )engine=innodb DEFAULT charset=utf8;

'''
splice = {"default":[
    'http://htdata2.qq.com/cgi-bin/httpconn?htcmd=0x6ff0080&u=',
    'https://mobile.qzone.qq.com/details?_wv=3&g_f=2000000209&res_uin='
]}


# write('./db/meso.json',splice,True)

# 数据库操作
class Sqlheper():
    def __init__(self):
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=host, user=user, password=pwd, database=db_dir, charset=coding)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def off(self):
        self.cursor.close()
        self.conn.close()

    def get_list(self,sql,args):
        self.cursor.execute(sql,args)
        result = self.cursor.fetchall()
        return result

    def get_one(self,sql,args):
        self.cursor.execute(sql,args)
        result = self.cursor.fetchone()
        return result

    def modify(self,sql,args):
        self.cursor.execute(sql,args)
        self.conn.commit()



# engine = create_engine("mysql+pymysql://%s:%s@%s:%s/%s?charset=%s"%(user,pwd,host,db_port,db_dir,coding), max_overflow=100)
#
# metadata=MetaData(engine)
#
# cookies.json = Table('cookies.json',metadata,
#                 Column('id',SmallInteger,primary_key=True, autoincrement=True),
#                 Column('cookie',String(700),nullable = False ,unique=True),
#                 )
# #
# # cookies.json
# def get_cookie(args=None):
#     '''
#     查询cookie
#     :param args: 默认为None  挖个坑
#     :return:
#     '''
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     if args == None:
#         cookie = session.query(cookies.json).one()
#         session.close()
#         return cookie
#     else:
#         cookie = session.query(cookies.json).filter(cookies.json.id == args[0]).all()
#         session.close()
#         return cookie
#
# def edit_cookie(args):
#     cid = args[0]
#     cookie = args[1]
#     Session = sessionmaker(bind=engine)
#     session = Session()
#
#     session.query(cookies.json.id,cookies.json.cookie).filter(cookies.json.id == cid).update({'cookie':cookie})
#
#     session.commit()  # 提交修改
#     session.close()  # 关闭连接

# if __name__ == '__main__':
    # info = Sqlheper.get_one("select id,cookie from cookies.json where id = %s",(1))
    # print(info)
    # edit_cookie((1,'pgv_pvid=283938062; pt2gguin=o0757588331; ptcz=d38c4ced6d26ed9e0fcd52de2bf5bd92fd167a4f573c1356c8898c2a85f4cb42; o_cookie=835805290; pac_uid=1_757588331; RK=GdtDNRQae0; pgv_pvi=2446087168;'))
    # print(get_cookie())
    # print(get_cookie((1)))