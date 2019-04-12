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
    sp[allPage-errPage]+=1
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
                pass
                # shutil.copy2(PDFDir+ '/' +  file[:-4] + '.pdf', pdfNDir + '/' + file[:-4] + '.pdf')
                # shutil.copy2(filePath, tarDir + '/' + file[:-4] + '.txt')



if __name__ == "__main__":

    # findblank('/Users/brobear/PycharmProjects/DOPDF2TXT/(1,39)_blank_Txt','/Users/brobear/PycharmProjects/DOPDF2TXT/(1,39)',
    #           '/Users/brobear/PycharmProjects/DOPDF2TXT/(1,39)_blank_Txt','/Users/brobear/PycharmProjects/DOPDF2TXT/(1,39)_ocr')
    sp = [0] * 1000
    findblank('/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/1,199_txt',#txt源
              '/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/page(1,199)',#pdf源
              '/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/1,199_blank_Txt',#txt输出
              '/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/page(1,199)_ocr'#pdf输出
              )
    findblank('/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/200,499_txt',  # txt源
              '/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/page(200,499)',  # pdf源
              '/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/200,499_blank_Txt',  # txt输出
              '/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/page(200,499)_ocr'  # pdf输出
              )
    ssp=sum(sp)
    for i in range(len(sp)):
        if(sp[i]!=0):
            print(str(i)+'页：'+str(sp[i])+'个\t'+('占%.2f%%' % (sp[i]/ssp*100)))
    print('共'+str(ssp)+'个')
'''
1页：8个	占0.38%
3页：1个	占0.05%
4页：6个	占0.29%
5页：5个	占0.24%
6页：8个	占0.38%
7页：5个	占0.24%
8页：10个	占0.48%
9页：19个	占0.90%
10页：15个	占0.71%
11页：10个	占0.48%
12页：39个	占1.86%
13页：48个	占2.28%
14页：25个	占1.19%
15页：48个	占2.28%
16页：41个	占1.95%
17页：29个	占1.38%
18页：37个	占1.76%
19页：51个	占2.43%
20页：61个	占2.90%
21页：52个	占2.47%
22页：70个	占3.33%
23页：38个	占1.81%
24页：64个	占3.04%
25页：48个	占2.28%
26页：45个	占2.14%
27页：76个	占3.62%
28页：71个	占3.38%
29页：58个	占2.76%
30页：52个	占2.47%
31页：47个	占2.24%
32页：39个	占1.86%
33页：42个	占2.00%
34页：56个	占2.66%
35页：41个	占1.95%
36页：54个	占2.57%
37页：41个	占1.95%
38页：42个	占2.00%
39页：27个	占1.28%
40页：33个	占1.57%
41页：37个	占1.76%
42页：37个	占1.76%
43页：30个	占1.43%
44页：33个	占1.57%
45页：36个	占1.71%
46页：38个	占1.81%
47页：25个	占1.19%
48页：20个	占0.95%
49页：28个	占1.33%
50页：33个	占1.57%
51页：24个	占1.14%
52页：19个	占0.90%
53页：19个	占0.90%
54页：25个	占1.19%
55页：11个	占0.52%
56页：21个	占1.00%
57页：17个	占0.81%
58页：14个	占0.67%
59页：17个	占0.81%
60页：9个	占0.43%
61页：9个	占0.43%
62页：10个	占0.48%
63页：9个	占0.43%
64页：12个	占0.57%
65页：2个	占0.10%
66页：8个	占0.38%
67页：6个	占0.29%
68页：3个	占0.14%
69页：5个	占0.24%
70页：8个	占0.38%
71页：6个	占0.29%
72页：3个	占0.14%
73页：2个	占0.10%
74页：1个	占0.05%
75页：2个	占0.10%
76页：7个	占0.33%
77页：2个	占0.10%
78页：3个	占0.14%
79页：3个	占0.14%
81页：2个	占0.10%
82页：1个	占0.05%
83页：5个	占0.24%
84页：2个	占0.10%
85页：2个	占0.10%
86页：3个	占0.14%
87页：5个	占0.24%
88页：1个	占0.05%
89页：1个	占0.05%
90页：2个	占0.10%
91页：1个	占0.05%
93页：2个	占0.10%
94页：1个	占0.05%
96页：1个	占0.05%
97页：2个	占0.10%
99页：3个	占0.14%
101页：1个	占0.05%
103页：2个	占0.10%
104页：1个	占0.05%
105页：1个	占0.05%
108页：1个	占0.05%
114页：1个	占0.05%
115页：1个	占0.05%
121页：1个	占0.05%
126页：1个	占0.05%
127页：1个	占0.05%
128页：1个	占0.05%
共2102个
'''

'''去除空页
0页：102个	占4.85%
1页：10个	占0.48%
2页：1个	占0.05%
3页：7个	占0.33%
4页：7个	占0.33%
5页：7个	占0.33%
6页：15个	占0.71%
7页：11个	占0.52%
8页：20个	占0.95%
9页：23个	占1.09%
10页：29个	占1.38%
11页：31个	占1.47%
12页：47个	占2.24%
13页：27个	占1.28%
14页：45个	占2.14%
15页：49个	占2.33%
16页：48个	占2.28%
17页：46个	占2.19%
18页：54个	占2.57%
19页：54个	占2.57%
20页：61个	占2.90%
21页：66个	占3.14%
22页：52个	占2.47%
23页：50个	占2.38%
24页：49个	占2.33%
25页：65个	占3.09%
26页：70个	占3.33%
27页：62个	占2.95%
28页：39个	占1.86%
29页：47个	占2.24%
30页：46个	占2.19%
31页：46个	占2.19%
32页：35个	占1.67%
33页：40个	占1.90%
34页：60个	占2.85%
35页：45个	占2.14%
36页：34个	占1.62%
37页：35个	占1.67%
38页：32个	占1.52%
39页：42个	占2.00%
40页：30个	占1.43%
41页：35个	占1.67%
42页：28个	占1.33%
43页：26个	占1.24%
44页：27个	占1.28%
45页：30个	占1.43%
46页：16个	占0.76%
47页：29个	占1.38%
48页：31个	占1.47%
49页：22个	占1.05%
50页：13个	占0.62%
51页：18个	占0.86%
52页：13个	占0.62%
53页：12个	占0.57%
54页：9个	占0.43%
55页：11个	占0.52%
56页：13个	占0.62%
57页：13个	占0.62%
58页：11个	占0.52%
59页：5个	占0.24%
60页：4个	占0.19%
61页：8个	占0.38%
62页：6个	占0.29%
63页：8个	占0.38%
64页：3个	占0.14%
65页：4个	占0.19%
66页：2个	占0.10%
67页：5个	占0.24%
68页：4个	占0.19%
69页：4个	占0.19%
70页：3个	占0.14%
71页：1个	占0.05%
73页：2个	占0.10%
74页：4个	占0.19%
75页：3个	占0.14%
76页：5个	占0.24%
77页：2个	占0.10%
78页：3个	占0.14%
79页：1个	占0.05%
80页：1个	占0.05%
81页：2个	占0.10%
83页：2个	占0.10%
84页：3个	占0.14%
85页：2个	占0.10%
86页：2个	占0.10%
87页：2个	占0.10%
88页：1个	占0.05%
89页：2个	占0.10%
90页：1个	占0.05%
91页：1个	占0.05%
93页：1个	占0.05%
94页：1个	占0.05%
95页：3个	占0.14%
101页：1个	占0.05%
102页：1个	占0.05%
104页：1个	占0.05%
107页：1个	占0.05%
120页：1个	占0.05%
共2102个
'''