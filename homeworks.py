import homeworks_head as heads
import homeworks_db as db
import homeworks_download as hdown
import homeworks_grade as hgrade


def main():
    # db.load_conf()
    db.init_conf()
    # get_cookie()
    # heads.init_login()
    # heads.get_courses() # 课程列表
    # heads.get_classes() # 班级列表
    # heads.get_lessons() # 题目列表
    # heads.get_homeworks() # 作业列表
    # db.load_homework()
    hgrade.load_template()
    # hgrade.save_template()
    # hdown.down_main()
    # heads.get_homework('7245062')
    # db.save_conf()

    pass

if __name__ == '__main__':
    main()