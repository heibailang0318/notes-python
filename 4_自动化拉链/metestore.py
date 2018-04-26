# coding=utf-8
'''数据库：hive3
用户名：hive3
密码：ChSqFxS5wt
端口：7432
'''

import psycopg2
import pandas as pd


class Metestore:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(database='', user='', password='', host='',
                                         port=)
        except Exception as e:
            print(e)
        else:
            print('--------Metestore连接成功--------')
            self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()
        print('\n--------Metestore连接关闭--------')

    def show_table(self, tbl_name):
        self.cur.execute('''
        select a."TBL_NAME", b."COLUMN_NAME", b."TYPE_NAME", b."COMMENT",c."PART_NAME"
        from "public"."TBLS" a join "public"."COLUMNS_V2" b
            on a."TBL_ID"=b."CD_ID"
        left join "public"."PARTITIONS" c
            on a."TBL_ID"=c."TBL_ID"
	    where a."TBL_NAME"=\'''' + tbl_name + '\''
                         )
        rows = pd.DataFrame(self.cur.fetchall(), columns=['TABLE','COLUMN', 'TYPE', 'COMMENT','PART_NAME']).fillna('')
        # print('表 '+ tbl_name +' 结构如下：')
        # print(rows, '\n')

        # for row in rows:
        #     print('TBL = ', row[0], ', COLUMN = ', row[1], ', TYPE = ', row[2],', COMMENT = ', row[3])
        return rows


if __name__ == "__main__":
    mete = Metestore()
    mete.show_table('a') # o_m_lnktbl
    mete.close()
