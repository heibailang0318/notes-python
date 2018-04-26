# coding=utf-8
import metestore

from pyhive import hive

# 连接元数据库，获得所需要的表
mete = metestore.Metestore()
table = input('输入表：')
rows = mete.show_table(table)   # o_m_lnktbl
col = tuple(rows['COLUMN'])


while True:
    pk = input('输入主键用逗号(,)间隔：').split(',')
    x = [True for i in tuple(pk) if i in col]  # 过滤正确字段
    if x:
        break;
while True:
    incr = input('输入增量字段：')
    x = [True for i in incr if i in col and i not in pk]     # 过滤正确字段
    if x:
        break;
lnk = tuple([i for i in col if i not in pk])
print('主键：', pk, '  增量字段：', incr, '  拉链字段：', lnk,'\n')

# def genderSql(table,pk,incr,lnk):

tmp = list(rows['COLUMN'] + ' ' + rows['TYPE'] +' COMMENT \'' + rows['COMMENT']+'\'')
sql1='CREATE TABLE ' + table + '_tmp (' + ', '.join(tmp)+') ROW FORMAT DELIMITED FIELDS TERMINATED BY \'\\001\' STORED AS TEXTFILE;'
sql2='CREATE TABLE ' + table + '_his (' + ', '.join(tmp)+ ', start_date varchar(10) COMMENT \'拉链起始日期\', end_date varchar(10) COMMENT \'拉链最新日期\' ) ' \
                                                          'ROW FORMAT DELIMITED FIELDS TERMINATED BY \'\\001\' STORED AS TEXTFILE;'
sql3 = 'INSERT OVERWRITE TABLE ' + table + '_tmp SELECT ' + ', '.join(col) + ' FROM ' + table + ' WHERE ' + incr + ' >= date_add(CURRENT_DATE,-1) and ' + incr + ' < CURRENT_DATE;'
sql4 = 'INSERT OVERWRITE TABLE ' + table + '_his SELECT ' + ', '.join(['t1.'+i for i in col]) +  \
        ', t1.start_date, case when t1.end_date=\'2099-01-01\' and concat('+',\'_\','.join(['t2.'+i for i in lnk])+') is not null then date_add(CURRENT_DATE,-1) else t1.end_date end as end_date FROM ' + \
        table + '_his t1 left join ' + table + '_tmp t2 on concat('+',\'_\','.join(['t1.'+i for i in pk])+') = concat('+',\'_\','.join(['t2.'+i for i in pk])+   \
        ') union all select '+', '.join(col) + ', CURRENT_DATE as start_date, \'2099-01-01\' as end_date from '+table+'_tmp'

print('-- 生成拉链临时表与拉链表：\n', sql1, '\n', sql2)
print('-- 每日拉链ETL逻辑：\n',sql3,'\n',sql4)


mete.close()
