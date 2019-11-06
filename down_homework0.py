# coding=UTF-8
import requests
from bs4 import BeautifulSoup
import urllib
import json
import os
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
Cookie = 'UM_distinctid=1673f30ad94210-07e7b303d236158-4a526f-13c680-1673f30ad9529; xt=gAAAAABb-UC29YBjNBF6o7QZAhxD6qtIZ357lttVtQ21oR7zOcoKNV48FGiWkdeODeiQBTPp5srw0H3FZpPrkoxIdOtt-EDRcmwJPhAJHtZNfOpqhtxgBWc; xt_expires_in=604800; identity=3; access_token=gAAAAABb-UC2N7FxMB8vYmj3-ba2SO6UgxtLoRP0cNbFttauFA8QXqull3qyEC4zVc-3sdjYLkv_lHDsdZnpvg4zmpX93ql8Y4u3_XYaYAFIMYxlKSD8Tas'
# main_id = input('输入课程id')
main_id = '5347'
# classroom = input('输入班级id')
classroom = '6419'
# class_id = input('输入作业id')
class_id = '19351'

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


def get_homeworks(name2, id2):
    # name = str(name)
    id2 = str(id2)

    if not os.path.exists('./download/' + name2):
        os.mkdir("./download/" + name2)

    header2 = header
    header[
        'x-referer'] = 'https://nkdx.xuetangx.com/managecourse#/manage/' + main_id + '/homework/homeworkSeekScore/' + str(
        class_id) + '/' + id2
    url2 = 'https://nkdx.xuetangx.com/admin/homework/score_correct/' + str(id2) + '/'
    str2 = requests.get(url2, headers=header2).text
    str2 = json.loads(str2)
    for i in str2[u'data'][0][u'attachments']:
        path1 = 'https://xuetangcloud-test.oss-cn-beijing.aliyuncs.com/' + i[u'upload_name']
        path2 = './download/' + name2 + '/' + i[u'file_name']
        urllib.urlretrieve(path1, path2, down_ok)
        print (path2)


def down_ok(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print ('已下载' + str(per))

string = requests.get(url, headers=header).text
string = json.loads(string)

print (string)
if not os.path.exists('./download'):
    os.mkdir("./download")

for item in string[u'data'][u'results']:
    id = item[u'id']
    name = item[u'user_name']
    name = name + " " + str(id)
    get_homeworks(name, id)
    # print id

print ("finished")

