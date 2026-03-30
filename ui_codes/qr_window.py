# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qr_window.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_qr_dialog(object):
    def setupUi(self, qr_dialog):
        if not qr_dialog.objectName():
            qr_dialog.setObjectName(u"qr_dialog")
        qr_dialog.resize(268, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(qr_dialog.sizePolicy().hasHeightForWidth())
        qr_dialog.setSizePolicy(sizePolicy)
        qr_dialog.setMinimumSize(QSize(250, 300))
        qr_dialog.setMaximumSize(QSize(268, 300))
        self.verticalLayout = QVBoxLayout(qr_dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_qr_image = QLabel(qr_dialog)
        self.label_qr_image.setObjectName(u"label_qr_image")
        self.label_qr_image.setMinimumSize(QSize(250, 250))
        self.label_qr_image.setMaximumSize(QSize(250, 250))
        self.label_qr_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_qr_image)

        self.label_qr_tips = QLabel(qr_dialog)
        self.label_qr_tips.setObjectName(u"label_qr_tips")
        self.label_qr_tips.setTextFormat(Qt.TextFormat.AutoText)
        self.label_qr_tips.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_qr_tips)


        self.retranslateUi(qr_dialog)

        QMetaObject.connectSlotsByName(qr_dialog)
    # setupUi

    def retranslateUi(self, qr_dialog):
        qr_dialog.setWindowTitle(QCoreApplication.translate("qr_dialog", u"\u8bf7\u626b\u63cf\u4e8c\u7ef4\u7801", None))
        self.label_qr_image.setText("")
        self.label_qr_tips.setText(QCoreApplication.translate("qr_dialog", u"\u8bf7\u4f7f\u7528bilibili App\u626b\u7801", None))
    # retranslateUi

