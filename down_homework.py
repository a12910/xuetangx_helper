# coding=UTF-8
import requests
# from bs4 import BeautifulSoup
import urllib
import json
import os
# import urllib2

import chardet

# id来源：
# 例子：打开任意学生作业界面：https://nkdx.xuetangx.com/managecourse#/manage/5347/homework/homeworkSeekScore/17405/349419
# 则：课程id为5347，作业id为17405
# 打开学生列表 得到班级id 赵宏李妍班为6419
# cookie获取：https://jingyan.baidu.com/article/afd8f4deaf490634e286e936.html
# 例子：Cookie = 'plat_id=328; org_id=84; mode=1; iskefu=1;
#               UM_distinctid=1673f30ad94210-07e7b303d236158-4a526f-13c680-1673f30ad9529;
#               CNZZDATA1273255756=914928742-1542950313-%7C1542961113;
#               xt=gAAAAABb95wUv8z9XDOUmts9alzCaqb6tAAcHMyNCZNgqAvSMdnXxsQycIKgaO3VMHqcY-nW5SBPK_
#               IegSKm_a0vhgAgGsJhVNZfD1eGvXwsZ0JMe7JoLvY; xt_expires_in=604800; identity=3;
#               access_token=gAAAAABb99tN9bZmMAyf_3Uti0tDGtr3nOahl8E0mhZURxaB_SBetrnVAj8l4Cc8IM87T8RlS3Y4wqP8YMXrEtZ3a6Vdg-C7PQD_0jm9of8mtAB4jGmp6bo'
# 若出错请更换cookie
# Cookie = input('输入cookie')
Cookie = 'CNZZDATA1273255756=914928742-1542950313-%7C1559755060; gr_user_id=98152e33-2779-4a55-be03-dfd304a0be17; UM_distinctid=16b034cb84d259-01d7bb50645667-4a5469-13c680-16b034cb84e446; plat_id=328; org_id=84; mode=1; access_token=gAAAAABc-ARZXXFCstHFj-I3I8IDoTe18MOG2ff9I2o1gk10sufN28ex4yM7BMof4_h9X2Jszd_0AqnVKjaIyy07JSCmDLIHEa8qpl9wflnH48x9hnDm0sw; xt=gAAAAABc-ARZGL59fy5ff3MxuSSxxO9uhg9LvonpPXdRv1zDIQIk1GnIlNK1VDLQEUz2zlPGbVClDkaAT5lNO7bM_juLxB8vZm3S-mn2xiSPA9-asashqzs; xt_expires_in=604800; identity=3; mjx.latest=2.7.5'
main_id = '8340'
# classroom = input('输入班级id')
classroom = '12083'
# class_id = input('输入作业id')
class_id = '46534'

limit = '100'
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Referer': 'https://nkdx.xuetangx.com/managecourse',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cookie': Cookie,
    'x-referer': 'https://nkdx.xuetangx.com/admin/user_homework/?product_id=' + main_id + '&class_id=' + classroom + '&limit=100&offset=0&homework_id=' + class_id,
    'X-Requested-With': 'XMLHttpRequest',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'nkdx.xuetangx.com'
}
url = 'https://nkdx.xuetangx.com/admin/user_homework/?product_id=' + main_id + '&class_id=' + classroom + '&limit=' + limit + '&offset=0&homework_id=' + str(
    class_id)

path11 = '/Users/a12910/Desktop/downloads'


def get_homeworks(name2, id2):
    # name = str(name)
    id2 = str(id2)

    if not os.path.exists(path11 + '/' + name2):
        os.mkdir(path11 + '/' + name2)

    header2 = header
    header['x-referer'] = 'https://nkdx.xuetangx.com/managecourse#/manage/' + main_id + '/homework/homeworkSeekScore/' + str(
        class_id) + '/' + id2
    url2 = 'https://nkdx.xuetangx.com/admin/homework/score_correct/' + str(id2) + '/'
    str2 = requests.get(url2, headers=header2).text
    str2 = json.loads(str2)
    print (str2)
    if len(str2[u'data']) == 0:
        return

    print(str2[u'data'])
    for no in str2[u'data']:
        if no[u'type'] == 5:
            for i in no[u'attachments']:
                path1 = 'https://xuetangcloud-test.oss-cn-beijing.aliyuncs.com/' + i[u'upload_name']
                path2 = path11 + '/' + name2 + '/' + i[u'file_name']
                urllib.urlretrieve(path1, path2, down_ok)
                print (path2)


def down_ok(a, b, c):
    if c == 0:
        return
    per = 100.0 * a * b / c
    if per > 100:
        per = 100

    print ('已下载' + str(per))

print ('start')
send_data = {"product_id":main_id,"class_id":classroom,"limit":100,"offset":0,"user_name":"","user_info":"","create_start_time":"","create_end_time":"","correct_start_time":"","correct_end_time":"","current_submit":"","status":"","homework_id":class_id}
send_data2 = urllib.urlencode(send_data)
header3 = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0',
#     'Referer': 'https://nkdx.xuetangx.com/managecourse',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept':'application/json, text/plain, */*',
#     'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#     'Cookie': Cookie,
#     'x-referer': 'https://nkdx.xuetangx.com/managecourse#/manage/'+ main_id + '/homework/homeworkScorelist/' + class_id,
# # 'https://nkdx.xuetangx.com/admin/user_homework/?product_id=' + main_id + '&class_id=' + classroom + '&limit=100&offset=0&homework_id=' + class_id,
# # 'X-Requested-With': 'XMLHttpRequest',
#     'Cache-Control': 'no-cache',
#     'Connection': 'keep-alive',
#     'Content-Length':233,
#     'Content-Type':'application/json;charset=utf-8',
#     'Host': 'nkdx.xuetangx.com',
#     'If-Modified-Since':0,
#     'Pragma':'no-cache',
#

'Host': 'nkdx.xuetangx.com',
'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0',
'Accept': 'application/json, text/plain, */*',
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding': 'gzip, deflate, br',
'Referer': 'https://nkdx.xuetangx.com/managecourse',
'Content-Type': 'application/json;charset=utf-8',
'x-referer': 'https://nkdx.xuetangx.com/managecourse#/manage/5347/homework/homeworkScorelist/19351',
'Cache-Control': 'no-cache',
'If-Modified-Since': 0,
'Content-Length': 233,
'Connection': 'keep-alive',
'Cookie': 'Cookie',
'Pragma': 'no-cache'


}
# url3 = 'https://nkdx.xuetangx.com/admin/user_homework/'
# # string = requests.get(url, headers=header).text
# req = urllib2.Request(url=url3, data=send_data2, headers=header3)
# res = urllib2.urlopen(req)
# string = res.read()
f = open('test.txt')
string = f.read()

string = json.loads(string)
print (string)

if not os.path.exists(path11):
    os.mkdir(path11)

for item in string[u'data'][u'results']:
    id = item[u'id']
    name = item[u'user_name']
    name = name
    get_homeworks(name, id)
    # print id

print ("finished")

