import json

import requests
from loguru import logger

from minifw.pusher.pusher import Pusher, PusherOptions


class ServerGirlOptions(PusherOptions):
    def __init__(self, title: str, desp=None, short=None, noip=None, channel=None, openid=None):
        """
        Initialize a ServerGirlOptions object with default or provided values.

        Parameters:
            title (str): 标题，必填
            desp (str, optional): 消息内容，选填。支持 Markdown语法 ，最大长度为 32KB ,消息卡片截取前 30 显示
            short (str, optional): 消息卡片内容，选填。最大长度64。如果不指定，将自动从desp中截取生成。
            noip (str, optional): 是否隐藏调用IP，选填。如果不指定，则显示；为1则隐藏。
            channel (str, optional): 动态指定本次推送使用的消息通道，选填。如不指定，则使用网站上的消息通道页面设置的通道。支持最多两个通道，多个通道值用竖线|隔开。比如，同时发送服务号和企业微信应用消息通道，则使用 9|66 。通道对应的值如下：
                -  官方Android版·β=98
                -  企业微信应用消息=66
                -  企业微信群机器人=1
                -  钉钉群机器人=2
                -  飞书群机器人=3
                -  Bark iOS=8
                -  测试号=0
                -  自定义=88
                -  PushDeer=18
                -  方糖服务号=9
            openid (str, optional): 消息抄送的openid. Defaults to None.

        Returns:
            None
        """
        self.title = title
        self.desp = desp
        self.short = short
        self.noip = noip
        self.channel = channel
        self.openid = openid

    def to_dict(self):
        data = {"title": self.title}
        if self.desp:
            data["desp"] = self.desp
        if self.short:
            data["short"] = self.short
        if self.noip:
            data["noip"] = self.noip
        if self.channel:
            data["channel"] = self.channel
        if self.openid:
            data["openid"] = self.openid
        return data


class ServerGirl(Pusher):
    """
    推送消息到 Server酱 应用
    https://sct.ftqq.com/sendkey
    """
    URL = "https://sctapi.ftqq.com"

    def __init__(self, token: str) -> None:
        super().__init__()
        self.token = token
        self.send_url = f"{ServerGirl.URL}/{self.token}.send"

    def send(self, options: ServerGirlOptions):
        response = requests.post(
            url=self.send_url,
            data=json.dumps(options.to_dict()).encode("utf-8"),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            logger.info("Server酱 发送通知成功")
            logger.info(response.json())
            return True
        else:
            logger.error("Server酱 发送通知失败")
            logger.error(f"错误代码：{response.status_code}")
            return False

