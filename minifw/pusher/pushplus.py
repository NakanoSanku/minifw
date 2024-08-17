import json

import requests
from loguru import logger

from .pusher import PusherOptions, Pusher


class PushPlusOptions(PusherOptions):
    def __init__(self, content: str, title=None, topic=None, template="html", channel="wechat", webhook=None,
                 call_back_url=None, timestamp=None, to=None) -> None:
        """
        Initialize a PushPlusOptions object with default or provided values.

        Parameters:
            content (str): 文本内容.
            title (str, optional): 消息标题. Defaults to None.
            topic (str, optional): 群组编码,不填仅发送给自己,channel为webhook时无效. Defaults to None.
            template (str, optional): 发送模板. Defaults to "html".
                - html 文本消息
                - markdown  Markdown消息
                - txt 文本消息
                - json json格式文本
                - cloudMonitor 阿里云监控报警定制模板
                - jenkins jenkins插件定制模板
                - route 路由器插件定制模板
                - pay 支付成功通知模板
            channel (str, optional): 发送渠道. Defaults to "wechat".
                - wechat 微信公众号
                - webhook 第三方webhook
                - cp 企业微信应用
                - mail 邮箱
                - sms 短信
            webhook (str, optional): webhook编码. Defaults to None.
            call_back_url (str, optional): 发送结果回调地址. Defaults to None.
            timestamp (str, optional): 毫秒时间戳。格式如:1632993318000。服务器时间戳大于此时间戳,则消息不会发送. Defaults to None.
            to (str, optional): 好友令,微信公众号渠道填写好友令牌,企业微信渠道填写企业微信用户id. Defaults to None.

        Returns:
             None
        """
        self.content = content
        self.title = title
        self.topic = topic
        self.template = template
        self.channel = channel
        self.webhook = webhook
        self.call_back_url = call_back_url
        self.timestamp = timestamp
        self.to = to

    def to_dict(self):
        data = {"content": self.content}
        if self.title:
            data["title"] = self.title
        if self.topic:
            data["topic"] = self.topic
        if self.template:
            data["template"] = self.template
        if self.channel:
            data["channel"] = self.channel
        if self.webhook:
            data["webhook"] = self.webhook
        if self.call_back_url:
            data["callbackUrl"] = self.call_back_url
        if self.timestamp:
            data["timestamp"] = self.timestamp
        if self.to:
            data["to"] = self.to
        return data


class PushPlus(Pusher):
    """
    推送消息到 PushPlus 应用
    https://www.pushplus.plus
    """
    URL = "https://www.pushplus.plus"
    SEND_API = URL + "/send"

    def __init__(self, token: str) -> None:
        super().__init__()
        self.token = token

    def send(self, options: PushPlusOptions) -> bool:
        send_data = {
            "token": self.token,
        }
        if options:
            send_data.update(**options.to_dict())
        response = requests.post(
            url=PushPlus.SEND_API,
            data=json.dumps(send_data).encode("utf-8"),
            headers={'Content-Type': 'application/json'}
        )
        response_data = response.json()
        if response_data["code"] == 200:
            logger.info("Send success")
            logger.info(response_data["msg"])
            return True
        elif response_data["code"] == 999:
            logger.error("Failed to send")
            logger.error(response_data["msg"])
            return False