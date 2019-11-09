import urllib
import json
import os
import requests
import homeworks_head as heads
import homeworks_db as db
import homeworks_download as hdown


def init_conf():
    pass

def main():
    db.load_conf()
    # init_conf()
    # get_cookie()
    # heads.init_login()
    # heads.get_courses() # 课程列表
    # heads.get_classes() # 班级列表
    # heads.get_lessons() # 题目列表
    # heads.get_homeworks() # 作业列表
    db.load_homework()
    hdown.down_main()
    # heads.get_homework('7245062')
    # db.save_conf()

    pass

if __name__ == '__main__':
    main()