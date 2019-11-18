import homeworks_head as heads
import homeworks_db as db
import homeworks_download as hdown
import homeworks_grade as hgrade
import homeworks_login as login

def prints(data):
    for i in data:
        print(i)

def main():
    print('<欢迎使用学堂云小助手>')
    db.init_conf('init')
    print('<当前信息>')
    print('课程 %s' % (db.user_info['course_name']))
    print('班级 %s' % (db.user_info['class_name']))
    print('题目 %s' % (db.user_info['lesson_name']))
    print('')
    prints(['<选择操作>', '1: 修改信息', '2: 批量下载作业', '3: 导出成绩模板', '4: 批量上传成绩模板', '5: 退出'])
    temp = int(input('选择 '))
    if temp == 1:
        db.init_conf('change')
    elif temp == 2:
        heads.get_homeworks()
        hdown.down_main()
    elif temp == 3:
        hgrade.load_template()
    elif temp == 4:
        hgrade.save_template()
    elif temp == 5:
        print('Bye~')
    else:
        print('Bye~')


def main2():
    db.load_conf()
    # db.init_conf('init')
    # get_cookie()
    login.login()
    # heads.init_login()
    heads.get_courses() # 课程列表
    # heads.get_classes() # 班级列表
    # heads.get_lessons() # 题目列表
    # heads.get_homeworks() # 作业列表
    # db.load_homework()
    # hgrade.load_template()
    # hgrade.save_template()
    # hdown.down_main()
    # heads.get_homework('7245062')
    # login.parse_index()

    db.save_conf()
    pass

if __name__ == '__main__':
    main()
