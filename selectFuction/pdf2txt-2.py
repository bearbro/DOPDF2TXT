#!/usr/bin/env python
# coding:utf8
# author:Z time:2018/7/30

import sys
import importlib

import os

importlib.reload(sys)

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

'''
 解析pdf 文本，保存到txt文件中
'''

def onePdf2Txt(path,outpath):
    fp = open(path, 'rb') # 以二进制读模式打开
    #用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)#WARNING:root:Parser index out of bounds

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    with open(outpath, 'a') as f:
                        results = x.get_text().strip()#strip删除首尾空格和换行
                        # print(results)
                        f.write(results+'\n')

def manyPdfToTxt (fileDir,tarDir):
    if fileDir[-1]=='/':
        fileDir=fileDir[:-1]

    if tarDir[-1]=='/':
        tarDir=tarDir[:-1]

    files = os.listdir(fileDir)
    if not os.path.exists(tarDir):
        os.mkdir(tarDir)

    for file in files:
        if file.split('.')[-1] in ['pdf' ,'PDF']:
            filePath = fileDir+'/'+file
            outPath = tarDir+'/'+file[:-4]+'.txt'
            onePdf2Txt(filePath, outPath)
            print("saved in"+outPath)


if __name__ == "__main__":
    manyPdfToTxt('./','./p2t-2')

##与Pdf2Txt.py相比，少了一些空行块，多了一些零散的空行
