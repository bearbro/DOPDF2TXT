# coding:utf-8
import requests, base64,json,time
import os



def OCR(filepath,mykey):
    # 二进制方式打开图文件
    f = open(filepath, 'rb')
    # 参数image：图像base64编码
    img = base64.b64encode(f.read())
    params = {"image": img}
    for i in range(3):
        content=requests.post(
            url=(mykey['url'] + mykey['access_token']),
            data=params,
            headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if content.status_code == 200:
            txt = ''
            content_json = json.loads(content.text)
            if "error_code" not in content_json:
                for j in content_json["words_result"]:
                    txt += j["words"]+'\n'

                return txt
            elif content_json["error_code"] in [17,19]:#	每天请求量超限额 请求总量超限额
                if mykey['url']==mykey['url2']:
                    raise NameError('每天请求量超限额')
                else:
                    mykey['url'] = mykey['url2']
            elif content_json["error_code"] in [18]:  #  QPS超限额
                time.sleep(2)
            elif content_json["error_code"] in [100,110,111]:  #无效的access_token参数，请检查后重新尝试 access_token无效 access token过期
                for ik in range(3):
                    key = requests.get(access_token_url)
                    if key.status_code == 200:
                        mykey['access_token']=json.loads(key.text)['access_token']
                        break
        time.sleep(1)
    info="------------------------Page "+filepath.split('_')[-1][:-4]+"  error----------------------------\n"
    file=filepath.split('/')[-2]
    print(file,info)

    return info
def manyPdfToTxt_OCR (fileDir,tarDir,mykey):
    if fileDir[-1]=='/':
        fileDir=fileDir[:-1]

    if tarDir[-1]=='/':
        tarDir=tarDir[:-1]

    files = os.listdir(fileDir)
    if not os.path.exists(tarDir):
        os.mkdir(tarDir)

    for file in files:
        filePath = fileDir+'/'+file
        outname = tarDir+'/'+file+'.txt'
        if not os.path.exists(outname):#已经存在则不再提取
            if not os.path.isdir(filePath):
                continue
            print(filePath)
            index=0
            while True:
                imagepath='%s/page_%s.png' % (filePath, index)
                index+=1
                if not os.path.exists(imagepath):
                    break
                try:
                    txt = OCR(imagepath, mykey)
                    with open(outname, 'a', encoding='UTF-8') as f:
                        f.write(txt)
                except NameError as e:
                    if len(e.args) > 0 and e.args[0] == '每天请求量超限额':
                        if os.path.exists(outname):
                            os.remove(outname)
                        raise e
                    else:
                        raise e
                except Exception as e:
                    print(e)
                    print(imagepath)
                    with open(outname, 'w', encoding='UTF-8') as f:
                        f.write('error' + str(e))
                    break
                with open(outname, 'a', encoding='UTF-8') as f:
                    f.write(txt)

if __name__ == "__main__":
    access_token_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
                       'client_id=7K4nVtmGK8z96aDqDVNC8iHS&' \
                       'client_secret=dloT1h4TDcEoN39uKbouekiIH18VYrfU'
    access_token = ''
    # 高精度版
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token='
    # 普通版
    url2 = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token='
    mykey={}
    mykey['access_token_url']=access_token_url
    mykey['url']=url2
    mykey['url2']=url2
    mykey['access_token']=access_token


    manyPdfToTxt_OCR('/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/page(200,499)_ocr_images',
                    '/Users/brobear/OneDrive/data-whitepaper/DOPDF2TXT/page(200,499)_ocr_txt_api_general',
                    mykey
                    )
