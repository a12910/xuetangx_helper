import rarfile
import os
fpath = './download/3152632 高诗嘉'
file = '实习一（1）.rar'
opath = './download2'
rf = rarfile.RarFile(fpath +'/' + file)
rf.extractall(opath)
