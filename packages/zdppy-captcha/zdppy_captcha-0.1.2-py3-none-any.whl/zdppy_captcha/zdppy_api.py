from .tobase64 import get_base64


def get_captcha_api(success):
    async def index(r):
        # TODO: code 记录下来，用于另一个接口进行比对
        code, img = get_base64(6)
        return success({"key":"xxx", "base64img": img})

    return index
