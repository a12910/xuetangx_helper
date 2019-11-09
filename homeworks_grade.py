import homeworks_db as db
import homeworks_head as head
import homeworks_download as hdown

import json, xlwt, xlrd, copy

def send_grade(homework_id, data):
    url, header = head.get_header({
        'Referer': 'managecourse',
        'x-referer': 'managercourse#/manage/' + db.user_info['course_id'] + '/homework/homeworkNewScore/' + db.user_info['lesson_id'] + '/' + homework_id,
        'url': 'admin/homework/score_correct/' + homework_id + '/'
    }, {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json;charset = utf-8',
        'If-Modified-Since':'0'
    })
    params = {
        'type':'2',
        'data': data
    }
    params = json.dumps(params)
    result = head.send_data_post(url, params, header)
    result_text = json.loads(result.text)
    # print(result_text)
    return result_text['code']

def load_template():
    print('<上传成绩模板>')
    work_path = hdown.mkdir(db.user_info['work_path'] + 'grade')
    wbook = xlrd.open_workbook(work_path + '/grade_template.xls')
    sheet1 = wbook.sheet_by_index(0)
    rows = sheet1.nrows
    ques_count = (sheet1.ncols-3)//3
    for row in range(1,rows):
        data = []
        for ques in range(ques_count):
            grades = {
                'id':str(int(sheet1.cell(row, ques*3+3).value//1)),
                'grade':str(int(sheet1.cell(row, ques*3+4).value)),
                'comment':sheet1.cell(row, ques*3+5).value
            }
            if grades['comment'] == '':
                grades['comment'] = grades['id']
            data.append(copy.deepcopy(grades))
        homework_id = sheet1.cell(row, 2).value
        name = sheet1.cell(row, 0).value
        # print(homework_id, data)

        result = send_grade(homework_id, data)
        if result == 0:
            print(row, name, [x['grade'] for x in data], '已上传')
    print('上传完成!')

def save_template():
    print('<导出成绩填写模板>')
    if len(db.homeworks) == 0:
        db.load_homework()
    temp = db.homeworks[0]
    temp2 = head.get_homework(temp['id'])
    question_num = len(temp2)
    question_marks = [item['mark'] for item in temp2]

    work_path = hdown.mkdir(db.user_info['work_path'] + 'grade')
    wbook = xlwt.Workbook()
    wsheet1 = wbook.add_sheet('grade')
    line1 = ['姓名','学号','作业编号']
    for i in range(question_num):
        line1 += ['题目'+ str(i+1) + '编号', '成绩(满分' + str(question_marks[i]) + ')', '评论']
    write_line(line1, 0, wsheet1)

    index = 0
    for item in db.homeworks:
        index += 1
        print(index, item['user_name'],'获取信息ing')
        result = head.get_homework(item['id'])
        line2 = [item['user_name'], item['user_number'], item['id']]
        for ques in result:
            line2 += [ques['id'],'','']
        write_line(line2, index, wsheet1)

    wbook.save(work_path + '/grade_template.xls')
    print('导出完成\n','保存至：工作路径/grade_template.xls')

def write_line(data, line, wsheet):
    for i in range(len(data)):
        wsheet.write(line, i, data[i])




if __name__ == '__main__':
    pass