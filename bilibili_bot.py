import requests
import urllib.parse
import hashlib
import re
import time
import json
import os
from bilibili_login import COOKIE_PATH, HEADERS

# ==========================================
# 1. 全局配置区 (Constants & Config)
# ==========================================
MIXIN_KEY_ENC_TAB = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]

def load_fresh_auth():
    """动态读取最新的 Cookie 和 Token"""
    if not os.path.exists(COOKIE_PATH):
        raise FileNotFoundError("本地无登录凭证，请先扫码登录！")
        
    with open(COOKIE_PATH, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
        
    cookies['buvid3'] = '5F73AD2E-CB24-B33E-AF6A-C868D9A8E22A18553infoc'
    cookies['buvid4'] = 'A70DCB7E-96CC-CD0E-8589-C92FB384798D22277-025052022-Xk7VGw3AS1BlWte9EP8pBQ%3D%3D'
    
    csrf_token = cookies.get('bili_jct', '')
    uid = cookies.get('DedeUserID', '')
    
    return cookies, csrf_token, uid

# ==========================================
# 2. 解密w_rid
# ==========================================
def get_wbi_keys():
    """获取全局 WBI 密钥"""
    cookies, _, _ = load_fresh_auth()
    response = requests.get('https://api.bilibili.com/x/web-interface/nav', headers=HEADERS, cookies=cookies)
    img_url: str = response.json()['data']['wbi_img']['img_url']
    sub_url: str = response.json()['data']['wbi_img']['sub_url']
    return img_url.split('/')[-1].split('.')[0], sub_url.split('/')[-1].split('.')[0]

def get_mixin_key(img_key: str, sub_key: str) -> str:
    raw_key = img_key + sub_key
    return "".join([raw_key[i] for i in MIXIN_KEY_ENC_TAB if i < len(raw_key)])[:32]

def generate_wbi_signature(params: dict, img_key: str, sub_key: str) -> dict:
    """WBI"""
    mixin_key = get_mixin_key(img_key, sub_key)
    params['wts'] = round(time.time()) 
    
    query_list = []
    for key in sorted(params.keys()):
        val = str(params[key])
        val = re.sub(r"[!'()*]", "", val)
        query_list.append(f"{urllib.parse.quote(key)}={urllib.parse.quote(val)}")
        
    hash_input = "&".join(query_list) + mixin_key
    params['w_rid'] = hashlib.md5(hash_input.encode('utf-8')).hexdigest()
    return params

# ==========================================
# 3. 核心业务动作 (Actions)
# ==========================================
def get_anchor_id(room_id):
    """返回主播 UID"""
    url = f'https://api.live.bilibili.com/live_user/v1/UserInfo/get_anchor_in_room?roomid={room_id}'
    try:
        response = requests.get(url, headers=HEADERS)
        res_json = response.json()
        if res_json.get("code") == 0:
            info_dict = res_json.get("data", {}).get("info")
            if info_dict is not None:
                return str(info_dict.get("uid"))
        else:
            return None
    except Exception:
        return None

def get_anchor_name(room_id):
    """返回主播昵称"""
    url = f"https://api.live.bilibili.com/live_user/v1/UserInfo/get_anchor_in_room?roomid={room_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        res_json = response.json()
        if res_json.get("code") == 0:
            info_dict = res_json.get("data", {}).get("info")
            if info_dict is not None:
                return info_dict.get("uname")
        else:
            return None            
    except Exception:
        return None

def send_danmaku(room_id, msg):
    """发送弹幕"""
    cookies, csrf_token, _ = load_fresh_auth()
    payload = {
        'msg': msg,
        'color': '14893055',
        'fontsize': '25',
        'rnd': str(round(time.time())),
        'roomid': str(room_id),
        'csrf': csrf_token,
        'csrf_token': csrf_token,
    }
    response = requests.post('https://api.live.bilibili.com/msg/send', cookies=cookies, headers=HEADERS, data=payload)
    return response

def send_like(room_id, click_times, anchor_id, img_key, sub_key):
    """自动点赞"""
    cookies, csrf_token, uid = load_fresh_auth()
    payload = {
        'uid': uid,
        'click_time': str(click_times), 
        'room_id': str(room_id),
        'anchor_id': anchor_id,
        'web_location': '444.8',
        'csrf': csrf_token
    }
    signed_payload = generate_wbi_signature(payload, img_key, sub_key)
    url = 'https://api.live.bilibili.com/xlive/app-ucenter/v1/like_info_v3/like/likeReportV3'
    response = requests.post(url, headers=HEADERS, params=signed_payload, cookies=cookies)
    print(f"[{time.strftime('%H:%M:%S')}] 房间 {room_id} 点赞发送结果: {response.status_code}")
    return response

# ==========================================
# 4. 主控战场 (Main Loop)
# ==========================================
if __name__ == '__main__':
    # 获取wbi秘钥
    IMG_KEY, SUB_KEY = get_wbi_keys()
    target_room = "1926784908" 
    target_uid = get_anchor_id(target_room)
    target_name = get_anchor_name(target_room)
    print(f">>> 房间 {target_room} 的主播 UID 为 {target_uid}")
    print(f">>> 房间 {target_room} 的主播昵称为 {target_name}")
    # for i in range(50):
    #     send_lick_respone = send_like(room_id=target_room, click_times=20, anchor_id=target_uid, img_key=IMG_KEY, sub_key=SUB_KEY)
    #     if send_lick_respone.json()['code'] == 0:
    #         print(f"第{i+1}次循环完成")
    #     else:
    #         print(f"第{i+1}次循环出错")
    #         break
    #     time.sleep(5)
