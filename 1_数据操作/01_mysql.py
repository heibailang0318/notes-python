# coding=utf-8
import pymysql
#获取连接
# db = pymysql.connect("localhost","testuser","test123","TESTDB" )
class Mysql(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host=' ',
                port= ,
                user=' ',
                passwd=' ',
                db=' ',
                charset='utf8'
            )
        except Exception as e:
            print(e)
        else:
            print('连接成功')
            self.cur = self.conn.cursor()

    def create_table(self):
        sql = '''
            drop table if exists testtb;
            create table testtb(id int, name varchar(10),age int);
            '''
        res = self.cur.execute(sql)
        print(res)

    def close(self):
        self.cur.close()
        self.conn.close()

    def add(self):  # 增
        sql = 'insert into testtb values(1,"Tom",18),(2,"Jerry",16),(3,"Hank",24)'
        res = self.cur.execute(sql)
        if res:
            self.conn.commit()
        else:
            self.conn.rollback()
        print(res)

    def rem(self):  # 删
        sql = 'delete from testtb where id=1'
        res = self.cur.execute(sql)
        if res:
            self.conn.commit()
        else:
            self.conn.rollback()
        print(res)

    def mod(self):  # 改
        sql = 'update testtb set name="Tom Ding" where id=2'
        res = self.cur.execute(sql)
        if res:
            self.conn.commit()
        else:
            self.conn.rollback()
        print(res)

    def show(self):  # 查
        sql = 'select * from testtb'
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            print(i)

if __name__ == "__main__":
    mysql = Mysql()
    mysql.create_table()
    mysql.add()
    mysql.mod()
    mysql.rem()
    mysql.show()
    mysql.close()