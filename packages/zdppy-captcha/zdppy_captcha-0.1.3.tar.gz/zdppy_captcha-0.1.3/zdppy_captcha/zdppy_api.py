from .tobase64 import get_base64


def get(success, num=4):
    """
    获取zdppy_api生成验证码的接口
    :param num: 验证码的个数
    :param success: api.resp.success 是zdppy_api框架中统一返回成功结果的方法
    :return:
    """
    async def get_captcha(req):
        key, code, img = get_base64(num)
        return success({
            "key": key,
            "img": img,
        })

    return get_captcha
