# -*- coding: utf-8 -*-

import os
import re
import shutil
def isblank(filename):
    f = open(filename,'r',errors='ignore') # 读模式
    allPage=0
    errPage=0
    t=0
    for line in f.readlines():  
        line=line.replace('\x00\x00',' ').replace('\x00','')
        if re.match(r'-+Page [0-9]+-+',line)!=None:
            if t<3:
                errPage+=1
                # print(allPage)
            t=0
            allPage+=1
        else: 
            if len(line.replace(' ',''))>30 and len(line.split())>=3:
                t+=(1+len(line)//120)
    if errPage > 10 or errPage/allPage > 0.5:
        return True
    else:
        return False

def findblank(fileDir,PDFDir,tarDir,pdfNDir):
    if fileDir[-1]=='/':
        fileDir=fileDir[:-1]
    if PDFDir[-1] == '/':
        PDFDir = PDFDir[:-1]
    if tarDir[-1]=='/':
        tarDir=tarDir[:-1]
    if pdfNDir[-1]=='/':
        pdfNDir=pdfNDir[:-1]

    files = os.listdir(fileDir)
    if not os.path.exists(tarDir):
        os.mkdir(tarDir)

    if not os.path.exists(pdfNDir):
        os.mkdir(pdfNDir)

    for file in files:
        if file.split('.')[-1] in ['txt']:
            filePath = fileDir + '/' + file
            if isblank(filePath):
                # pass
                shutil.copy2(PDFDir+ '/' +  file[:-4] + '.pdf', pdfNDir + '/' + file[:-4] + '.pdf')
                shutil.move(filePath, tarDir + '/' + file[:-4] + '.txt')



if __name__ == "__main__":

    # findblank('/Users/brobear/PycharmProjects/DOPDF2TXT/(1,39)_blank_Txt','/Users/brobear/PycharmProjects/DOPDF2TXT/(1,39)',
    #           '/Users/brobear/PycharmProjects/DOPDF2TXT/(1,39)_blank_Txt','/Users/brobear/PycharmProjects/DOPDF2TXT/(1,39)_ocr')

    findblank('/Users/brobear/Downloads/新建文件夹 (2)','/Users/brobear/PycharmProjects/DOPDF2TXT/(1,39)',
              '/Users/brobear/PycharmProjects/DOPDF2TXT/(1,39)_blank_Txt','/Users/brobear/PycharmProjects/DOPDF2TXT/(1,39)_ocr')
