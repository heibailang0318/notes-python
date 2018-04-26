# coding=utf-8
import metestore
import templet
import xlrd

excel=u'file/添加拉链的表.xlsx'
xlsx = xlrd.open_workbook(excel)
sheet_names = xlsx.sheet_names()
sheet = xlsx.sheet_by_name(sheet_names[0])

file = open('file/genderFile.sql', 'w', encoding='utf-8')
mete = metestore.Metestore()
templet=templet.Templet(mete)
for r in range(1, sheet.nrows):
    row = sheet.row_values(r)
    if row[0].strip() != ''  :    # 剔除空表
        if row[3]=='incr':
            file.write('-- 第%s行:' % (r) +str(row) + templet.tpl_incr(row))
        elif row[3]=='full':
            file.write('-- 第%s行:' % (r) + str(row) + templet.tpl_full(row))
        else:
            file.write('-- 第%s行type列有误: ' % (r) + str(row)+'\n')
    else:
        file.write('-- 第%s行table列有误: ' % (r)+ str(row)+'\n')
file.close()
mete.close()

try:
    fd = open(u'file/genderFile.sql','r',encoding='utf-8')
    print('\n已写内容如下：\n',fd.read())
finally:
    fd.close()