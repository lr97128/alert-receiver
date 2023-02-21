#!/usr/bin/python3
# -*- coding:utf-8 -*-
_author_ = "liurui"

from http.client import HTTPSConnection
from sqlite3 import Timestamp
import ssl
import hashlib
import base64
import hmac
import time
import json

def gen_sign(timestamp, secret):
  # 拼接timestamp和secret
  string_to_sign = '{}\n{}'.format(timestamp, secret)
  hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
  
  # 对结果进行base64处理
  sign = base64.b64encode(hmac_code).decode('utf-8')
  
  return sign

if __name__ == '__main__':
    secret = "SIuvv0jrGqdsc5bPj5oqGg"
    timestamp = int(time.time())
    sign = gen_sign(timestamp,secret)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
    }
    data = {"timestamp": timestamp, "sign": sign, "msg_type": "interactive", "card": {"config": {"wide_screen_mode": "true"}, "header": {"template": "red", "title": {"content": "中海庭运维组告警", "tag": "plain_text"}}, "elements": [{"tag": "div", "text": {"content": "<at id=all>所有人</at>", "tag": "lark_md"}}]}}
    beyond = json.dumps(data, sort_keys=False, indent=4 ,separators=(',', ': ')).encode('utf-8').decode('latin1')
    print(beyond)
    body = """ {
        {
	"msg_type": "post",
	"content": {
		"post": {
			"zh_cn": {
				"title": "中海庭运维组告警",
				"content": [
					[{
							"tag": "text",
							"text": "kafka集群有告警\n"
						},
						{
							"tag": "a",
							"text": "请查看",
							"href": "https://www.baidu.com/"
						},
						{
							"tag": "at",
							"user_id": "all"
						}
					]
				]
			}
		}
	}
}  
    """.encode('utf-8').decode('latin1')
    print(body)
    cxt = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    conn = HTTPSConnection(host="open.feishu.cn", context=cxt)
    conn.request(method="GET", url="https://open.feishu.cn/open-apis/bot/v2/hook/cc5c69be-e0d3-42f5-ad15-4526a262fe07", headers=headers, body=body)
    res = conn.getresponse()
    print(res.status, res.info())
    res.close()
    conn.close()