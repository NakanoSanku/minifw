import json

import requests
from loguru import logger

from .pusher import Pusher, PusherOptions


class WxPusherOptions(PusherOptions):
    def __init__(self, content: str = None, summary: str = None, content_type: int = None, topic_ids: list[str] = None,
                 uids: list[str] = None, url: str = None,
                 verify_pay: bool = None, verify_pay_type: int = None):
        """
        {
          "appToken":"AT_xxx",//必传
          "content":"<h1>H1标题</h1><br/><p style=\"color:red;\">欢迎你使用WxPusher，推荐使用HTML发送</p>",//必传
          //消息摘要，显示在微信聊天页面或者模版消息卡片上，限制长度20(微信只能显示20)，可以不传，不传默认截取content前面的内容。
          "summary":"消息摘要",
          //内容类型 1表示文字  2表示html(只发送body标签内部的数据即可，不包括body标签，推荐使用这种) 3表示markdown
          "contentType":2,
          //发送目标的topicId，是一个数组！！！，也就是群发，使用uids单发的时候， 可以不传。
          "topicIds":[
              123
          ],
          //发送目标的UID，是一个数组。注意uids和topicIds可以同时填写，也可以只填写一个。
          "uids":[
              "UID_xxxx"
          ],
          //原文链接，可选参数
          "url":"https://wxpusher.zjiecode.com",
          //是否验证订阅时间，true表示只推送给付费订阅用户，false表示推送的时候，不验证付费，不验证用户订阅到期时间，用户订阅过期了，也能收到。
          //verifyPay字段即将被废弃，请使用verifyPayType字段，传verifyPayType会忽略verifyPay
          "verifyPay":false,
          //是否验证订阅时间，0：不验证，1:只发送给付费的用户，2:只发送给未订阅或者订阅过期的用户
          "verifyPayType":0
        }
        """
        self.content = content
        self.summary = summary
        self.content_type = content_type
        self.uids = uids
        self.topic_ids = topic_ids
        self.url = url
        self.verify_pay = verify_pay
        self.verify_pay_type = verify_pay_type

    def to_dict(self):
        data = {}
        if self.content:
            data["content"] = self.content
        if self.summary:
            data["summary"] = self.summary
        if self.content_type:
            data["contentType"] = self.content_type
        if self.uids:
            data["uids"] = self.uids
        if self.topic_ids:
            data["topicIds"] = self.topic_ids
        if self.url:
            data["url"] = self.url
        if self.verify_pay:
            data["verifyPay"] = self.verify_pay
        if self.verify_pay_type:
            data["verifyPayType"] = self.verify_pay_type
        return data


class WxPusher(Pusher):
    """
    推送消息到 WxPusher 应用
    """
    URL = "https://wxpusher.zjiecode.com/api/send/message"

    def __init__(self, token: str) -> None:
        super().__init__()
        self.token = token

    def send(self, options: WxPusherOptions):
        send_data = options.to_dict()
        send_data["appToken"] = self.token
        response = requests.post(
            url=WxPusher.URL,
            data=json.dumps(send_data).encode("utf-8"),
            headers={'Content-Type': 'application/json'}
        )
        response_data = response.json()
        if response.status_code == 200 and response_data["code"] == 1000:
            logger.info("WxPusher 发送通知成功")
            logger.info(response_data)
            return True
        else:
            logger.error("WxPusher 发送通知失败")
            logger.error(f"错误代码：{response.status_code}")
            logger.error(response_data)
            return False
