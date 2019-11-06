import os
import rarfile
import zipfile
import shutil
import re

inpath = './download'
outpath = './download2/'
homeworks = ['1', '2']


def WorkJudge(path, file):
    print(file, 'Det')
    Jlist = [{'name': '1', 'judge': 'merge'}, {'name': '1', 'judge': '第一'}, {'name': '1', 'judge': '作业一'},
             {'name': '2', 'judge': '作业二'}, {'name': '2', 'judge': '第二'}, {'name': '1', 'judge': 'LinearList'},
             {'name': '1', 'judge': 'LinkList'}]
    Jlist2 = [{'name': '1', 'judge': '1'}, {'name': '1', 'judge': '一'}, {'name': '2', 'judge': '2'},
              {'name': '2', 'judge': '二'}, {'name': '', 'judge': 'Debug'}, {'name': '', 'judge': 'sln'},{'name': '', 'judge': '3'}]
    for i in Jlist:
        i['judge'] = i['judge'].upper()
        if file.upper().find(i['judge']) != -1:
            return i['name']
    for i in Jlist2:
        i['judge'] = i['judge'].upper()
        if file.upper().find(i['judge']) != -1:
            return i['name']

    if os.path.isdir(path + '/' + file):
        print('not found')
        return ''

    f = open(path + '/' + file)
    try:
        for line in f:
            for i in Jlist:
                if line.upper().find(i['judge']) != -1:
                    f.close()
                    return i['name']
    except BaseException:
        f.close()
        print('not found')
        return ''

    f.close()
    print('not found')
    return ''


def FileToFolder(fpath, file, type, stu):
    for i in homeworks:
        if type.find(i) != -1:
            if os.path.isfile(fpath + '/' + file):
                shutil.copy(fpath + '/' + file, outpath + stu + '/' + i + '/' + file)
            else:
                wdir = fpath + '/' + file
                lists = os.listdir(wdir)

                if os.path.isdir(wdir + '/' + file):
                    wdir = wdir + '/' + lists[0]
                    lists = os.listdir(wdir)
                for t in lists:
                    if t == file:
                        lists2 = os.listdir(wdir)
                        for k in lists2:
                            last3 = k[-3:]
                            if last3 == 'cpp' or k[-2:] == '.h' or last3 == 'hpp':
                                shutil.copy(wdir + '/' + file + '/' + k, outpath + stu + '/' + i + '/' + k)
                    else:
                        last3 = t[-3:]
                        if last3 == 'cpp' or t[-2:] == '.h' or last3 == 'hpp':
                            shutil.copy(wdir + '/' + t, outpath + stu + '/' + i + '/' + t)

    if os.path.isfile(fpath + '/' + file):
        os.remove(fpath + '/' + file)
        return
    else:
        # os.removedirs(fpath + '/' + file)
        return


def unzip(file, fpath, opath, new=False):
    last3 = file[-3:]
    if new:
        new2 = file[:-4]
    if not os.path.isfile(fpath + '/' + file):
        return 'folder'
    try:
        if last3 == 'zip':
            f = zipfile.ZipFile(fpath + '/' + file, 'r')

            # for file in f.namelist():
            #     filename = file.encode('cp437').decode('gbk')  # 先使用cp437编码，然后再使用gbk解码
            #     # print(filename)
            #     f.extract(file, opath)  # 解压缩ZIP文件
            #     # os.chdir(release_file_dir)  # 切换到目标目录
            #     os.rename(opath + '/' + file, filename)  # 重命名文件
            if new:
                opath = opath + '/' + file[:-4]
                if not os.path.exists(opath):
                    os.mkdir(opath)

            f.extractall(opath)
            os.remove(fpath + '/' + file)
            ftype = 'folder'
        elif last3 == 'rar':
            rf = rarfile.RarFile(fpath + '/' + file)

            if new:
                opath = opath + '/' + file[:-4]
                if not os.path.exists(opath):
                    os.mkdir(opath)

            rf.extractall(opath)
            os.remove(fpath + '/' + file)
            ftype = 'folder'

        elif last3 == 'cpp' or item[-2:] == '.h' or last3 == 'hpp':
            ftype = 'doc'

        else:
            ftype = 'other'
            print(fpath, item)
    except BaseException:
        print(file, fpath)
        ftype = ''
        pass

    return ftype


all_lists = os.listdir(inpath)

for i in range(len(all_lists)):
    stu = all_lists[i]
    print(stu)

    if not os.path.exists(outpath + '/' + stu) and stu[0:1] != '.':
        os.mkdir(outpath + '/' + stu)
    else:
        continue
    for i in homeworks:
        if not os.path.exists(outpath + '/' + stu + '/' + i):
            os.mkdir(outpath + '/' + stu + '/' + i)

    # FolderType(path1)
    # ftype = []
    inpath2 = inpath + '/' + stu

    lists = os.listdir(inpath2)
    if len(lists) == 1:
        unzip(lists[0], inpath2, inpath2)
        # os.remove(inpath2 + '/' + lists[0])
        lists0 = lists[0]
        lists = os.listdir(inpath2)
        if len(lists) == 1 and not os.path.isfile(inpath2 + '/' + lists[0]):
            lists2 = os.listdir(inpath2 + '/' + lists[0])
            for i in lists2:
                shutil.move(inpath2 + '/' + lists[0] + '/' + i, inpath2 + '/' + i)
            os.rmdir(inpath2 + '/' + lists[0])

    else:
        for item in lists:
            x = unzip(item, inpath2, inpath2, True)
            if x == 'doc':
                print(item, homeworks, 'type?')
                print(lists)

                x2 = WorkJudge(inpath2, item)
                if x2 == '':
                    x2 = input()
                else:
                    print(x2)
                FileToFolder(inpath2, item, str(x2), stu)

    lists = os.listdir(inpath2)
    for item in lists:
        if not os.path.isdir(inpath2 + '/' + item):
            continue
        print(lists)
        print(item, homeworks, "type?")
        x2 = WorkJudge(inpath2, item)
        if x2 == '':
            x2 = input()
        else:
            print(x2)

        FileToFolder(inpath2, item, str(x2), stu)

print('finish')
