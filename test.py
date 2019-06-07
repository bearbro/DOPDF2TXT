import re
import os

def pageN(filename):
    f = open(filename,'r',errors='ignore') # 读模式
    allPage=0
    for line in f.readlines():
        line=line.replace('\x00\x00',' ').replace('\x00','')
        if re.match(r'-+Page [0-9]+-+',line)!=None:
            allPage+=1
    sp[allPage]+=1

if  __name__=='__main__':
    sp = [0] * 1000
    fileDir='/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/200,499_blank_Txt'
    files = os.listdir(fileDir)
    for file in files:
        if file.split('.')[-1] in ['txt']:
            filePath = fileDir + '/' + file
            pageN(filePath)


    ssp = sum(sp)
    sumpage=0
    for i in range(len(sp)):
        if (sp[i] != 0):
            print(str(i) + '页：' + str(sp[i]) + '个\t' + ('占%.2f%%' % (sp[i] / ssp * 100)))
            sumpage += i*sp[i]
    print('共' + str(ssp) + '个')
    print('共' + str(sumpage) + '页')