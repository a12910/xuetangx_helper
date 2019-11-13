import numpy as np
import pdb
import homeworks_head as heads
import homeworks_login as login

user_info = {
    "Cookie" : "",
    "course_id":'',
    "course_name":'',
    "term_id":'519',
    'class_id':'',
    "class_name":'',
    'lesson_id':'',
    "lesson_name":'',
    'homework_id':'',
    'user':'',
    'passwd':'',
    'work_path':''
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

def save_conf(show=True):
    if True:
        print('<保存配置文件>')
    out_file = open("conf.txt", "w")
    for key in user_info.keys():
        out_file.write(key+',,,')
        out_file.write(str(user_info[key]) + '\n')
    out_file.close()

def init_conf(mode):
    global user_info

    if mode == 'init':
        if user_info['user'] == '':
            print('<请输入用户信息>')
            user_info['user'] = input('用户名 ')
            user_info['passwd'] = input('密码 ')
            user_info['work_path'] = input('工作路径')
            login_result = login.login()
            save_conf()
            if not login_result:
                init_conf(mode)
            else:
                heads.get_courses() # 课程列表
                heads.get_classes() # 班级列表
                heads.get_lessons() # 题目列表
                save_conf()
        else:
            load_conf()
    elif mode == 'change':
        print('<请输入用户信息>')
        user_info['user'] = input2('用户名 ', user_info['user'])
        user_info['passwd'] = input2('密码 ', user_info['passwd'])
        user_info['work_path'] = input2('工作路径 ', user_info['work_path'])
        heads.get_courses()  # 课程列表
        heads.get_classes()  # 班级列表
        heads.get_lessons()  # 题目列表
        save_conf()

def input2(string, default):
    temp = input(string)
    if temp == '':
        return default
    else:
        return temp


