# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoginWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, CheckBox, HyperlinkButton, LineEdit,
    PrimaryPushButton)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(900, 500)
        Form.setMinimumSize(QSize(900, 500))
        Form.setMaximumSize(QSize(900, 500))
        icon = QIcon()
        icon.addFile(u":/logo.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        Form.setWindowIcon(icon)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.background = QLabel(Form)
        self.background.setObjectName(u"background")
        self.background.setPixmap(QPixmap(u":/bg.png"))
        self.background.setScaledContents(True)

        self.horizontalLayout.addWidget(self.background)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(360, 0))
        self.widget.setMaximumSize(QSize(360, 16777215))
        self.widget.setStyleSheet(u"QLabel{\n"
"	font: 13px 'Microsoft YaHei'\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(9)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 20)
        self.verticalSpacer_1 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_1)

        self.logo = QLabel(self.widget)
        self.logo.setObjectName(u"logo")
        self.logo.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy1)
        self.logo.setMinimumSize(QSize(122, 100))
        self.logo.setMaximumSize(QSize(100, 100))
        self.logo.setPixmap(QPixmap(u":/logo.png"))
        self.logo.setScaledContents(True)

        self.verticalLayout_2.addWidget(self.logo, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_2 = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.label_username = BodyLabel(self.widget)
        self.label_username.setObjectName(u"label_username")

        self.verticalLayout_2.addWidget(self.label_username)

        self.input_username = LineEdit(self.widget)
        self.input_username.setObjectName(u"input_username")
        self.input_username.setClearButtonEnabled(True)

        self.verticalLayout_2.addWidget(self.input_username)

        self.label_password = BodyLabel(self.widget)
        self.label_password.setObjectName(u"label_password")

        self.verticalLayout_2.addWidget(self.label_password)

        self.input_password = LineEdit(self.widget)
        self.input_password.setObjectName(u"input_password")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setClearButtonEnabled(True)

        self.verticalLayout_2.addWidget(self.input_password)

        self.verticalSpacer_3 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.checkbox_autologin = CheckBox(self.widget)
        self.checkbox_autologin.setObjectName(u"checkbox_autologin")
        self.checkbox_autologin.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkbox_autologin)

        self.verticalSpacer_4 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.button_login = PrimaryPushButton(self.widget)
        self.button_login.setObjectName(u"button_login")

        self.verticalLayout_2.addWidget(self.button_login)

        self.verticalSpacer_5 = QSpacerItem(20, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_5)

        self.button_logout = HyperlinkButton(self.widget)
        self.button_logout.setObjectName(u"button_logout")

        self.verticalLayout_2.addWidget(self.button_logout)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_6)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u7f51\u7edc\u8ba4\u8bc1", None))
        self.background.setText("")
        self.logo.setText("")
        self.label_username.setText(QCoreApplication.translate("Form", u"\u7528\u6237\u540d", None))
        self.input_username.setPlaceholderText("")
        self.label_password.setText(QCoreApplication.translate("Form", u"\u5bc6\u7801", None))
        self.input_password.setPlaceholderText("")
        self.checkbox_autologin.setText(QCoreApplication.translate("Form", u"\u81ea\u52a8\u767b\u5f55", None))
        self.button_login.setText(QCoreApplication.translate("Form", u"\u767b\u5f55", None))
        self.button_logout.setText(QCoreApplication.translate("Form", u"\u4e0b\u7ebf", None))
    # retranslateUi

