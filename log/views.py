from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import re
import datetime
import requests
import json

# Create your views here.
def get_all_log(request):
    # 载入日志
    logs = open(r'/tmp/modsec_audit.log','r').read()
    logs = re.finditer(r"---[\da-zA-Z]{8}---A--[\s\S]*?---[\da-zA-Z]{8}---Z--",logs)

    # ip_loc_cache = {}

    # # 获取ip物理位置
    # def get_loc(ip):
    #     url = 'https://restapi.amap.com/v3/ip?key=0113a13c88697dcea6a445584d535837'
    #     headers = {
    #     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
    #     }
    #     data = {'ip':ip}
    #     result = requests.post(url,data)
    #     html = result.content.decode('utf-8')
    #     html = json.loads(html)
    #     return html['province'] + ' ' + html['city']

    reqjson = []
    logNum = 0
    # 解析日志
    for log in logs:
        # 原始日志
        original = log.group()

        # 攻击时间
        attTime = re.search(r"\d\d/[a-zA-Z]{3}/\d{4}:\d{2}:\d{2}:\d{2}", original).group()
        attTime = datetime.datetime.strptime(attTime, "%d/%b/%Y:%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        
        # 攻击URL = Host + URI （改为攻击HOST）
        attHost = re.search(r"Host: (.*?)\n", original)[1] # 攻击Host
        attURI = re.search(r" (.*?) HTTP", original)[1] # 攻击URI
        attURL = attHost + attURI if attURI != '/' else attHost

        # 攻击IP
        attIP = re.search(r"---A--\n\[.*?\] \d+ (.*?) ", original)[1]

        # 攻击地址,调用ip138的API
        # if attIP in ip_loc_cache:
        #     attLoc = ip_loc_cache[attIP]
        # else:
        #     attLoc = get_loc(attIP)
        #     ip_loc_cache[attIP] = attLoc

        # 攻击类型(??)  （改为攻击URI）
        # attType = ""

        # 规则ID（命中多条规则）
        ruleIDs = []
        it_kid = re.finditer('\[id\s"\d+?"\]', original)
        for match_kid in it_kid:
            ruleIDs.append(match_kid.group().replace('[id "','').replace('"]',''))

        # 请求方法
        reqMethod = re.search(r"---B--\n(.*?) ", original)[1]

        # 请求信息 reqInfo（改为规则信息）
        ruleMsgs = []
        it_kid = re.finditer('msg ".*?"', original)
        for match_kid in it_kid:
            ruleMsgs.append(match_kid.group().replace('msg "','').replace('"',''))

        # 处理方式
        actts = []
        it_kid = re.finditer('ModSecurity: .*? Matched', original)
        for match_kid in it_kid:
            actts.append(match_kid.group().replace('ModSecurity: ','').replace('. Matched',''))

        # 日志标志
        # logNum
        
        for ruleID,ruleMsg,actt in zip(ruleIDs,ruleMsgs,actts):
            logNum += 1
            req = {"attTime":attTime, "attHost":attHost, "attIP":attIP, "attURI":attURI, "ruleID":ruleID, "reqMethod":reqMethod, "ruleMsg":ruleMsg, "actt":actt, "logNum":logNum}
            reqjson.append(req)

    return JsonResponse(reqjson,safe=False)

def get_selected_log(request):
# 载入日志
    logs = open(r'/tmp/modsec_audit.log','r').read()
    logs = re.finditer(r"---[\da-zA-Z]{8}---A--[\s\S]*?---[\da-zA-Z]{8}---Z--",logs)

    # ip_loc_cache = {}

    # # 获取ip物理位置
    # def get_loc(ip):
    #     url = 'https://restapi.amap.com/v3/ip?key=0113a13c88697dcea6a445584d535837'
    #     headers = {
    #     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
    #     }
    #     data = {'ip':ip}
    #     result = requests.post(url,data)
    #     html = result.content.decode('utf-8')
    #     html = json.loads(html)
    #     return html['province'] + ' ' + html['city']

    reqjson = []
    logNum = 0
    # 解析日志
    for log in logs:
        # 原始日志
        original = log.group()

        # 攻击时间
        attTime = re.search(r"\d\d/[a-zA-Z]{3}/\d{4}:\d{2}:\d{2}:\d{2}", original).group()
        attTime = datetime.datetime.strptime(attTime, "%d/%b/%Y:%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        
        # 攻击URL = Host + URI （改为攻击HOST）
        attHost = re.search(r"Host: (.*?)\n", original)[1] # 攻击Host
        attURI = re.search(r" (.*?) HTTP", original)[1] # 攻击URI
        attURL = attHost + attURI if attURI != '/' else attHost

        # 攻击IP
        attIP = re.search(r"---A--\n\[.*?\] \d+ (.*?) ", original)[1]

        # 攻击地址,调用ip138的API
        # if attIP in ip_loc_cache:
        #     attLoc = ip_loc_cache[attIP]
        # else:
        #     attLoc = get_loc(attIP)
        #     ip_loc_cache[attIP] = attLoc

        # 攻击类型(??)  （改为攻击URI）
        # attType = ""

        # 规则ID（命中多条规则）
        ruleIDs = []
        it_kid = re.finditer('\[id\s"\d+?"\]', original)
        for match_kid in it_kid:
            ruleIDs.append(match_kid.group().replace('[id "','').replace('"]',''))

        # 请求方法
        reqMethod = re.search(r"---B--\n(.*?) ", original)[1]

        # 请求信息 reqInfo（改为规则信息）
        ruleMsgs = []
        it_kid = re.finditer('msg ".*?"', original)
        for match_kid in it_kid:
            ruleMsgs.append(match_kid.group().replace('msg "','').replace('"',''))

        # 处理方式
        actts = []
        it_kid = re.finditer('ModSecurity: .*? Matched', original)
        for match_kid in it_kid:
            actts.append(match_kid.group().replace('ModSecurity: ','').replace('. Matched',''))

        # 日志标志
        # logNum
        
        for ruleID,ruleMsg,actt in zip(ruleIDs,ruleMsgs,actts):
            logNum += 1
            req = {"attTime":attTime, "attHost":attHost, "attIP":attIP, "attURI":attURI, "ruleID":ruleID, "reqMethod":reqMethod, "ruleMsg":ruleMsg, "actt":actt, "logNum":logNum}
            reqjson.append(req)

    return JsonResponse(reqjson,safe=False)

def get_detailed_log(request):
    # 载入日志
    logs = open('/tmp/modsec_audit.log','r').read()
    logs = re.finditer(r"---[\da-zA-Z]{8}---A--[\s\S]*?---[\da-zA-Z]{8}---Z--",logs)

    logNum = 0
    reqjson = []
    # 解析日志
    for log in logs:
        # 原始日志
        original = log.group()
        requestbody = re.search(r'---B--\n((.|\n)*?)---', original)[1]
        # attIP = re.search(r"---A--\n\[.*?\] \d+ (.*?) ", original)[1]
        responsebody = re.search(r'---F--\n((.|\n)*?)---', original)[1]
        logNum += 1
        reqjson.append({'t':requestbody + responsebody,'logNum':logNum})
    return JsonResponse(reqjson,safe=False)