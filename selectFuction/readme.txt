该包内容
3个PDF转txt的函数
    前两个Pdf2Txt.py,pdf2txt-2.py使用了包pdfminer3k
    另一个pdf2txt-3.py使用了包pdfminer.six

对比
    Pdf2Txt.py与pdf2txt-2.py对比
        生成的txt的内容基本相同
        Pdf2Txt.py
            存在生产大块空行的情况
        pdf2txt-2.py
            部分句子之间存在一个空行

    pdf2txt-2.py与pdf2txt-3.py对比
        两者内容大致相同
        pdf2txt-3.py
            也存在生产大块空行的情况
            存在少量语序混乱/丢失

结论
    选用pdf2txt-2.py文件中的转换函数

不足
    未处理pdf为图片组成的情况
