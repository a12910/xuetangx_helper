import numpy as np
import pdb

user_info = {
    "Cookie" : "",
    "course_id":'17045',
    "term_id":'519',
    'class_id':'28909',
    'lesson_id':'114870',
    'user':'',
    'passwd':'h129100',
    'work_path':'/Users/hrd/Desktop/xuetangx_work/'
}


homeworks = []

def save_homework(data):
    '''保存作业列表'''
    out_file = open("homeworks.txt", "w")
    # print(data)
    # pdb.set_trace()
    for item in data:
        # print(item)
        out_file.write(str(item['id']) + ',,,')
        out_file.write(item['user_name'] + ',,,')
        out_file.write(item['user_number'] + '\n')
    out_file.close()

    global homeworks
    homeworks = data

def load_homework():
    ''' 载入作业 '''
    data = []
    for line in open("homeworks.txt", "r"):
        data.append(line)

    data2 = []
    for item in data:
        item2 = item.split(',,,')
        data2.append({
            'id':item2[0],
            'user_name':item2[1],
            'user_number':item2[2].replace('\n', '')
        })

    global homeworks
    homeworks = data2
    return data

def load_conf():
    ''' 载入配置 '''
    print('<载入配置文件>')
    data = []
    for line in open("conf.txt", "r"):
        data.append(line)

    conf = {}
    for item in data:
        item = item.split(',,,')
        conf[item[0]] = item[1].replace('\n', '')

    global user_info
    user_info.update(conf)
    return user_info

def save_conf():
    print('<保存配置文件>')
    out_file = open("conf.txt", "w")
    for key in user_info.keys():
        out_file.write(key+',,,')
        out_file.write(str(user_info[key]) + '\n')
    out_file.close()

def init_conf():

    pass


