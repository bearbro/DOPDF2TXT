# -*- coding: utf-8 -*-

import sys
import importlib
import os
import time

from OCR import pdf2txt_ocr

importlib.reload(sys)
import shutil
from pdfminer.pdfparser import PDFParser, PDFDocument, PDFSyntaxError, PDFEncryptionError, PSEOF
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import re


##记录日志
def writeFail(logfile, content):
    with open(logfile, 'a+', encoding='UTF-8') as f:  #
        f.write(content + '\n')


'''
 解析pdf 文本，保存到txt文件中
'''
def onePdf2Txt(path, outpath):
    fp = open(path, 'rb')  # 以二进制读模式打开
    # 用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)

    doc.set_parser(praser)  # WARNING:root:Parser index out of bounds

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
        for page in doc.get_pages():  # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    # if hasattr(x, "get_text"):
                    with open(outpath, 'a', encoding='UTF-8') as f:
                        results = x.get_text().strip()  # strip删除首尾空格和换行
                        # print(results)
                        f.write(results + '\n')


def dealFail(file, fileDir, message):
    if message == None:
        message = 'other'
    content = 'extract_fail:' + file + '\tmessage:' + message
    writeFail(fileDir + '_log.txt', content)

    filePath = fileDir + '/' + file
    faildir = fileDir + '/fail'
    if not os.path.exists(faildir):
        os.mkdir(faildir)

    if os.path.exists(faildir + '/' + file):  # 已经存在
        return
    shutil.copy2(filePath, faildir + '/' + file)


def manyPdfToTxt(fileDir, tarDir, mykey):
    time_start = time.time()
    if fileDir[-1] == '/':
        fileDir = fileDir[:-1]

    if tarDir[-1] == '/':
        tarDir = tarDir[:-1]

    files = os.listdir(fileDir)
    if not os.path.exists(tarDir):
        os.mkdir(tarDir)

    for file in files:
        if file.split('.')[-1] in ['pdf', 'PDF']:
            filePath = fileDir + '/' + file
            outPath = tarDir + '/' + file[:-4] + '.txt'
            if not os.path.exists(outPath):  # 已经存在则不再提取
                try:
                    onePdf2Txt(filePath, outPath)
                    if not os.path.exists(outPath):
                        raise PDFTextExtractionNotAllowed
                    else:
                        print("finish" + outPath)
                except (PDFSyntaxError, PDFEncryptionError, PSEOF, Exception) as e:  # 图片PDF
                    bufferDir = tarDir + '/' + file[:-4]
                    if not os.path.exists(outPath):  # 已经存在则不再提取
                        # ocr
                        pdf2txt_ocr(filePath, outPath, bufferDir, mykey)
                    print("finish" + outPath)

    time_end = time.time()
    print('time cost', time_end - time_start, 's')
    writeFail(fileDir + '_log.txt', 'time cost:' + str(int(time_end - time_start)) + 's')

# 演示 pdf 文字提取 耗时70s
if __name__ == "__main__":
    access_token_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
                       'client_id=7K4nVtmGK8z96aDqDVNC8iHS&' \
                       'client_secret=dloT1h4TDcEoN39uKbouekiIH18VYrfU'
    access_token = ''
    # 高精度版
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token='
    # 普通版
    url2 = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token='
    mykey = {'access_token_url': access_token_url, 'url': url, 'url2': url2, 'access_token': access_token, 'runtime': 0}
    manyPdfToTxt('./test/1',  # 输入文件夹
                 './test/1_txt',  # 输出文件夹
                 mykey=mykey
                 )
