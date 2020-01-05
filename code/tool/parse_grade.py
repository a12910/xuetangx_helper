# coding=UTF-8
"""
# 使用说明：
# 将姓名保存在当前目录下为name.xlsx
# 评价表格保存在当前目录/download下
# 输出为当前目录out.xls
"""

import os, xlwt, xlrd, copy, numpy

from collections import defaultdict

dic = {'name': '', 'grade': [], 'average':[0,0,0,0,0]}
namebook = xlrd.open_workbook('name.xlsx')
name_sheet0 = namebook.sheet_by_index(0)
names = name_sheet0.col_values(0)
paths = '/Users/hrd/Desktop/未命名文件夹/'

results = {}

for i in range(len(names)):
    if names[i] != '':
        results[names[i]] = numpy.array([0,0,0,0,0,  0], dtype=float)

    # dic['name'] = names[i]
    # names[i] = copy.deepcopy(dic)

for root, dirs, files in os.walk(paths):
    for file in files:
        if str(file).find('xls') == -1 :
            continue
        print(file)
        tempbook = xlrd.open_workbook(paths + file)
        sheet0 = tempbook.sheet_by_index(0)
        count = len(sheet0.col_values(0))-2
        for u in range(count):
            line = sheet0.row_values(u+2)
            # print(line)

            name = line[0]
            for o in range(1,6):
                if line[o] == '':
                    line[o] = 5
            grade = numpy.array(line[1:6] + [1], dtype=float)
            if not name in results.keys():
                print('no name', name, grade)
                results[name] = numpy.array([0,0,0,0,0,  0], dtype=float)
            results[name] += grade


out = xlwt.Workbook(encoding='UTF-8')
ws = out.add_sheet('out grade')
# for e in range(len(names)):
e = 0
for nn in results.keys():
    # nn = names[e]
    e += 1
    if nn == '':
        continue
    print (nn, results[nn])
    ws.write(e, 0, label=nn)
    ws.write(e, 1, label=results[nn][5])
    if not results[nn][5] == 0:
        results[nn] = results[nn] / results[nn][5]
    for u in range(5):
        ws.write(e, 2+u, label=results[nn][u])

out.save('out.xls')
print('finish')