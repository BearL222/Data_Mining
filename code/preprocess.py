# coding:utf-8
import codecs
import os

todelete = {'a', 'an', 'the', 'is', 'are', 'to', 'for', 'of', 'in', 'at', 'on', 'after', 'from', 'since', 'behind',
            'beside', 'under', 'below', 'over', 'above', 'by', 'among', 'about', 'with', 'except', 'besides', 'up',
            'near', 'this', 'not', 'and', 'or', 'that', 'if', 'be'}


def is_alphabet(uchar):
    if u'\u0041' <= uchar <= u'\u005a' or u'\u0061' <= uchar <= u'\u007a':
        return True
    else:
        return False


def word_process(word):
    if word[len(word) - 2:len(word)] == 'ed':
        return word[0:len(word) - 1]
    tmp = 0
    for i in range(len(word)):
        if not is_alphabet(word[i]):
            tmp = i
            break
    if tmp != 0:
        return word[0:tmp]
    return word


def makedict(datafile, dictionary, dictionary_content):
    recording = 0
    tmp2 = []
    for line in datafile:
        if line[0:4] == 'From':
            tmp = line.split()
            if tmp[len(tmp) - 1] in dictionary_content:
                dictionary_content[tmp[len(tmp) - 1]] += 1
            else:
                dictionary_content[tmp[len(tmp) - 1]] = 1
        if line[0:7] == 'Subject' or recording == 1:
            if recording == 1:
                tmp = line.split()
            elif line[0:7] == 'Subject':
                tmp = line[9:len(line)].split()
            for i in tmp:
                tmp2.append(i.strip('`~@#$%^&*()-_+=\,.!?;:"[]{}/|<>').lower())
                if tmp2[len(tmp2) - 1] in todelete:
                    tmp2.pop()
        if line[0:25] == 'Content-Transfer-Encoding':
            recording = 1
    for i in tmp2:
        if not is_alphabet(i[0:1]) or len(i) > 13:
            continue
        i = word_process(i)
        if i in dictionary:
            dictionary[i] += 1
        else:
            dictionary[i] = 1


def readtxt(dictionary1, dictionary2, dictionary3, dictionary4):
    sourcedir = 'D:\\NJU\\数据挖掘\\作业\\大作业\\data\\train\\spam'
    dictionary = [dictionary1, dictionary2]
    dictionary_content = [dictionary3, dictionary4]
    for i in range(2):
        if i == 1:
            sourcedir = sourcedir[0:len(sourcedir) - 4] + 'ham'
        filename = os.listdir(sourcedir)
        for name in filename:
            datafile = codecs.open(sourcedir + '\\' + name, 'r', 'big5', 'ignore')
            makedict(datafile, dictionary[i], dictionary_content[i])
            datafile.close()
        for key in dictionary[i].keys():
            dictionary[i][key] = (dictionary[i][key] + 1) / (len(filename) + 2)
