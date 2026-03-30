import sys
import os
import traceback
import time
import json
import qrcode
import webbrowser
import requests
from typing import Literal
from PIL import ImageQt
from PySide6.QtWidgets import QWidget, QApplication, QDialog, QTableWidgetItem, QFileDialog, QHeaderView
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QObject, QTimer, Slot, QRunnable, QThreadPool, Signal, Qt, QDateTime
from ui_codes.console import Ui_MainWindow
from ui_codes.qr_window import Ui_qr_dialog
from bilibili_login import get_qrcode, poll_if_scan, check_cookie_valid, get_executable_dir
from bilibili_bot import get_anchor_name, get_anchor_id, send_danmaku, send_like, get_wbi_keys
from task_config import TaskConfigError, load_task_list, normalize_task_list

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def format_exception_for_log(error: Exception) -> str:
    if isinstance(error, requests.Timeout):
        return "网络请求超时，请检查网络连接后重试"
    if isinstance(error, requests.ConnectionError):
        return "网络连接失败，请检查网络后重试"
    if isinstance(error, requests.HTTPError):
        return f"B站接口访问失败：{error}"
    return str(error)

class MySignal(QObject):
    error = Signal(tuple)
    result = Signal(object)
    log = Signal(str)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.signals = MySignal()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
    
    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc())) 
        else:
            self.signals.result.emit(result)           

