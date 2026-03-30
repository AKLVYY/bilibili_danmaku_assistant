import requests
import time
import qrcode
import json
import os
import sys
from typing import Literal
from bilibili_errors import format_bilibili_error

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'Origin': 'https://live.bilibili.com',
    'Referer': 'https://live.bilibili.com/',
}
REQUEST_TIMEOUT = 10


class LoginError(RuntimeError):
    pass


def _load_json_response(response: requests.Response, action: str) -> dict:
    response.raise_for_status()
    try:
        return response.json()
    except ValueError as exc:
        raise LoginError(f"{action}失败：接口返回了非 JSON 数据") from exc

def get_executable_dir():
    """获取程序运行的真实物理目录"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

COOKIE_PATH = os.path.join(get_executable_dir(), 'cookies.json')

def get_qrcode():
    qrcode_response = requests.get(
        'https://passport.bilibili.com/x/passport-login/web/qrcode/generate',
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT,
    )
    payload = _load_json_response(qrcode_response, "获取登录二维码")
    data = payload.get('data') or {}
    qrcode_key = data.get('qrcode_key')
    qrcode_url = data.get('url')
    if not qrcode_key or not qrcode_url:
        raise LoginError("获取登录二维码失败：响应缺少二维码信息")
    return qrcode_key, qrcode_url

def poll_if_scan(qrcode_key: str) -> Literal["Success", "Waiting", "Confirming", "Timeout"]:
    base_url = 'https://passport.bilibili.com/x/passport-login/web/qrcode/poll'
    params = {
        'qrcode_key': qrcode_key,
        'source': 'main-fe-header',
        'x-bili-locale-json': r'%7B%22c_locale%22:%7B%22language%22:%22zh%22,%22script%22:%22Hans%22%7D,%22always_translate%22:true%7D',
    }
    poll_response = requests.get(
        base_url,
        headers=HEADERS,
        params=params,
        timeout=REQUEST_TIMEOUT,
    )
    payload = _load_json_response(poll_response, "轮询扫码状态")
    data = payload.get('data') or {}
    code = data.get('code')
    if code == 0:
        with open(COOKIE_PATH, 'w', encoding='utf-8') as f:
            json.dump(requests.utils.dict_from_cookiejar(poll_response.cookies), f)
        return "Success"
    elif code == 86101:
        return "Waiting"
    elif code == 86090:
        return "Confirming"
    elif code == 86038:
        return "Timeout"
    message = data.get('message') or payload.get('message') or payload.get('msg') or '未知错误'
    raise LoginError(f"轮询扫码状态失败：{format_bilibili_error(code, message)}")

def check_cookie_valid() -> bool:
    """验证cookie是否有效"""
    if not os.path.exists(COOKIE_PATH):
        return False
        
    try:
        with open(COOKIE_PATH, 'r', encoding='utf-8') as f:
            cookie_dict = json.load(f)            
        nav_url = 'https://api.bilibili.com/x/web-interface/nav'
        response = requests.get(nav_url, headers=HEADERS, cookies=cookie_dict, timeout=5)
        data: dict = response.json()
        if data.get('code') == 0 and data.get('data', {}).get('isLogin'):
            return True
        return False
    except Exception:
        return False

if __name__ == '__main__':
    qrcode_key, qrcode_url = get_qrcode()
    img_qrcode = qrcode.make(qrcode_url)
    img_qrcode.show()
    while True:
        print("扫了吗？")
        poll_response = poll_if_scan(qrcode_key)
        print(poll_response)
        if poll_response in ("Success", "Timeout"):
            break
        time.sleep(2)
