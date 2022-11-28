# 百度通用翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
import http.client
import hashlib
import urllib
import random
import json
# 要注意ip地址：112.91.150.34 or 117.136.79.228


def translate(q, fromLang, toLang, appid, secretKey):
    salt = random.randint(32768, 65536)
    myurl = '/api/trans/vip/translate'
    httpClient = None
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        # if success then get the result
        return_result = result["trans_result"][0]["dst"]

    # else get the error message
    except Exception as e:
        return_result = e

    finally:
        if httpClient:
            httpClient.close()

    # return the result
    return return_result


# # # 测试英文翻译中文
# appid = '20220713001272202'  # 填写你的appid
# secretKey = 'v4x3PC6W6X9etHyXO5wu'  # 填写你的密钥
# fromLang = 'auto'  # 原文语种
# toLang = 'zh'  # 译文语种
# query = 'Where is the position of UIC?'
# re = translate(query, fromLang, toLang, appid, secretKey)
# print(query)
# print(re)
# print(type(re))
