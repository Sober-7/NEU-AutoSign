#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests
import re
import time
import json

login_payload = {'username': 20194974, # 在这里填写用户名
                'grant_type': 'password',
                'password': 201094, # 在这里填写密码
                'imageCodeResult':'' ,
                'imageKey':'' }
post_data = {} # 在这里填写个人数据
__headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
             'Content-Type': 'application/json;charset=UTF-8',
             'Authorization': 'Basic dnVlOnZ1ZQ=='}
SCKEY = "" # Server酱的Token

login_page = requests.post("http://stuinfo.neu.edu.cn/api/auth/oauth/token",
                            headers = __headers,
                            params = login_payload,
                            data = dict([('_t',int(time.time()))]))
__cookies = dict(accessToken=re.findall(r'token\":\"(.*?)\"',login_page.text,re.S|re.M)[0],
            userName=str(login_payload['username']))
__headers['Authorization'] = 'Bearer ' + __cookies['accessToken']
get_sign_page = requests.post("http://stuinfo.neu.edu.cn/cloud-xxbl/studenLogin",
                            headers = __headers,
                            data = dict([('_t',int(time.time()))]))

try :
    assert(re.findall(r'success":true',get_sign_page.text,re.S|re.M)[0]=='success":true') 
    print('[ + ] Login success.')
except:
    print('[ - ] Login error.')
    print(get_sign_page.text)
    if SCKEY:
        requests.get('https://sc.ftqq.com/'+SCKEY+'.send',params = dict(text='Something wrong.',desp='Login error.'))
    sys.exit(0)
    
sign_page = requests.get("http://stuinfo.neu.edu.cn/cloud-xxbl/studentinfo",
                            headers = __headers,
                            params = dict(tag=re.findall(r'data\":\"(.*?)\"',get_sign_page.text,re.S|re.M)[0]),
                            cookies = __cookies)
__cookies['JSESSIONID'] = sign_page.cookies['JSESSIONID']

sign = requests.post("http://stuinfo.neu.edu.cn/cloud-xxbl/updateStudentInfo",
                    headers = __headers,
                    params = dict([('t',int(time.time()))]),
                    data = json.dumps(post_data),
                    cookies = __cookies)
try :
    assert(re.findall(r'success":true',sign.text,re.S|re.M)[0]=='success":true' )
    print('[ + ] Sign success.')
except:
    print('[ - ] Sign error.')
    print(sign.text)
    if SCKEY:
        requests.get('https://sc.ftqq.com/'+SCKEY+'.send',params = dict(text='Something wrong.',desp='Sign error. '+sign.text))
    sys.exit(0)

verify = requests.get("http://stuinfo.neu.edu.cn/cloud-xxbl/getStudentInfo",
                    headers = __headers,
                    cookies = __cookies)
try :
    assert(re.findall(r'success":true',verify.text,re.S|re.M)[0]=='success":true') 
    print('[ + ] Verify success.')
    if SCKEY:
        requests.get('https://sc.ftqq.com/'+SCKEY+'.send',params = dict(text='Bonjour, Sir.',desp='AutoSign completed successfully.'))
except:
    print('[ - ] Verify error.')
    if SCKEY:
        requests.get('https://sc.ftqq.com/'+SCKEY+'.send',params = dict(text='Something wrong.',desp='Verify error. '+verify.text))
