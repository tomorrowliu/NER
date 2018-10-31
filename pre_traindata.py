# encoding='UTF-8'
from collections import OrderedDict
import os
import os.path
import re
import numpy as np
from config import read_config

def do_convert(text, labeled):
    i = 0
    result = list()
    while i < len(text):
        entity = 'O'
        if (labeled and int(labeled[0][2]) == i):
            for j in range(int(labeled[0][3]) - int(labeled[0][2])):
                if j == 0:
                    entity = 'B-' + str(labeled[0][1])
                else:
                    entity = 'I-' + str(labeled[0][1])
                line = text[i] + ' ' + entity
                result.append(line)
                i += 1
            else:
                del labeled[0]
        elif text[i] == '\n' or text[i] == ' ':
            line = ' '
            i +=1
            result.append(line)
        else:
            line = text[i] + ' ' + entity
            i += 1
            result.append(line)
    return result

def pre_train():
    files = list(read_config.train_brat_files)
    for file in files:
        data_labeled = open(read_config.train_brat_path + file[0], 'r',encoding='UTF-8')
        data_orig = open(read_config.train_brat_path + file[1], 'r',encoding='UTF-8')
        result = list()
        text = data_orig.read().strip('\n').strip('\r')
        for line in data_labeled.readlines():
            line = line.strip()
            if ";" in line:
                line = line.replace(';',' ')
            if not len(line) or line.startswith('#'):
                continue
            line = re.split(r'[\s]', line)
            result.append(line)

        result.sort(key=lambda x:int(x[2]))
        train_ref_data = do_convert(text, result)
        data_labeled.close()
        data_orig.close()
        with open(read_config.train_ref_path + file[0].split('.')[0] + '.txt' , 'w',encoding='UTF-8') as fw:
            fw.write('%s' % '\n'.join(train_ref_data))
    else:
        print("Convert complete %d files" % len(files))

def pre_test():
    path = ("G:\\tensorflow\\pre-train\\data\\pre_testdata_brat")
    path_list = os.listdir(path)
    for filename in path_list:
        data_orig = os.path.join(path , filename)
        f = open(data_orig, 'r',encoding='UTF-8')
        text = f.read().strip('\n').strip('\r')
        result = list()
        i = 0
        while i < len(text):
            line = text[i]
            i += 1
            result.append(line)
        f.close()
        name = []
        name.append(filename.replace('.txt', ''))
        os.chdir(r'G:\\tensorflow\\pre-train\\data\\testdata_crf')
        with open( str(name[0]) + '.txt', 'w',encoding='UTF-8') as fw:
            fw.write('%s' % '\n'.join(result))
    else:
        print("Convert complete %d files" % len(path_list))

def submit():
    path = 'G:\\tensorflow\\pre-train\\data\\output_data\\'
    path_list = os.listdir(path)
    for file in path_list:
        f = open(path + file, 'r',encoding='UTF-8')
        result = list()
        for line in f.readlines():
            line = line.strip()
            line = re.split(r'[\s]', line)
            result.append(line)
        i = 0
        flag = 0
        num = 1
        result2 = list()
        while (i < len(result)):
            if len(result[i]) == 3 and str(result[i][2]) == 'O':
                flag += 1
                i += 1
            elif len(result[i]) == 2 and str(result[i][1]) == 'O':
                flag += 1
                i += 1
            elif len(result[i]) == 1 and str(result[i][0]) == '':
                i += 1
            elif len(result[i]) == 3 and str(result[i][2])[0] == 'B':
                    start = flag
                    Class = str(result[i][1])[2:]
                    j = i
                    while len(result[i + 1]) == 3 and (str(result[i + 1][2]) == str('I-' + Class)):
                        i += 1
                        flag += 1
                        end = flag + 1
                    message = ''
                    for k in range(j, i + 1):
                        message = message + str(result[k][0])
                    temp = ''
                    temp = ('T' + str(num) + "    " + str(Class) + ' ' + str(start) + ' ' + str(end) + "    " + str(
                        message))
                    i += 1
                    flag += 1
                    num += 1
                    result2.append(temp)
            else:
                i += 1
                flag += 1

        f.close()
        name = []
        name.append(file.replace('.txt', ''))
        os.chdir(r'G:\\tensorflow\\pre-train\\data\\submit_data')
        with open( str(name[0]) + '.ann', 'w', encoding='UTF-8') as fw:
            fw.write('%s' % '\n'.join(result2))
    else:
        print("Convert complete %d files" % len(path_list))

def concat():
    #coding=utf-8
    import os
    #获取目标文件夹的路径
    filedir = os.getcwd()+'/data/traindata_crf'
    #获取当前文件夹中的文件名称列表
    filenames=os.listdir(filedir)
    #打开当前目录下的result.txt文件，如果没有则创建
    f=open('result.txt','w')
    #先遍历文件名
    for filename in filenames:
        filepath = filedir+'/'+filename
        #遍历单个文件，读取行数
        for line in open(filepath):
            f.writelines(line)
    #关闭文件
    f.close()

if __name__ == "__main__":
    #pre_train()
    #pre_test()
    #submit()
     concat()

    """
    # -*- coding:utf-8 -*-
    fileobj = open("name.txt", "a")
    path = "G:\\tensorflow\\pre-train\\data\\pre_testdata_brat"  # 待读取的文件夹

    path_list = os.listdir(path)
    path_list.sort()  # 对读取的路径进行排序

    for filename in path_list:
        if os.path.splitext(filename)[1] == '.txt':
            name = []
            name.append(filename.replace('.txt',''))
            for item in name:
                final_name = []
                final_name.append(item +'.ann ')
                final_name.append(item + '.txt')
                temp = " = ".join(final_name)
                fileobj.write(temp)
                fileobj.write("\n")
    fileobj.close()
    """



