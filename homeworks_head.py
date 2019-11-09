import requests
import homeworks as mains
import homeworks_db as db
import json
import pdb


def get_courses():
    # 选择课程
    user_info = db.user_info
    url, header = get_header({
        'Referer':'manager',
        'x-referer':'manager#/teachercourselist',
        'url':'course_manage_list'
    },{
        'Cache-Control':'no-cache',
        'Accept': 'application/json, text/plain, */*',
        'If-Modified-Since': '0'
    })
    params = {
        'term_id':user_info['term_id'],
        'page_size':10,
        'running_status':'',
        'search':'',
        'page':'1',
        'course_type':''

    }
    result = send_data(url, params, header)
    lists = json.loads(result.text)['data']['results']
    if len(lists) == 0:
        print('err')

    result_choice = choose_list('course_name', 'course_id', lists, '班级序号')
    db.user_info['course_id'] = result_choice
    return result_choice

def get_lessons():
    url, header = get_header({
        'Referer': 'managecourse',
        'x-referer': 'managercourse#/manage/' + db.user_info['course_id'] + '/homework/homeworkScoreManage',
        'url': 'inner_api/score_homework/'
    }, {
        'Cache-Control': 'no-cache',

    })
    params = {
        'product_id': db.user_info['course_id'],
        'class_id':db.user_info['class_id'],
        'limit':'100',
        'offset':'0'
    }
    result = send_data(url, params, header)
    lists = json.loads(result.text)['data']['results']

    result_choice = choose_list('name', 'in_id', lists, '作业序号')
    db.user_info['homework_id'] = result_choice

    return result_choice
    pass

def get_classes():
    url, header = get_header({
        'Referer': 'managecourse',
        'x-referer': 'managercourse#/manage/' + db.user_info['course_id'] + '/homework/homeworkScoreManage',
        'url': 'server/api/workbench_courseinfo'
    }, {
        'Cache-Control': 'no-cache',

    })
    params = {
        'course_id': db.user_info['course_id'],
    }
    result = send_data(url, params, header)
    lists = json.loads(result.text)['data']

    result_choice = choose_list('name', 'id', lists, '班级序号')
    db.user_info['class_id'] = result_choice

    return result_choice
    pass


def get_homework(homework_id):
    url, header = get_header({
        'Referer': 'managecourse',
        'x-referer': 'managercourse#/manage/' + db.user_info['course_id'] + '/homework/homeworkScorelist/' +
                     db.user_info['lesson_id'] + '/' + homework_id,
        'url': 'admin/homework/score_correct/' + homework_id + '/'
    }, {
        'Cache-Control': 'no-cache',
    })
    params = {}
    result = send_data(url, params, header)
    result = json.loads(result.text)['data']
    return result


def get_homeworks():

    url, header = get_header({
        'Referer': 'managecourse',
        'x-referer': 'managercourse#/manage/' + db.user_info['course_id'] + '/homework/homeworkScorelist/' + db.user_info['lesson_id'],
        'url': 'admin/user_homework/'
    }, {
        'Cache-Control': 'no-cache',

    })
    params = {
        'product_id': db.user_info['course_id'],
        'class_id':db.user_info['class_id'],
        'homework_id':db.user_info['homework_id'],
        'limit':'20',
        'offset':'0'
    }
    result = send_data(url, params, header)
    result_text = json.loads(result.text)
    main_count = int(result_text['data']['count'])
    lists = []
    lists += result_text['data']['results']
    for offset in range(1, main_count // 20 + 1):
        params['offset'] = offset * 20
        result_temp = send_data(url, params, header).text
        result_temp = json.loads(result_temp)['data']['results']
        # print(result_temp)
        # pdb.set_trace()
        lists += result_temp
    db.save_homework(lists)
    # print(db.homeworks)
    return db.homeworks
    pass


def choose_list(key_note, key_out, lists, note):
    if len(lists) == 0:
        print('err')
    print('请输入', note, ' 0: ', lists[0][key_out])
    count = 0
    for item in lists:
        # print(count, ': ', item[key_note], ':', item[key_out])
        print(count, ': ', item[key_note])
        count += 1
    result = input('请选择 ')
    if result == '':
        result = 0
    else:
        result = int(result)
    return lists[result][key_out]




def init_login():
    url, header = get_header({
        'Referer': '',
        'x-referer': '',
        'url': 'managecourse'
    }, {
        'Referer':'',
        'x-referer':'',
        'Upgrade-Insecure-Requests':'1'
    })
    params = {
        'course_id': db.user_info['course_id'],
    }
    result = send_data(url, params, header).headers
    result = json.loads(result)

    # print(result)


def get_header(data, data_add = {}):
    user_info = db.user_info
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Referer': 'https://nkdx.xuetangx.com/' + data['Referer'],
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': user_info['Cookie'],
        'x-referer': 'https://nkdx.xuetangx.com/' + data['x-referer'],
        'X-Requested-With': 'XMLHttpRequest',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'nkdx.xuetangx.com',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Upgrade-Insecure-Requests':'1'
    }
    url = 'https://nkdx.xuetangx.com/' + data['url']
    header.update(data_add)
    return url, header

def send_data(url, params, header):
    return requests.get(url, params=params, headers=header)


if __name__ == '__main__':
    pass
# https://nkdx.xuetangx.com/server/api/file_from_oss?file=https://xuetangcloud-test.oss-cn-beijing.aliyuncs.com/exams/attachments-online-2019116113739522318078.jpg&filename=111.jpg