# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'console.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDateTimeEdit, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTableWidget, QTableWidgetItem, QTextBrowser,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(691, 756)
        MainWindow.setStyleSheet(u"")
        self.verticalLayout_4 = QVBoxLayout(MainWindow)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(MainWindow)
        self.label.setObjectName(u"label")
        self.label.setEnabled(True)
        font = QFont()
        font.setPointSize(9)
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.label_login_status = QLabel(MainWindow)
        self.label_login_status.setObjectName(u"label_login_status")

        self.horizontalLayout.addWidget(self.label_login_status)

        self.btn_get_qr = QPushButton(MainWindow)
        self.btn_get_qr.setObjectName(u"btn_get_qr")
        self.btn_get_qr.setFont(font)

        self.horizontalLayout.addWidget(self.btn_get_qr)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.groupBox = QGroupBox(MainWindow)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.input_room_id = QLineEdit(self.groupBox)
        self.input_room_id.setObjectName(u"input_room_id")

        self.gridLayout.addWidget(self.input_room_id, 0, 1, 1, 1)

        self.input_danmaku_text = QTextEdit(self.groupBox)
        self.input_danmaku_text.setObjectName(u"input_danmaku_text")

        self.gridLayout.addWidget(self.input_danmaku_text, 1, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.spin_loop_count = QSpinBox(self.groupBox)
        self.spin_loop_count.setObjectName(u"spin_loop_count")
        self.spin_loop_count.setMinimum(1)
        self.spin_loop_count.setMaximum(999)

        self.gridLayout.addWidget(self.spin_loop_count, 2, 1, 1, 1)

        self.spin_interval = QSpinBox(self.groupBox)
        self.spin_interval.setObjectName(u"spin_interval")
        self.spin_interval.setMinimum(5)
        self.spin_interval.setMaximum(9999)

        self.gridLayout.addWidget(self.spin_interval, 3, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.btn_add_task = QPushButton(self.groupBox)
        self.btn_add_task.setObjectName(u"btn_add_task")

        self.horizontalLayout_2.addWidget(self.btn_add_task)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.btn_edit_task = QPushButton(self.groupBox)
        self.btn_edit_task.setObjectName(u"btn_edit_task")

        self.horizontalLayout_2.addWidget(self.btn_edit_task)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_4.addWidget(self.groupBox)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_4)

        self.groupBox_2 = QGroupBox(MainWindow)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.table_tasks = QTableWidget(self.groupBox_2)
        if (self.table_tasks.columnCount() < 4):
            self.table_tasks.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_tasks.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_tasks.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_tasks.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_tasks.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.table_tasks.setObjectName(u"table_tasks")
        self.table_tasks.setMaximumSize(QSize(16777215, 16777215))
        self.table_tasks.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.verticalLayout_2.addWidget(self.table_tasks)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.btn_delete_task = QPushButton(self.groupBox_2)
        self.btn_delete_task.setObjectName(u"btn_delete_task")

        self.horizontalLayout_3.addWidget(self.btn_delete_task)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_7)

        self.btn_clear_task = QPushButton(self.groupBox_2)
        self.btn_clear_task.setObjectName(u"btn_clear_task")

        self.horizontalLayout_3.addWidget(self.btn_clear_task)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_8)

        self.btn_save_config = QPushButton(self.groupBox_2)
        self.btn_save_config.setObjectName(u"btn_save_config")

        self.horizontalLayout_3.addWidget(self.btn_save_config)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_9)

        self.btn_load_config = QPushButton(self.groupBox_2)
        self.btn_load_config.setObjectName(u"btn_load_config")

        self.horizontalLayout_3.addWidget(self.btn_load_config)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_10)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_7.addWidget(self.groupBox_2)

        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 2)

        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.groupBox_3 = QGroupBox(MainWindow)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_5.addWidget(self.label_6)

        self.time_schedule = QDateTimeEdit(self.groupBox_3)
        self.time_schedule.setObjectName(u"time_schedule")

        self.horizontalLayout_5.addWidget(self.time_schedule)

        self.btn_schedule_send = QPushButton(self.groupBox_3)
        self.btn_schedule_send.setObjectName(u"btn_schedule_send")

        self.horizontalLayout_5.addWidget(self.btn_schedule_send)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_9)

        self.btn_like = QPushButton(self.groupBox_3)
        self.btn_like.setObjectName(u"btn_like")

        self.horizontalLayout_5.addWidget(self.btn_like)

        self.btn_enter_room = QPushButton(self.groupBox_3)
        self.btn_enter_room.setObjectName(u"btn_enter_room")

        self.horizontalLayout_5.addWidget(self.btn_enter_room)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)


        self.verticalLayout_4.addWidget(self.groupBox_3)

        self.btn_start_send = QPushButton(MainWindow)
        self.btn_start_send.setObjectName(u"btn_start_send")
        self.btn_start_send.setStyleSheet(u"QPushButton {\n"
"    background-color: #FB7299; /* B\u7ad9\u6807\u51c6\u7c89\u8272 */\n"
"    color: white; /* \u7eaf\u767d\u6587\u5b57\uff0c\u4fdd\u8bc1\u9ad8\u5bf9\u6bd4\u5ea6 */\n"
"    font-weight: bold; /* \u5b57\u4f53\u52a0\u7c97 */\n"
"    font-size: 16px; /* \u5b57\u53f7\u52a0\u5927\uff0c\u7a81\u51fa\u4e3b\u70ae\u5730\u4f4d */\n"
"    border-radius: 8px; /* \u5706\u6ed1\u7684\u88c5\u7532\u8fb9\u7f18 */\n"
"    padding: 10px; /* \u589e\u52a0\u5185\u8fb9\u8ddd\uff0c\u8ba9\u6309\u94ae\u770b\u8d77\u6765\u66f4\u4e30\u6ee1 */\n"
"    border: none; /* \u53bb\u9664\u9ed8\u8ba4\u7684\u4e11\u964b\u9ed1\u8fb9 */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #ff85a8; /* \u9f20\u6807\u60ac\u505c\u65f6\u7a0d\u5fae\u53d8\u4eae\uff0c\u589e\u52a0\u4ea4\u4e92\u611f */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #e06085; /* \u6309\u4e0b\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4f53\u73b0\u673a\u68b0\u6309\u538b\u611f */\n"
"}")

        self.verticalLayout_4.addWidget(self.btn_start_send)

        self.groupBox_4 = QGroupBox(MainWindow)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.text_log = QTextBrowser(self.groupBox_4)
        self.text_log.setObjectName(u"text_log")

        self.verticalLayout_3.addWidget(self.text_log)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_11)

        self.btn_clear_log = QPushButton(self.groupBox_4)
        self.btn_clear_log.setObjectName(u"btn_clear_log")

        self.horizontalLayout_10.addWidget(self.btn_clear_log)

        self.btn_export_log = QPushButton(self.groupBox_4)
        self.btn_export_log.setObjectName(u"btn_export_log")

        self.horizontalLayout_10.addWidget(self.btn_export_log)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)


        self.verticalLayout_4.addWidget(self.groupBox_4)


        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"b\u7ad9\u5f39\u5e55\u52a9\u624b", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u767b\u5f55\u72b6\u6001\uff1a", None))
        self.label_login_status.setText(QCoreApplication.translate("MainWindow", u"\u672a\u767b\u5f55\uff08\u8bf7\u626b\u7801\u767b\u5f55\uff09", None))
        self.btn_get_qr.setText(QCoreApplication.translate("MainWindow", u"\u83b7\u53d6\u767b\u5f55\u4e8c\u7ef4\u7801", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u5f39\u5e55\u8bbe\u7f6e", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u5faa\u73af\u6b21\u6570", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u95f4\u9694\uff08\u79d2\uff09", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5f39\u5e55\u5185\u5bb9", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u623f\u95f4\u53f7", None))
        self.btn_add_task.setText(QCoreApplication.translate("MainWindow", u"\u2795\u6dfb\u52a0\u5230\u961f\u5217", None))
        self.btn_edit_task.setText(QCoreApplication.translate("MainWindow", u"\u270f\ufe0f\u4fee\u6539\u9009\u4e2d\u9879", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u4efb\u52a1\u961f\u5217", None))
        ___qtablewidgetitem = self.table_tasks.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u64ad\u6635\u79f0", None))
        ___qtablewidgetitem1 = self.table_tasks.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u5f39\u5e55\u5185\u5bb9", None))
        ___qtablewidgetitem2 = self.table_tasks.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u5faa\u73af\u6b21\u6570", None))
        ___qtablewidgetitem3 = self.table_tasks.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u95f4\u9694\uff08\u79d2\uff09", None))
        self.btn_delete_task.setText(QCoreApplication.translate("MainWindow", u"\u2796\u5220\u9664\u961f\u5217", None))
        self.btn_clear_task.setText(QCoreApplication.translate("MainWindow", u"\U0001f5d1\U0000fe0f\U00006e05\U00007a7a\U0000961f\U00005217", None))
        self.btn_save_config.setText(QCoreApplication.translate("MainWindow", u"\U0001f4be\U00004fdd\U00005b58\U0000914d\U00007f6e", None))
        self.btn_load_config.setText(QCoreApplication.translate("MainWindow", u"\U0001f4c1\U00005bfc\U00005165\U0000914d\U00007f6e", None))
        self.groupBox_3.setTitle("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u7f16\u8f91\u65f6\u95f4", None))
        self.btn_schedule_send.setText(QCoreApplication.translate("MainWindow", u"\u23f0\ufe0f\u5b9a\u65f6\u53d1\u9001", None))
        self.btn_like.setText(QCoreApplication.translate("MainWindow", u"\u2764\ufe0f\u4e00\u952e\u70b9\u8d5e", None))
        self.btn_enter_room.setText(QCoreApplication.translate("MainWindow", u"\U0001f6aa\U00008fdb\U00005165\U000076f4\U000064ad\U000095f4", None))
        self.btn_start_send.setText(QCoreApplication.translate("MainWindow", u"\U0001f680\U00004e00\U0000952e\U000053d1\U00009001", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c\u65e5\u5fd7", None))
        self.btn_clear_log.setText(QCoreApplication.translate("MainWindow", u"\U0001f5d1\U0000fe0f\U00006e05\U00007a7a\U000065e5\U00005fd7", None))
        self.btn_export_log.setText(QCoreApplication.translate("MainWindow", u"\u2b07\ufe0f\u5bfc\u51fa\u65e5\u5fd7", None))
    # retranslateUi

