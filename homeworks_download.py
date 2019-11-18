import homeworks_db as db
import homeworks_head as head
from contextlib import closing
import sys, math, requests, os

def down_main():
    work_path = mkdir(db.user_info['work_path'] + 'download')
    work_path = mkdir(work_path + '/' + db.user_info['lesson_name'])
    index = -1
    for item in db.homeworks:
        index += 1
        work_path2 = mkdir(work_path + '/' + item['user_number'] + ' ' + item['user_name'])

        homework_id = str(item['id'])

        results = head.get_homework(homework_id)
        for result in results:
            if len(results) == 1:
                work_path3 = work_path2
            else:
                work_path3 = mkdir(work_path2 + '/' + str(index))

            attachments = result['attachments']
            outfile = open(work_path3 + '/answer.txt', 'w')
            text = result['answer']
            for ans in text:
                outfile.write(ans + '\n')
            outfile.close()

            down_path = 'https://xuetangcloud-test.oss-cn-beijing.aliyuncs.com/'
            print(index, item['user_name'], item['user_number'], '下载附件')
            for atta in attachments:
                down_path2 = down_path + atta['upload_name']
                out_path = work_path3 + '/' + atta['file_name']
                download_file(down_path2, out_path, atta['file_name'] + ' ')

    print('<下载完成>')

def download_file(file_url, file_path, string):
    print(string)
    with closing(requests.get(file_url, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 内容体总大小
        data_count = 0
        with open(file_path, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count = int(data_count + len(data))
                processBar(data_count, content_size)
                # now_jd = (data_count / content_size) * 100

                # print("\r 文件下载进度：%d%%(%d/%d) - %s" % (now_jd, data_count, content_size, file_path), end=" ")

def processBar(num, total):  # 进度条
    rate = num / total
    rate_num = int(rate * 100)
    if rate_num == 100:
        r = '\r%s>%d%%\n' % ('=' * int(rate_num / 6), rate_num,) # 控制等号输出数量，除以3,表示显示1/3
    else:
        r = '\r%s>%d%%' % ('=' * int(rate_num / 6), rate_num,)
    sys.stdout.write(r)
    sys.stdout.flush

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return path

if __name__ == '__main__':
    pass