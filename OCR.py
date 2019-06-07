# coding:utf-8
import requests, base64, json, time
from pdf2image import convert_from_path
import tempfile
import os
import functools


def log(text):
    def decorator(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kw):
            s1 = time.time()
            r = fun(*args, **kw)
            s2 = time.time()
            print('%s %s %s ms' % (text, fun.__name__, 1000 * (s2 - s1)))
            return r

        return wrapper

    return decorator


def OCR(filepath, mykey):
    # 二进制方式打开图文件
    f = open(filepath, 'rb')
    # 参数image：图像base64编码
    img = base64.b64encode(f.read())
    params = {"image": img}
    for i in range(3):
        mykey['runtime'] += 1
        content = requests.post(
            url=(mykey['url'] + mykey['access_token']),
            data=params,
            headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if content.status_code == 200:
            txt = ''
            content_json = json.loads(content.text)
            if "error_code" not in content_json:
                for j in content_json["words_result"]:
                    txt += j["words"] + '\n'

                return txt
            elif content_json["error_code"] in [17, 19]:  # 每天请求量超限额 请求总量超限额
                if mykey['url'] == mykey['url2']:
                    raise NameError('每天请求量超限额')
                else:
                    mykey['url'] = mykey['url2']
            elif content_json["error_code"] in [18]:  # QPS超限额
                time.sleep(2)
            elif content_json["error_code"] in [100, 110,
                                                111]:  # 无效的access_token参数，请检查后重新尝试 access_token无效 access token过期
                for ik in range(3):
                    key = requests.get(mykey['access_token_url'])
                    if key.status_code == 200:
                        mykey['access_token'] = json.loads(key.text)['access_token']
                        break
        time.sleep(1)
    info = "------------------------Page " + filepath.split('_')[-1][:-4] + "  error----------------------------\n"
    file = filepath.split('/')[-2]
    print(file, info)

    return info


##pdf2txt by ocr
def pdf2txt_ocr(filename, outname, bufferDir, mykey):
    # print('filename=', filename)
    # print('outputDir=', outputDir)
    if not os.path.exists(bufferDir):
        os.mkdir(bufferDir)
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(filename)
        for index, img in enumerate(images):
            filepath = '%s/page_%s.png' % (bufferDir, index)
            #  能不能直接将img传入OCR，以减少io 影响不大，耗时的是request请求
            img.save(filepath)
            try:
                txt = OCR(filepath, mykey)
                with open(outname, 'a', encoding='UTF-8') as f:
                    f.write(txt)
            except NameError as e:
                if len(e.args) > 0 and e.args[0] == '每天请求量超限额':
                    if os.path.exists(outname):
                        os.remove(outname)
                    os.remove(filepath)
                    time.sleep(1)
                    os.removedirs(bufferDir)
                    print('本次运行调用api次数：' + str(mykey['runtime']))
                    raise e
                else:
                    raise e
            except Exception as e:
                print(e)
                print(filepath)
                with open(outname, 'w', encoding='UTF-8') as f:
                    f.write('error' + str(e))
                break
            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)
    time.sleep(1)
    os.removedirs(bufferDir)


@log('useTime')
def manyPdfToTxt_OCR(fileDir, tarDir, mykey):
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
            bufferDir = tarDir + '/' + file[:-4]
            if not os.path.exists(outPath):  # 已经存在则不再提取
                pdf2txt_ocr(filePath, outPath, bufferDir, mykey)


if __name__ == "__main__":
    access_token_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
                       'client_id=7K4nVtmGK8z96aDqDVNC8iHS&' \
                       'client_secret=dloT1h4TDcEoN39uKbouekiIH18VYrfU'
    access_token = ''
    # 高精度版
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token='
    # 普通版
    url2 = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token='
    mykey = {}
    mykey['access_token_url'] = access_token_url
    mykey['url'] = url
    mykey['url2'] = url2
    mykey['access_token'] = access_token
    mykey['runtime'] = 0
    manyPdfToTxt_OCR('/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/page(200,499)_ocr',  # 输入文件夹
                     '/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/page(200,499)_ocr_txt_api',  # 输出文件夹
                     mykey
                     )
    # manyPdfToTxt_OCR('./test/1',  # 输入文件夹
    #              './test/2_txt',  # 输出文件夹
    #              mykey=mykey
    #              )
