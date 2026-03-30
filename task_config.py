from __future__ import annotations

import json
from typing import Any


class TaskConfigError(ValueError):
    pass


def _task_label(index: int) -> str:
    return f"第 {index + 1} 条任务"


def _ensure_non_empty_text(value: Any, *, field_name: str, index: int) -> str:
    if not isinstance(value, str):
        raise TaskConfigError(f"{_task_label(index)}的{field_name}必须是字符串")
    normalized = value.strip()
    if not normalized:
        raise TaskConfigError(f"{_task_label(index)}的{field_name}不能为空")
    return normalized


def _ensure_room_id(value: Any, *, index: int) -> str:
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    return _ensure_non_empty_text(value, field_name="房间号", index=index)


def _ensure_optional_text(value: Any, *, field_name: str, index: int, default: str) -> str:
    if value is None:
        return default
    if not isinstance(value, str):
        raise TaskConfigError(f"{_task_label(index)}的{field_name}必须是字符串")
    normalized = value.strip()
    return normalized or default


def _ensure_int(value: Any, *, field_name: str, index: int, minimum: int) -> int:
    if isinstance(value, bool):
        raise TaskConfigError(f"{_task_label(index)}的{field_name}必须是整数")

    normalized = value
    if isinstance(value, str):
        normalized = value.strip()
        if not normalized:
            raise TaskConfigError(f"{_task_label(index)}的{field_name}不能为空")
        try:
            normalized = int(normalized)
        except ValueError as exc:
            raise TaskConfigError(f"{_task_label(index)}的{field_name}必须是整数") from exc

    if not isinstance(normalized, int):
        raise TaskConfigError(f"{_task_label(index)}的{field_name}必须是整数")
    if normalized < minimum:
        raise TaskConfigError(f"{_task_label(index)}的{field_name}不能小于 {minimum}")
    return normalized


def normalize_task(task: Any, index: int) -> dict[str, Any]:
    if not isinstance(task, dict):
        raise TaskConfigError(f"{_task_label(index)}必须是 JSON 对象")

    room = _ensure_room_id(task.get("room"), index=index)
    message = _ensure_non_empty_text(task.get("msg"), field_name="弹幕内容", index=index)
    loop = _ensure_int(task.get("loop"), field_name="循环次数", index=index, minimum=1)
    send_interval = _ensure_int(task.get("send_interval"), field_name="发送间隔", index=index, minimum=5)
    uname = _ensure_optional_text(task.get("uname"), field_name="主播昵称", index=index, default=f"房间 {room}")

    return {
        "room": room,
        "uname": uname,
        "msg": message,
        "loop": loop,
        "send_interval": send_interval,
    }


def normalize_task_list(task_list: Any) -> list[dict[str, Any]]:
    if not isinstance(task_list, list):
        raise TaskConfigError("任务配置必须是 JSON 数组")
    return [normalize_task(task, index) for index, task in enumerate(task_list)]


def load_task_list(file_path: str) -> list[dict[str, Any]]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise TaskConfigError(f"JSON 解析失败：第 {exc.lineno} 行第 {exc.colno} 列附近格式不正确") from exc
    return normalize_task_list(data)
