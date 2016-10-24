# coding:utf-8
import preprocess
import os
import codecs

dictionary1 = {}
dictionary2 = {}
dictionary3 = {}
dictionary4 = {}
preprocess.readtxt(dictionary1, dictionary2, dictionary3, dictionary4)
sourcedir = 'D:\\NJU\\数据挖掘\\作业\\大作业\\data\\test'
filewrite = open('D:\\NJU\\数据挖掘\\作业\\大作业\\data\\131180026.txt', 'w')
filename = os.listdir(sourcedir)
for i in range(1, len(filename) + 1):
    datafile = codecs.open(sourcedir + '\\' + str(i) + '.txt', 'r', 'big5', 'ignore')
    recording = 0
    tmp2 = []
    # score0 = 2333 / 9970
    # score1 = 7637 / 9970
    score0 = 10000000
    score1 = 1
    finish = 0
    for line in datafile:
        if line[0:4] == 'From':
            tmp = line.split()
            if tmp[len(tmp) - 1] in dictionary3:
                filewrite.write(str(i) + '.txt' + '\t+1\n')
                finish = 1
                break
            elif tmp[len(tmp) - 1] in dictionary4:
                filewrite.write(str(i) + '.txt' + '\t-1\n')
                finish = 1
                break
        if line[0:7] == 'Subject' or recording == 1:
            if recording == 1:
                tmp = line.split()
            elif line[0:7] == 'Subject':
                tmp = line[9:len(line)].split()
            for j in tmp:
                tmp2.append(j.strip(',.!?;:"[]{}/|<>').lower())
                if tmp2[len(tmp2) - 1] in preprocess.todelete:
                    tmp2.pop()
        if line[0:25] == 'Content-Transfer-Encoding':
            recording = 1
    if finish == 1:
        continue
    for j in range(len(tmp2) - 1, -1, -1):
        if not preprocess.is_alphabet(tmp2[j][0:1]):
            tmp2.pop(j)
    tmp2 = list(set(tmp2))
    for j in tmp2:
        if j in dictionary1 and j in dictionary2:
            score0 *= dictionary1[j]
            score1 *= dictionary2[j]
    if score0 > score1:
        result = '+1'
    else:
        result = '-1'
    filewrite.write(str(i) + '.txt' + '\t' + result + '\n')
filewrite.close()
