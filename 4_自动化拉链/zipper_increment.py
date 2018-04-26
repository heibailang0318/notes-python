#coding:utf-8
import pymysql
import re
import os
import time
class ConnInfo(object):
    def __init__(self,host="",user="",passwd="",db=""):
        self.host=host
        self.user=user
        self.passwd=passwd
        self.db=db
class GetFile(object):
    def __init__(self,pathname,pathfile):
        self.pathname=pathname
        self.pathfile=pathfile
    def getfile(self):
        os.chdir(self.pathname)
        path=os.getcwd()
        sfile=str(path) +"\\"+self.pathfile
        return sfile

class app(object):
    def __init__(self,conninfo=ConnInfo()):
        self.conninfo=conninfo
        self.connchild=pymysql.connect(conninfo.host,conninfo.user,conninfo.passwd,conninfo.db)
    def getConn(self):
        return pymysql.connect(self.conninfo.host,self.conninfo.user,self.conninfo.passwd,self.conninfo.db)
    def getsql(self):
        sql="SELECT tab_name,md5_string,join_field,partition_field,order_field,chipped_filed,mode_choice FROM zipper_config_repository WHERE flag=1"
        #sql="insert into zipper_log "\
        #    "values('ods.o_m_chrprj_t_org_dq','ods.o_m_chrprj_t_org_dq_his','ods.o_m_chrprj_t_org_dq_update','1','E:\mypython\hive_sql\ods.o_m_chrprj_t_org_dq_20180319163338.sql','2018-03-19 16:33:38','1');"
        #print(sql)
        conn = self.getConn()
        cursor = conn.cursor()
        cursor.execute(sql)
        line = cursor.fetchall()
        return line
    def get_config(self):
        config_info=self.getsql()
        for tab_name,md5_string,join_field,partition_field,order_field,chipped_filed,mode_choice  in config_info:
            os.chdir("E:\\mypython\\hive_sql")
            filepath=os.getcwd()
            file_name=tab_name+"_"+time.strftime("%Y%m%d%H%M%S", time.localtime())+".sql"
            filepathname=filepath+"\\"+file_name
            #print(filepathname)
            with open(file_name,"a",encoding='utf-8') as file:
                #增量update表字段拼接
                #tab_name_update=tab_name+"_update"
                tab_name_update="tmp.tmp_"+tab_name.replace("ods.","")+"_update"
                comment="-- 增量数据每次来的切片\n"
                space="\n      "
                int_tab_field=space+join_field+space+","+md5_string.replace(",",space+",")
                #print(int_tab_field)
                #"insert into table "+tab_name_update+" partition (partition_mt='${#date(0,0,-1):yyyyMM#}')\n"\
                tab_update_sql= "drop table if exists "+tab_name_update+";\ncreate table "+tab_name_update+" as\n"\
                               "select "+int_tab_field+space+",md5\nfrom\n(\nselect "+int_tab_field+space+",get_md5_string(CONCAT_WS("+md5_string+")) as md5"\
                               +space+",row_number()over(partition by "+partition_field+" order by "+order_field+" desc) rm\n"\
                               " from "+tab_name+"\nwhere "+chipped_filed+" between '${#date(0,0,-1):yyyyMM01#}'\n  and '${#date(0,0,-1):yyyyMMdd#}'\n) x\nwhere rm=1\n;\n"
                print(tab_update_sql)
                file.write(comment+tab_update_sql)

                #月初初始化脚本
                tab_name_tmp="tmp.tmp_"+tab_name.replace("ods.","")
                tab_name_his=tab_name+"_his"
                comment="-- 月初1号初始化数据\n"
                tab_month_inc_sql="drop table if exists "+tab_name_tmp+";\ncreate table "+tab_name_tmp+"\nas\nselect "+int_tab_field+space+",'${#date(0,0,-1):yyyy-MM-01#}' start_time" \
                                  +space+",get_md5_string(CONCAT_WS("+md5_string+")) as md5\n from "+tab_name_his+"\nwhere partition_mt='${#date(0,0,-1):yyyyMM#}'\n and end_time=LAST_DAY('${#date(0,0,-1):yyyy-MM-dd#}')\n;\n"
                #print(tab_month_inc_sql)
                file.write(comment+tab_month_inc_sql)

                #增量与全量合并 如1号数据和上月数据合并
                comment="-- 增量与全量合并\n"
                tab_his_sql="insert into table "+tab_name_his+" partition (partition_mt='${#date(0,0,-1):yyyyMM#}')\n"\
                            "select "+space+"a."+join_field+space+",a."+md5_string.replace(",",space+",a.")+space+",a.start_time"+space+",case when b."+join_field+" is not null then '${#date(0,0,-1):yyyy-MM-dd#}' else a.end_time end\n"\
                            "from\n"+tab_name_tmp+" A\nleft join\n"+tab_name_update+" B\non A."+join_field+"=B."+join_field+" and a.md5=b.md5 \nunion all\n"\
                            #-- union all完成
                #print(tab_his_sql)
                #新增的全部开链
                tab_his_sql= tab_his_sql+"select"+int_tab_field+space+",start_time"+space+",end_time \nfrom "\
                             "\n(select "+int_tab_field+space+",'${#date(0,0,-1):yyyy-MM-dd#}' start_time"+space+",LAST_DAY('${#date(0,0,-1):yyyy-MM-dd#}') end_time"\
                             +space+",row_number()over(partition by "+partition_field+" order by "+order_field+" desc) rm\n"\
                             "from "+tab_name_update+"\n"\
                             ") x \nwhere rm=1\n;"
                #print(tab_his_sql)
                file.write(comment+tab_his_sql)

                #生成完成,输入到目标表
                con_insertlog=self.getConn()
                insert_log_sql="insert into zipper_log \n"\
                               "values('"+tab_name+"','"+tab_name_his+"','"+tab_name_update+"','1','"+filepathname+"','"+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+"','1');"
                #print(insert_log_sql)
                cursor_log = con_insertlog.cursor()
                cursor_log.execute(insert_log_sql)
                con_insertlog.commit()
                cursor_log.close()
                con_insertlog.close()

if __name__ == "__main__":
    call_app=app().get_config()
    #call_app=app().getsql()

