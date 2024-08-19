import base64
import hashlib
import hmac
import json
from datetime import datetime
from time import mktime
from urllib.parse import urlparse, urlencode
from wsgiref.handlers import format_date_time

import cv2
import requests
from loguru import logger

from minifw.common import Rect
from minifw.ocr.ocr import OcrResult, OcrProvider


class XfOcrOptions:
    def __init__(self, data_image: cv2.Mat, category: str = "ch_en_public_cloud", header_status: int = 3,
                 result_encoding: str = "utf8", result_compress: str = "raw", result_format: str = "json",
                 data_encoding: str = "jpg", data_status: int = 3, xf_ocr_secret_port="sf8e6aca1") -> None:
        # 获取图片的base64编码
        _, image_data = cv2.imencode(f".{data_encoding}", data_image)
        image_base64_str = str(base64.b64encode(image_data.tobytes()).decode("utf-8"))

        self.data_image = image_base64_str
        self.category = category
        self.data_status = data_status
        self.data_encoding = data_encoding
        self.result_compress = result_compress
        self.result_encoding = result_encoding
        self.result_format = result_format
        self.header_status = header_status
        self.xf_ocr_secret_port = xf_ocr_secret_port

    def to_dict(self):
        return {
            "header": {
                "status": self.header_status
            },
            "payload": {
                f"{self.xf_ocr_secret_port}_data_1": {
                    "image": self.data_image,
                    "status": self.data_status,
                    "encoding": self.data_encoding
                }
            },
            "parameter": {
                self.xf_ocr_secret_port: {
                    "category": self.category,
                    "result": {
                        "compress": self.result_compress,
                        "encoding": self.result_encoding,
                        "format": self.result_format
                    }
                }
            }
        }


class XfOcr:
    URL = "https://api.xf-yun.com/v1/private/"

    def __init__(self, app_id: str, api_key: str, api_secret: str, xf_ocr_secret_port="sf8e6aca1") -> None:
        # 调用密钥
        self.app_id = app_id
        # 鉴权密钥
        self.app_key = api_key
        self.app_secret = api_secret
        # 获取鉴权的地址
        u = urlparse(f"{XfOcr.URL}{xf_ocr_secret_port}")
        date = format_date_time(mktime(datetime.now().timetuple()))
        signature_origin = f"host: {u.hostname}\ndate: {date}\nPOST {u.path} HTTP/1.1"
        signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'), hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode('utf-8')
        authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
        query_params = {
            "host": u.hostname,
            "date": date,
            "authorization": authorization
        }
        self.url = f"{XfOcr.URL}{xf_ocr_secret_port}?{urlencode(query_params)}"
        logger.info(f"讯飞OCR鉴权后的地址：{self.url}")

    def send(self, options: XfOcrOptions) -> dict | None:
        send_data = options.to_dict()
        send_data["header"]["app_id"] = self.app_id
        response = requests.post(self.url,
                                 data=json.dumps(send_data),
                                 headers={'content-type': "application/json", 'host': 'api.xf-yun.com',
                                          'app_id': self.app_id})

        if response.status_code == 200:
            temp_result = json.loads(response.content.decode())
            final_result = base64.b64decode(temp_result["payload"]["result"]["text"]).decode()
            final_result = final_result.replace(" ", "").replace("\n", "").replace("\t", "").strip()
            json_result = json.loads(final_result)
            logger.info(f"识别结果：{json_result}")
            return json_result
        else:
            logger.error(f"识别失败，错误码：{response.status_code}")
            logger.error(f"错误信息：{response.content}")
            return None


class XfOcrProvider(OcrProvider):
    """
    讯飞OCR服务提供者
    """
    NAME = "讯飞"

    def __init__(self, app_id: str, api_key: str, api_secret: str, xf_ocr_options: XfOcrOptions):
        super().__init__()
        self.provider = XfOcr(app_id, api_key, api_secret)
        self.xf_ocr_options = xf_ocr_options

    def run(self, image: cv2.Mat) -> list[OcrResult] | None:
        result = self.provider.send(XfOcrOptions(
            data_image=image,
            category=self.xf_ocr_options.category,
            data_status=self.xf_ocr_options.data_status,
            data_encoding=self.xf_ocr_options.data_encoding,
            result_compress=self.xf_ocr_options.result_compress,
            result_encoding=self.xf_ocr_options.result_encoding,
            result_format=self.xf_ocr_options.result_format,
            header_status=self.xf_ocr_options.header_status,
            xf_ocr_secret_port=self.xf_ocr_options.xf_ocr_secret_port
        ))
        if result is not None:
            return [
                OcrResult(
                    text=r["words"][0]["content"],
                    confidence=r["conf"],
                    region=Rect(
                        x=int(r["coord"][0]["x"]),
                        y=int(r["coord"][0]["y"]),
                        w=int(r["coord"][2]["x"]) - int(r["coord"][0]["x"]),
                        h=int(r["coord"][2]["y"]) - int(r["coord"][0]["y"])
                    )) for r in result["pages"][0]["lines"]]
        return None
