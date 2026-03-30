from __future__ import annotations


ERROR_CODE_MESSAGES = {
    -101: "登录状态已失效，请重新扫码登录",
    -111: "请求校验失败，请重新登录后再试",
    -400: "请求参数不合法",
    -401: "当前账号未登录或认证失效",
    -403: "当前账号没有权限执行此操作",
    -404: "目标资源不存在",
    -412: "请求被风控拦截，请稍后重试",
    86038: "二维码已过期，请重新获取",
    86090: "已扫码，请在手机上确认授权",
    86101: "等待扫码中",
}


def format_bilibili_error(code: object, raw_message: str | None = None) -> str:
    known_message = ERROR_CODE_MESSAGES.get(code)
    cleaned_raw = (raw_message or "").strip()

    if known_message and cleaned_raw and cleaned_raw not in {known_message, "0", "success", "成功"}:
        return f"{known_message}（错误码 {code}，原始信息：{cleaned_raw}）"
    if known_message:
        return f"{known_message}（错误码 {code}）"
    if cleaned_raw:
        return f"B站接口返回错误（错误码 {code}，原始信息：{cleaned_raw}）"
    return f"B站接口返回错误（错误码 {code}）"