class MainConsole(QWidget):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.table_tasks.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        icon_path = resource_path("robot.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.ui.label_login_status.setText("正在初始化系统...")
        self.ui.label_login_status.setStyleSheet("color: gray;")
        
        self.ui.btn_start_send.setEnabled(False)
        self.ui.btn_like.setEnabled(False)
        self.ui.btn_schedule_send.setEnabled(False)
        self.ui.btn_get_qr.setEnabled(False) 
        
        worker_check_login = Worker(check_cookie_valid)
        worker_check_login.signals.result.connect(self.on_login_checked)
        self.threadpool.start(worker_check_login)

        self.task_list = []
        self.is_sending = False
        self.is_liking = False
        self.is_timing = False
        self.target_datetime = None

        self.timer_send = QTimer(self)

        self.style_pink_default = self.ui.btn_start_send.styleSheet()
        self.style_red_danger = """
            QPushButton {
                background-color: #ff4d4f; 
                color: white; 
                font-weight: bold; 
                font-size: 16px; 
                border-radius: 8px; 
                padding: 10px; 
                border: none; 
            }
            QPushButton:hover {
                background-color: #ff7875; 
            }
            QPushButton:pressed {
                background-color: #d9363e; 
            }
        """

        self.bind_signals()

        default_config_path = os.path.join(get_executable_dir(), "bilibili_tasks.json")
        if os.path.exists(default_config_path):
            try:
                imported_data = load_task_list(default_config_path)
                if imported_data:
                    self.task_list = imported_data
                    self._refresh_table_ui()
            except TaskConfigError as e:
                self.print_log(f"默认任务配置加载失败：{e}")
            except Exception as e:
                self.print_log(f"默认任务配置加载失败：{format_exception_for_log(e)}")

    def bind_signals(self):
        self.ui.btn_get_qr.clicked.connect(self.start_fetch_qrcode)
        self.ui.btn_add_task.clicked.connect(self.start_add_task)
        self.ui.btn_edit_task.clicked.connect(self.slot_edit_task)
        self.ui.btn_delete_task.clicked.connect(self.slot_delete_task)
        self.ui.btn_clear_task.clicked.connect(self.slot_clear_task)
        self.ui.btn_save_config.clicked.connect(self.slot_save_config)
        self.ui.btn_load_config.clicked.connect(self.slot_load_config)
        self.ui.btn_start_send.clicked.connect(self.toggle_send_danmaku)
        self.ui.btn_like.clicked.connect(self.toggle_send_like)
        self.ui.btn_schedule_send.clicked.connect(self.slot_toggle_timing)
        self.ui.btn_enter_room.clicked.connect(self.slot_enter_room)
        self.ui.btn_clear_log.clicked.connect(self.slot_clear_log)
        self.ui.btn_export_log.clicked.connect(self.slot_export_log)
        self.ui.table_tasks.itemSelectionChanged.connect(self.slot_table_clicked)
        self.timer_send.timeout.connect(self.check_timing_tick)

    def print_log(self, message: str):
        """插入日志"""
        current_time = time.strftime('%H:%M:%S')
        self.ui.text_log.append(f"[{current_time}] {message}")

        scrollbar = self.ui.text_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    @Slot()
    def on_login_checked(self, is_valid: bool):
        self.ui.btn_get_qr.setEnabled(True) # 恢复扫码按钮

        if is_valid:
            self.ui.label_login_status.setText("已登录")
            self.ui.label_login_status.setStyleSheet("color: green;")
            
            self.ui.btn_start_send.setEnabled(True)
            self.ui.btn_like.setEnabled(True)
            self.ui.btn_schedule_send.setEnabled(True)
            
        else:
            self.ui.label_login_status.setText("未登录或网络异常")
            self.ui.label_login_status.setStyleSheet("color: red;")
            self.ui.btn_start_send.setEnabled(False)
            self.ui.btn_like.setEnabled(False)
            self.ui.btn_schedule_send.setEnabled(False)
            self.print_log("无法验证登录凭证，请检查网络或重新扫码")

    def _make_item(self, text: str) -> QTableWidgetItem:
            """自动转换字符串并居中"""
            item = QTableWidgetItem(str(text))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            return item

    def _refresh_table_ui(self):
        self.ui.table_tasks.setRowCount(0)
        for row_index, task in enumerate(self.task_list):
            self.ui.table_tasks.insertRow(row_index)
            
            self.ui.table_tasks.setItem(row_index, 0, self._make_item(task.get("uname")))
            self.ui.table_tasks.setItem(row_index, 1, self._make_item(str(task.get("msg"))))
            self.ui.table_tasks.setItem(row_index, 2, self._make_item(str(task.get("loop"))))
            self.ui.table_tasks.setItem(row_index, 3, self._make_item(str(task.get("send_interval"))))

    def _send_danmaku_circ(self, task_list: list, log_signal: Signal):
        if not task_list:
            log_signal.emit("任务队列为空，请先添加任务")
            return

        for task in task_list:
            if not self.is_sending: 
                log_signal.emit("已停止发送弹幕")
                return

            room_id = task["room"]
            uname = task["uname"]
            msg = task["msg"]
            loop_times = task["loop"]
            send_interval = task["send_interval"]
            for i in range(loop_times):
                if not self.is_sending: 
                    log_signal.emit(f"已停止发送弹幕")
                    return

                try:
                    send_danmaku(room_id, msg)
                    log_signal.emit(f"已完成第 {i+1}/{loop_times} 个向主播 {uname} 发送的 {msg} 弹幕")
                except Exception as e:
                    log_signal.emit(f"向主播 {uname} 发送弹幕失败：{e}")
                    raise e

                for _ in range(10*send_interval):
                    if not self.is_sending:
                        log_signal.emit("已停止发送弹幕")
                        return

                    time.sleep(0.1)
            log_signal.emit(f"向主播 {uname} 的 {msg} 弹幕已全部发送完毕")
        log_signal.emit(f"所有任务队列已执行完毕")
        return

    def _send_like_circ(self, room_id: str, uname: str, log_signal: Signal):
        try:
            IMG_KEY, SUB_KEY = get_wbi_keys()
            anchor_id = get_anchor_id(room_id)
            if not anchor_id:
                raise RuntimeError("未能获取主播 UID，请检查房间号或网络")
        except Exception as e:
            self.is_liking = False
            log_signal.emit(f"点赞准备失败: {e}")
            return
        
        log_signal.emit(f"开始向主播 {uname} 发送 1000 赞(若已达单日上限，服务器将静默忽略)。")
        for i in range(50):
            if not self.is_liking: 
                log_signal.emit(f"已停止向主播 {uname} 点赞。")
                return
            try:
                send_like(room_id, 20, anchor_id, IMG_KEY, SUB_KEY)
                log_signal.emit(f"向主播 {uname} 的第 {i+1}/50 轮点赞完成")
            except Exception as e:
                log_signal.emit(f"点赞请求发送失败：{e}")
                raise e

            for _ in range(15):
                if not self.is_liking:
                    log_signal.emit(f"已停止向主播 {uname} 点赞。")
                    return

                time.sleep(0.1)
        log_signal.emit(f"主播 {uname} 的点赞任务已完成，已到达今日的单场点赞上限")
        return

    @Slot()
    def start_fetch_qrcode(self):
        self.ui.btn_get_qr.setEnabled(False)
        worker_fetch_qrcode = Worker(get_qrcode)
        worker_fetch_qrcode.signals.result.connect(self.on_qrcode_fetched)
        worker_fetch_qrcode.signals.error.connect(self.on_qr_error)
        self.threadpool.start(worker_fetch_qrcode)
    
    @Slot()
    def on_qrcode_fetched(self, package: tuple[str, str]) -> None:
        qrcode_key, qrcode_url = package
        qrcode_qimg = ImageQt.ImageQt(qrcode.make(qrcode_url))
        qrcode_qpixmap = QPixmap(qrcode_qimg)
        qr_dialog = QRDialog(qrcode_key, qrcode_qpixmap)
        qr_dialog.timer.start(2000)

        was_logged_in = self.ui.btn_start_send.isEnabled()

        result = qr_dialog.exec()

        if result:
            self.on_login_checked(True)
            self.print_log("登录成功") 
        else:
            if was_logged_in:
                self.print_log("登录失败，原登录凭证依旧有效，已自动恢复")
            else:
                self.print_log("登录失败，请重新扫码登录")
        self.ui.btn_get_qr.setEnabled(True)

    @Slot()
    def on_qr_error(self, error_tuple):
        _, value, _ = error_tuple
        self.print_log(f"获取登录二维码失败，请检查网络连接: {format_exception_for_log(value)}")
        self.ui.btn_get_qr.setEnabled(True)

    @Slot()
    def start_add_task(self):
        room_id = self.ui.input_room_id.text().strip()
        danmaku_msg = self.ui.input_danmaku_text.toPlainText().strip()
        if not room_id or not danmaku_msg:
            self.print_log("房号和弹幕内容均不能为空")
            return
        loop_times = self.ui.spin_loop_count.value()
        send_interval = self.ui.spin_interval.value()
        new_task = {"room": room_id, "msg": danmaku_msg, "loop": loop_times, "send_interval": send_interval}
        worker_fetch_anchor_name = Worker(lambda: (get_anchor_name(room_id), new_task, "add", -1))
        worker_fetch_anchor_name.signals.result.connect(self.on_uname_fetched)
        self.threadpool.start(worker_fetch_anchor_name)

    @Slot()
    def on_uname_fetched(self, result: tuple[str, dict, Literal["add", "edit"], int]):
        anchor_name, new_task, action, selected_row = result
        if not anchor_name or "Error" in anchor_name: 
            self.print_log("未能获取主播昵称，无法添加/修改任务，请检查房号或网络")
            return
        if action == "add":
            new_task["uname"] = anchor_name
            self.task_list.append(new_task)

            current_row_count = self.ui.table_tasks.rowCount()
            self.ui.table_tasks.insertRow(current_row_count)

            self.ui.table_tasks.setItem(current_row_count, 0, self._make_item(anchor_name))
            self.ui.table_tasks.setItem(current_row_count, 1, self._make_item(new_task.get("msg")))
            self.ui.table_tasks.setItem(current_row_count, 2, self._make_item(new_task.get("loop")))
            self.ui.table_tasks.setItem(current_row_count, 3, self._make_item(new_task.get("send_interval")))
        
        elif action == "edit":
            if selected_row < 0 or selected_row >= len(self.task_list):
                return
            new_task["uname"] = anchor_name
            self.task_list[selected_row] = new_task
            self.ui.table_tasks.setItem(selected_row, 0, self._make_item(anchor_name))
            self.ui.table_tasks.setItem(selected_row, 1, self._make_item(new_task.get("msg")))
            self.ui.table_tasks.setItem(selected_row, 2, self._make_item(new_task.get("loop")))
            self.ui.table_tasks.setItem(selected_row, 3, self._make_item(new_task.get("send_interval")))

    @Slot()
    def slot_edit_task(self):
        selected_row = self.ui.table_tasks.currentRow()
        if selected_row < 0 or not self.ui.table_tasks.selectedItems():
            self.print_log("请先在右侧表格选中需要修改的任务")
            return
        old_room_id = self.task_list[selected_row].get("room")
        old_uname = self.task_list[selected_row].get("uname")
        new_room_id = self.ui.input_room_id.text().strip()
        new_danmaku_msg = self.ui.input_danmaku_text.toPlainText().strip()
        if not new_room_id or not new_danmaku_msg:
            self.print_log("房号和弹幕内容均不能为空")
            return
        new_loop_times = self.ui.spin_loop_count.value()
        new_send_interval = self.ui.spin_interval.value()
        new_task = {"room": new_room_id, "uname": old_uname, "msg": new_danmaku_msg, "loop": new_loop_times, "send_interval": new_send_interval}

        if old_room_id != new_room_id:
            worker_fetch_anchor_name = Worker(lambda: (get_anchor_name(new_room_id), new_task, "edit", selected_row))
            worker_fetch_anchor_name.signals.result.connect(self.on_uname_fetched)
            self.threadpool.start(worker_fetch_anchor_name)
            return

        self.task_list[selected_row] = new_task
        self.ui.table_tasks.setItem(selected_row, 1, self._make_item(new_task.get("msg")))
        self.ui.table_tasks.setItem(selected_row, 2, self._make_item(new_task.get("loop")))
        self.ui.table_tasks.setItem(selected_row, 3, self._make_item(new_task.get("send_interval")))
            
    @Slot()
    def slot_delete_task(self):
        selected_row = self.ui.table_tasks.currentRow()
        if selected_row < 0 or not self.ui.table_tasks.selectedItems(): return
        del self.task_list[selected_row]
        self.ui.table_tasks.removeRow(selected_row)

    @Slot()
    def slot_clear_task(self):
        self.task_list.clear()
        self.ui.table_tasks.setRowCount(0)

    @Slot()
    def slot_save_config(self):
        if not self.task_list:
            self.print_log("任务队列为空")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "保存当前配置", 
            "bilibili_tasks.json", 
            "JSON 文件 (*.json);;所有文件 (*)"
        )

        if file_path:
            try:
                normalized_task_list = normalize_task_list(self.task_list)
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(normalized_task_list, f, ensure_ascii=False, indent=4)
                self.print_log(f"任务配置已成功保存至：{file_path}")
            except TaskConfigError as e:
                self.print_log(f"保存配置失败：{e}")
            except Exception as e:
                self.print_log(f"保存配置失败：{format_exception_for_log(e)}")

    @Slot()
    def slot_load_config(self):
        """读取本地 JSON，并强制覆盖当前任务队列"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "导入配置", 
            "", 
            "JSON 文件 (*.json);;所有文件 (*)"
        )
        
        if file_path:
            try:
                imported_data = load_task_list(file_path)
                self.task_list = imported_data
                self._refresh_table_ui() 
                self.print_log(f"成功导入配置：{file_path}")
            except TaskConfigError as e:
                self.print_log(f"导入配置失败：{e}")
            except Exception as e:
                self.print_log(f"导入配置失败：{format_exception_for_log(e)}")

    @Slot()
    def slot_table_clicked(self):
        current_row = self.ui.table_tasks.currentRow()
        if current_row >= 0:
            current_task = self.task_list[current_row]
            self.ui.input_room_id.setText(current_task["room"])
            self.ui.input_danmaku_text.setPlainText(current_task["msg"])
            self.ui.spin_loop_count.setValue(current_task["loop"])
            self.ui.spin_interval.setValue(current_task["send_interval"])            

    @Slot()
    def toggle_send_danmaku(self):
        if not self.is_sending:
            if not self.task_list:
                self.print_log("任务队列为空，请先添加任务")
                return
            self.is_sending = True

            self.ui.btn_start_send.setText("⏹️停止发送")
            self.ui.btn_start_send.setStyleSheet(self.style_red_danger)

            self.ui.btn_add_task.setEnabled(False)
            self.ui.btn_edit_task.setEnabled(False)
            self.ui.btn_delete_task.setEnabled(False)
            self.ui.btn_clear_task.setEnabled(False)
            self.ui.btn_schedule_send.setEnabled(False)
            self.ui.time_schedule.setEnabled(False)

            worker_send_danmaku = Worker(self._send_danmaku_circ, self.task_list)
            worker_send_danmaku.kwargs["log_signal"] = worker_send_danmaku.signals.log
            worker_send_danmaku.signals.result.connect(self.on_danmaku_finished)
            worker_send_danmaku.signals.log.connect(self.print_log)
            worker_send_danmaku.signals.error.connect(self.on_danmaku_error)
            self.threadpool.start(worker_send_danmaku)
        else:
            self.is_sending = False
            self.ui.btn_start_send.setEnabled(False)
    
    @Slot()
    def on_danmaku_finished(self, _):
        self.is_sending = False

        self.ui.btn_start_send.setText("🚀一键发送")
        self.ui.btn_start_send.setStyleSheet(self.style_pink_default)
        self.ui.btn_start_send.setEnabled(True)
        
        self.ui.btn_add_task.setEnabled(True)
        self.ui.btn_edit_task.setEnabled(True)
        self.ui.btn_delete_task.setEnabled(True)
        self.ui.btn_clear_task.setEnabled(True)
        self.ui.btn_schedule_send.setEnabled(True)
        self.ui.time_schedule.setEnabled(True)        

    @Slot()
    def on_danmaku_error(self, error_tuple):
        _, value, _ = error_tuple
        self.print_log(f"弹幕发送失败：{format_exception_for_log(value)}")

        self.is_sending = False

        self.ui.btn_start_send.setText("🚀一键发送")
        self.ui.btn_start_send.setStyleSheet(self.style_pink_default)
        self.ui.btn_start_send.setEnabled(True)
        
        self.ui.btn_add_task.setEnabled(True)
        self.ui.btn_edit_task.setEnabled(True)
        self.ui.btn_delete_task.setEnabled(True)
        self.ui.btn_clear_task.setEnabled(True)
        self.ui.btn_schedule_send.setEnabled(True)
        self.ui.time_schedule.setEnabled(True)  

    @Slot()
    def slot_toggle_timing(self):
        """按下'定时发送'按钮时触发"""
        if not self.is_timing:
            if not self.task_list:
                self.print_log("任务队列为空，请先添加任务后再设置定时")
                return
            target_qtime = self.ui.time_schedule.dateTime() 
            current_qtime = QDateTime.currentDateTime()

            if target_qtime <= current_qtime:
                self.print_log("定时时间必须晚于当前真实时间")
                return
                
            self.is_timing = True
            self.target_datetime = target_qtime
            
            self.ui.btn_schedule_send.setText("❎取消定时")
            self.ui.btn_start_send.setEnabled(False)
            self.ui.time_schedule.setEnabled(False) 
            
            self.print_log(f"计时器已启动，任务队列将在 {target_qtime.toString('yyyy-MM-dd HH:mm:ss')} 时执行, 定时期间一键发送将被禁用，若要启用请先取消定时")
            self.timer_send.start(1000) 
            
        else:
            self.is_timing = False
            self.timer_send.stop()
            self.target_datetime = None

            self.ui.btn_schedule_send.setText("⏰️定时发送")
            self.ui.btn_schedule_send.setEnabled(True)
            self.ui.btn_start_send.setEnabled(True)
            self.ui.time_schedule.setEnabled(True)
            self.print_log("定时任务已手动关闭")

    @Slot()
    def check_timing_tick(self):
        """检查是否到达设定时间"""
        if self.target_datetime is None:
            return
        if QDateTime.currentDateTime() >= self.target_datetime:

            self.timer_send.stop() 
            self.is_timing = False
            self.target_datetime = None
            
            self.ui.btn_schedule_send.setText("⏰️定时发送")
            self.ui.time_schedule.setEnabled(True)
            self.ui.btn_start_send.setEnabled(True)
            
            self.print_log("已达到设定时间，任务队列将执行")
            self.toggle_send_danmaku()

    @Slot()
    def toggle_send_like(self):
        if not self.is_liking:
            selected_row = self.ui.table_tasks.currentRow()
            if selected_row < 0 or not self.ui.table_tasks.selectedItems():
                self.print_log("请先在右侧表格选中要点赞的目标房间")
                return
            
            self.is_liking = True

            self.ui.btn_like.setText("⏹️停止点赞")

            room_id = self.task_list[selected_row]["room"]
            uname = self.task_list[selected_row]["uname"]

            worker_send_like = Worker(self._send_like_circ, room_id, uname)
            worker_send_like.kwargs["log_signal"] = worker_send_like.signals.log
            worker_send_like.signals.result.connect(self.on_like_finished)
            worker_send_like.signals.error.connect(self.on_like_error)
            worker_send_like.signals.log.connect(self.print_log)
            self.threadpool.start(worker_send_like)
        else:
            self.is_liking = False
            self.ui.btn_like.setEnabled(False)

    @Slot()
    def on_like_finished(self, result=None):
        self.is_liking = False

        self.ui.btn_like.setText("❤️一键点赞")
        self.ui.btn_like.setEnabled(True)

    @Slot()
    def on_like_error(self, error_tuple):
        _, value, _ = error_tuple
        self.print_log(f"点赞任务发生异常：{format_exception_for_log(value)}")

        self.is_liking = False
        self.ui.btn_like.setText("❤️一键点赞")
        self.ui.btn_like.setEnabled(True)

    @Slot()
    def slot_enter_room(self):
        selected_row = self.ui.table_tasks.currentRow()
        if selected_row < 0 or not self.ui.table_tasks.selectedItems():
            self.print_log("请先在右侧表格选中要进入的目标房间")
            return
        room_id = self.task_list[selected_row]["room"]
        uname = self.task_list[selected_row]["uname"]
        url = f"https://live.bilibili.com/{room_id}"
        self.print_log(f"已打开默认浏览器，进入 {uname} 的直播间 ")
        try:
            webbrowser.open(url)
        except Exception:
            self.print_log(f"打开浏览器失败，请手动复制网址: {url}")

    @Slot()
    def slot_clear_log(self):
        self.ui.text_log.clear()

    @Slot()
    def slot_export_log(self):
        """将日志导出为本地 txt 文件"""
        log_content = self.ui.text_log.toPlainText()
        if not log_content:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "选择保存位置", 
            "bilibili_live_log.txt", 
            "文本文件 (*.txt);;所有文件 (*)"
        )

        if file_path: 
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(log_content)
                self.print_log(f"日志已导出至硬盘：{file_path}")
            except Exception as e:
                self.print_log(f"日志导出失败：{format_exception_for_log(e)}")

    def closeEvent(self, event):
        self.is_sending = False
        self.is_liking = False
        self.is_timing = False
        self.timer_send.stop()
        return super().closeEvent(event)

class QRDialog(QDialog):
    def __init__(self, qrcode_key: str, qrcode_qpixmap: QPixmap):
        super().__init__()
        self.ui = Ui_qr_dialog()
        self.ui.setupUi(self)
        
        self.timer = QTimer(self)
        self.threadpool = QThreadPool()
        
        self.qrcode_key = qrcode_key
        self.qrcode_qpixmap = qrcode_qpixmap
        self.poll_in_flight = False
        self.is_closing = False
        
        self._embed_qrcode()
        
        self.timer.timeout.connect(self.start_poll_if_scan)

    def _embed_qrcode(self):
        self.ui.label_qr_image.setScaledContents(True)
        self.ui.label_qr_image.setPixmap(self.qrcode_qpixmap)        

    @Slot()
    def start_poll_if_scan(self):
        if self.poll_in_flight:
            return
        self.poll_in_flight = True
        worker_poll_if_scan = Worker(poll_if_scan, self.qrcode_key)
        worker_poll_if_scan.signals.result.connect(self.on_poll_finished)
        worker_poll_if_scan.signals.error.connect(self.on_poll_error)
        self.threadpool.start(worker_poll_if_scan)

    @Slot()
    def on_poll_finished(self, poll_response: Literal["Success", "Waiting", "Confirming", "Timeout"]):
        self.poll_in_flight = False
        if self.is_closing:
            return
        if poll_response == "Success":
            self.timer.stop()
            self.accept()
        elif poll_response == "Confirming":
            self.ui.label_qr_tips.setText("已扫码，请在手机上确认")
        elif poll_response == "Timeout":
            self.timer.stop()
            self.reject()  

    @Slot()
    def on_poll_error(self, _):
        self.poll_in_flight = False
        if self.is_closing:
            return
        self.timer.stop()
        self.ui.label_qr_tips.setText("验证失败，请关闭重试")
        self.ui.label_qr_tips.setStyleSheet("color: red;")

    def closeEvent(self, arg__1):
        self.is_closing = True
        self.timer.stop()
        return super().closeEvent(arg__1)     

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainconsole = MainConsole()
    mainconsole.show()
    sys.exit(app.exec())


