# coding:utf-8
import requests, base64,json,time





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
                mykey['url']=mykey['url2']
            elif content_json["error_code"] in [18]:  #  QPS超限额
                time.sleep(2)
            elif content_json["error_code"] in [100,110,111]:  #无效的access_token参数，请检查后重新尝试 access_token无效 access token过期
                for ik in range(3):
                    key = requests.get(access_token_url)
                    if key.status_code == 200:
                        mykey['access_token']=json.loads(key.text)['access_token']
                        break
    info="------------------------Page "+filepath.split('_')[-1][:-4]+"  error----------------------------\n"
    file=filepath.split('/')[-2]
    print(file,info)

    return info





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
    mykey['url']=url
    mykey['url2']=url2
    mykey['access_token']=access_token

    imagePath=r'/Users/brobear/Desktop/9-1/page_0.png'
    t=OCR(imagePath,mykey)
    print(t)
