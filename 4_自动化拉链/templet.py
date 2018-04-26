# coding=utf-8


class Templet:
    def __init__(self,mete):
        self.mete = mete

    def tpl_incr(self,row):

        tableinfo = self.mete.show_table(row[0])  # o_m_lnktbl
        table = row[0]
        pk = row[1].split(',')
        incr = row[2]

        col = list(tableinfo['COLUMN'])
        lnk = tuple([i for i in col if i not in pk])
        lnk_col=',\'_\','.join(['t2.' + i for i in lnk])

        tmp = ', '.join(list(tableinfo['COLUMN'] + ' ' + tableinfo['TYPE'] + ' COMMENT \'' + tableinfo['COMMENT'] + '\''))
        t1_pkcol='concat(' + ',\'_\','.join(['t1.' + i for i in pk])+')'
        t2_pkcol='concat(' + ',\'_\','.join(['t2.' + i for i in pk])+')'
        t1_col=', '.join(['t1.' + i for i in col])

        sql1 = 'CREATE TABLE ' + table + '_his (' + tmp + ', start_date varchar(10) COMMENT \'拉链起始日期\', end_date varchar(10) COMMENT \'拉链最新日期\' ) ' \
                   'ROW FORMAT DELIMITED FIELDS TERMINATED BY \'\\001\' STORED AS TEXTFILE;'
        sql2= 'INSERT OVERWRITE TABLE ' + table + '_his SELECT distinct ' + t1_col + ', \'2000-01-01\' as start_date, \'2099-01-01\' as end_date FROM ' + table+ ';'

        sql3 = 'CREATE TABLE ' + table + '_tmp as SELECT distinct ' + t1_col + ' FROM ' + table + ' WHERE ' + incr + ' = date_add(CURRENT_DATE,-1);'

        sql4 = 'INSERT OVERWRITE TABLE ' + table + '_his SELECT ' + t1_col + \
               ', t1.start_date, case when t1.end_date=\'2099-01-01\' and ' + lnk_col + ' is not null then date_add(CURRENT_DATE,-2) else t1.end_date end as end_date FROM ' + \
               table + '_his t1 left join ' + table + '_tmp t2 on ' + t1_pkcol + ' = ' + t1_pkcol + \
               ' union all select ' + t1_col + ', date_add(CURRENT_DATE,-1) as start_date, \'2099-01-01\' as end_date from ' + table + '_tmp t1;'

        # mete.close()
        row = '\n-- 表：' + str(table) + '\n-- 处理方式：增量' + '\n-- 主键字段：' + str(pk) +'\n-- 增量字段：' + str(incr) +'\n-- 拉链字段：' + str(lnk) + \
                '\n-------------------------------生成语句：-------------------------------'+\
                '\n-- 创建拉链表：\n' + sql1 + \
                '\n-- 初始化拉链表：\n' + sql2+ \
                '\n----- 每日拉链ETL逻辑：-----'+\
                '\n-- 1.存储增量数据：\n' + sql3 +\
                '\n-- 2.拉链逻辑：\n' + sql4 +'\n\n'
        return row

    def tpl_full(self,row):
        tableinfo = self.mete.show_table(row[0])  # o_m_lnktbl
        table = row[0]
        col = list(tableinfo['COLUMN'])
        if row[1] == '':  # 没主键按照全字段拉链
            pk = col
            lnk = col
        else:  # 有主键按非主键拉链
            pk = row[1].split(',')
            lnk = tuple([i for i in col if i not in pk])

        tmp = ', '.join(list(tableinfo['COLUMN'] + ' ' + tableinfo['TYPE'] + ' COMMENT \'' + tableinfo['COMMENT'] + '\''))
        t1_pkcol='concat(' + ',\'_\','.join(['t1.' + i for i in pk])+')'
        t2_pkcol='concat(' + ',\'_\','.join(['t2.' + i for i in pk])+')'
        t1_col=', '.join(['t1.' + i for i in col])

        sql1 = 'CREATE TABLE ' + table + '_his (' + tmp + ', start_date varchar(10) COMMENT \'拉链起始日期\', end_date varchar(10) COMMENT \'拉链最新日期\' ) ' \
                   'ROW FORMAT DELIMITED FIELDS TERMINATED BY \'\\001\' STORED AS TEXTFILE;'
        sql2 = 'INSERT OVERWRITE TABLE ' + table + '_his SELECT distinct ' + t1_col + ', \'2000-01-01\' as start_date, \'2099-01-01\' as end_date FROM ' + table + ';'

        sql3 = 'CREATE TABLE ' + table + '_tmp as SELECT * from (select case ' \
            'when ' + t1_pkcol + ' is not null and ' + t2_pkcol + ' is null then \'I\' ' \
            'when ' + t1_pkcol + ' is null and ' + t2_pkcol + ' is not null then \'D\' ' \
            'when ' + t1_pkcol + ' is not null and '+ t2_pkcol +' is not null and ' \
                        + t1_pkcol +' <> '+ t2_pkcol +' then \'U\' else \'N\' end as dtype, ' \
            + t1_col+', '+t1_pkcol +' as t1_pkcol'+', '+t2_pkcol +' as t1_pkcol from (' \
            'select distinct * from '+table+' where partition_dt=date_add(CURRENT_DATE,-1)) t1 full join (select distinct * from '\
            +table+' where partition_dt=date_add(CURRENT_DATE,-2)) t2 on '+t1_pkcol+'='+t2_pkcol+') t where dtype<>\'N\';'

        sql4 = 'INSERT OVERWRITE TABLE ' + table + '_his SELECT ' + t1_col + \
               ', t1.start_date, case when t1.end_date=\'2099-01-01\' and ' + t2_pkcol + ') is not null then date_add(CURRENT_DATE,-2) else t1.end_date end as end_date FROM ' + \
               table + '_his t1 left join ' + table + '_tmp t2 on ' + t1_pkcol + ' = ' + t2_pkcol + \
               ' union all select ' + t1_col + ', date_add(CURRENT_DATE,-1) as start_date, \'2099-01-01\' as end_date from ' + table + '_tmp t1 where dtype <> \'D\';'

        # mete.close()
        row = '\n---- 表：' + str(table) + '\n-- 处理方式：全量\n-- 主键字段：' + str(pk) +'\n-- 拉链字段：' + str(lnk) + \
                '\n-------------------------------生成语句：-------------------------------'+\
                '\n-- 创建拉链表：\n' + sql1 + \
                '\n-- 初始化拉链表：\n' + sql2+ \
                '\n----- 每日拉链ETL逻辑：-----'+\
                '\n-- 1.存储增量数据：\n' + sql3 +\
                '\n-- 2.拉链逻辑：\n' + sql4 +'\n\n'
        return row

if __name__ == '__main__':
    # tpl_incr(['o_m_order', 'order_id', 'update_time'])
    templet=Templet()
    templet.tpl_full(['o_m_lnktbl2', '', '','full'])
