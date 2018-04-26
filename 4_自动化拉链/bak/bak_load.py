#coding=utf-8
import metestore
import xlrd


def load_excel(file=u'添加拉链的表.xlsx'):
    xlsx = xlrd.open_workbook(file)
    sheet_names = xlsx.sheet_names()
    print('sheet名:',sheet_names[0])
    sheet = xlsx.sheet_by_name(sheet_names[0])
    return sheet

def genderFile(sheet):
    file = open('file/genderFile.sql', 'w', encoding='utf-8')
    for r in range(1,sheet.nrows):
        # 获取列内容
        row = sheet.row_values(r)
        print('第%s行:' %(r),row)
        tableinfo = mete.show_table(row[0])  # o_m_lnktbl
        table = row[0]
        pk = row[1].split(',')
        incr = row[2]
        col = list(tableinfo['COLUMN'])
        lnk = tuple([i for i in col if i not in pk])


        # 校验pk，incr
        # for i in tuple(pk):
        #     if i not in col:
        #         print('%s字段在表%s中不存在！'%(i,table))
        #         break


        tmp = list(tableinfo['COLUMN'] + ' ' + tableinfo['TYPE'] + ' COMMENT \'' + tableinfo['COMMENT'] + '\'')
        sql1 = 'CREATE TABLE ' + table + '_tmp (' + ', '.join(
            tmp) + ') ROW FORMAT DELIMITED FIELDS TERMINATED BY \'\\001\' STORED AS TEXTFILE;'
        sql2 = 'CREATE TABLE ' + table + '_his (' + ', '.join(
            tmp) + ', start_date varchar(10) COMMENT \'拉链起始日期\', end_date varchar(10) COMMENT \'拉链最新日期\' ) ' \
                   'ROW FORMAT DELIMITED FIELDS TERMINATED BY \'\\001\' STORED AS TEXTFILE;'
        sql3 = 'INSERT OVERWRITE TABLE ' + table + '_tmp SELECT ' + ', '.join(
            col) + ' FROM ' + table + ' WHERE ' + incr + ' >= date_add(CURRENT_DATE,-1) and ' + incr + ' < CURRENT_DATE;'
        sql4 = 'INSERT OVERWRITE TABLE ' + table + '_his SELECT ' + ', '.join(['t1.' + i for i in col]) + \
               ', t1.start_date, case when t1.end_date=\'2099-01-01\' and concat(' + ',\'_\','.join(['t2.' + i for i in
                                                                                                     lnk]) + ') is not null then date_add(CURRENT_DATE,-1) else t1.end_date end as end_date FROM ' + \
               table + '_his t1 left join ' + table + '_tmp t2 on concat(' + ',\'_\','.join(
            ['t1.' + i for i in pk]) + ') = concat(' + ',\'_\','.join(['t2.' + i for i in pk]) + \
               ') union all select ' + ', '.join(
            col) + ', CURRENT_DATE as start_date, \'2099-01-01\' as end_date from ' + table + '_tmp;'


        # print('table:',table)
        # print('pk:',pk)
        # print('incr:',incr)
        # print('col:',col)
        # print('lnk', lnk)
        # print('-- 生成拉链临时表与拉链表：\n', sql1, '\n', sql2)
        # print('-- 每日拉链ETL逻辑：\n', sql3, '\n', sql4)

        # file.write('---- 表：' + str(table) + '\n' + '-- 主键字段：' + str(pk) +'\n' + '-- 增量字段：' + str(incr) +'\n' + '-- 拉链字段：' + str(lnk) + '\n')
        # file.write('-- 生成拉链临时表与拉链表：' + '\n' + sql1 + '\n' + sql2+ '\n' + '-- 每日拉链ETL逻辑：' + '\n' + sql3 + '\n' + sql4+'\n\n')



if __name__ == '__main__':
    mete = metestore.Metestore()
    sheet=load_excel()
    genderFile(sheet)
    mete.close()