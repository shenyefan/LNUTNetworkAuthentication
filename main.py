import sys
import requests
import socket
import uuid
import os
import urllib.parse
import configparser
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QThread, Signal, QTimer
from qfluentwidgets import Theme, InfoBar, InfoBarPosition
from qfluentwidgets import setTheme
from LoginWindow import Ui_Form  # 这里直接引用由uic生成的.py文件
import resource_rc  # 导入生成的资源文件

# 获取本机IP地址
def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"获取到的IP地址: {ip_address}")  # 日志输出
    return ip_address

# 获取本机MAC地址
def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                    for elements in range(0, 2*6, 2)][::-1])
    print(f"获取到的MAC地址: {mac}")  # 日志输出
    return mac

# 检查网络连接是否正常
def check_network_status():
    try:
        response = requests.get("https://www.baidu.com/favicon.ico", timeout=3)
        print(f"检查网络连接状态码: {response.status_code}")  # 日志输出
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"检查网络失败: {e}")  # 日志输出
        return False

class NetworkCheckThread(QThread):
    network_status = Signal(bool)

    def run(self):
        status = check_network_status()
        self.network_status.emit(status)

class LoginThread(QThread):
    login_result = Signal(bool, str)

    def __init__(self, url, headers, data):
        super().__init__()
        self.url = url
        self.headers = headers
        self.data = data

    def run(self):
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data)

            if "成功登陆" in response.text:
                self.login_result.emit(True, "登录成功")
            elif "帐号不存在" in response.text:
                self.login_result.emit(False, "帐号不存在")
                print(f"服务器响应内容: {response.text}")  # 日志输出
            elif "密码错误" in response.text:
                self.login_result.emit(False, "密码错误")
                print(f"服务器响应内容: {response.text}")  # 日志输出
            elif "系统错误" in response.text:
                self.login_result.emit(False, "参数错误")
                print(f"服务器响应内容: {response.text}")  # 日志输出
            elif "认证失败" in response.text:
                self.login_result.emit(False, "登录失败")
                print(f"服务器响应内容: {response.text}")  # 日志输出
            else:
                self.login_result.emit(False, "未知错误")
                print(f"服务器响应内容: {response.text}")  # 日志输出

        except Exception as e:
            print(f"请求失败: {e}")  # 日志输出
            self.login_result.emit(False, f"请求失败: {e}")

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.config = configparser.ConfigParser()
        self.config_file = "./config.ini"

        # 常量部分
        self.login_url = "http://10.9.18.71/portalAuthAction.do"
        self.headers = {
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        # 连接信号和槽
        self.ui.button_login.clicked.connect(self.login)
        self.ui.button_logout.clicked.connect(self.logout)

        # 启动网络检查线程
        self.network_thread = NetworkCheckThread()
        self.network_thread.network_status.connect(self.handle_network_status)
        self.network_thread.start()

        # 加载保存的用户名、密码和自动登录设置
        self.load_credentials()

    def handle_network_status(self, status):
        """处理网络检查结果"""
        if status:
            InfoBar.success(
                title="状态",
                content="网络已连接，将在5秒后关闭...",
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,  # 自动隐藏时间（毫秒）
                parent=self
            )
            self.ui.button_login.setEnabled(False)  # 禁用登录按钮
            # 创建一个定时器，在5秒后自动关闭应用程序
            QTimer.singleShot(5000, self.close_application)
        else:
            InfoBar.info(
                title="状态",
                content="网络未连接，自动登录中...",
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,
                parent=self
            )
            self.login()  # 自动尝试登录

    def load_credentials(self):
        """加载保存的用户名和密码"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            if 'Credentials' in self.config:
                self.ui.input_username.setText(self.config['Credentials'].get('username', ''))
                self.ui.input_password.setText(self.config['Credentials'].get('password', ''))
                if self.config['Credentials'].get('autologin', 'false') == 'true':
                    self.ui.checkbox_autologin.setChecked(True)
        print(f"已加载用户名: {self.ui.input_username.text()}")  # 日志输出

    def save_credentials(self):
        """保存用户名和密码到config.ini"""
        self.config['Credentials'] = {
            'username': self.ui.input_username.text(),
            'password': self.ui.input_password.text(),
            'autologin': 'true' if self.ui.checkbox_autologin.isChecked() else 'false'
        }
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        print(f"保存了用户名: {self.ui.input_username.text()}，自动登录状态: {self.ui.checkbox_autologin.isChecked()}")  # 日志输出

    def login(self):
        """登录操作"""
        data = {
            "wlanacname": "NFV-BASE",
            "vlan": "0",
            "userid": self.ui.input_username.text(),
            "passwd": self.ui.input_password.text(),
            "wlanuserip": get_ip_address(),
            "mac": get_mac_address()
        }

        # 对数据进行URL编码
        encoded_data = urllib.parse.urlencode(data)

        print(f"登录请求数据 (编码后): {encoded_data}")  # 日志输出

        # 启动登录线程，避免UI卡顿
        self.login_thread = LoginThread(self.login_url, self.headers, encoded_data)
        self.login_thread.login_result.connect(self.handle_login_result)
        self.login_thread.start()

    def handle_login_result(self, success, message):
        if success:
            # 弹出一个 InfoBar，通知用户登录成功，并提示将在 5 秒后关闭程序
            InfoBar.success(
                title="登录成功",
                content="登录成功，将在5秒后关闭...",
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,
                parent=self
            )
            self.ui.button_login.setEnabled(False)
            # 保存用户名密码
            self.save_credentials()

            # 创建一个定时器，在5秒后自动关闭应用程序
            QTimer.singleShot(5000, self.close_application)

        else:
            # 根据不同的失败信息显示不同的提示
            if "帐号不存在" in message:
                InfoBar.error(
                    title="登录失败",
                    content="帐号不存在，请检查输入。",
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=3000,
                    parent=self
                )
            elif "密码错误" in message:
                InfoBar.error(
                    title="登录失败",
                    content="密码错误，请重试。",
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=3000,
                    parent=self
                )
            elif "参数错误" in message:
                InfoBar.error(
                    title="系统错误",
                    content="参数错误，请联系管理员。",
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=3000,
                    parent=self
                )
            elif "登录失败" in message:
                InfoBar.error(
                    title="登录失败",
                    content="认证失败，请重试。",
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=3000,
                    parent=self
                )
            else:
                InfoBar.error(
                    title="登录失败",
                    content="未知错误，请联系技术支持。",
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=3000,
                    parent=self
                )

    def close_application(self):
        """关闭应用程序"""
        InfoBar.info(
            title="提示",
            content="关闭中...",
            position=InfoBarPosition.TOP_RIGHT,
            duration=1000,
            parent=self
        )
        QTimer.singleShot(1000, QApplication.instance().quit)  # 在 3 秒后退出应用程序

    def logout(self):
        """下线操作"""
        url = "http://10.9.11.145/cgi-bin/wlogout.cgi"
        print("发送下线请求...")  # 日志输出
        try:
            response = requests.get(url)
            print(f"服务器响应状态码: {response.status_code}")  # 日志输出
            if response.status_code == 200:
                InfoBar.success(
                    title="成功",
                    content="您已成功下线",
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=3000,
                    parent=self
                )
                self.ui.button_login.setEnabled(True)
            else:
                InfoBar.error(
                    title="错误",
                    content="下线操作失败",
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=3000,
                    parent=self
                )
        except Exception as e:
            print(f"请求失败: {e}")  # 日志输出
            InfoBar.error(
                title="请求失败",
                content=f"{e}",
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,
                parent=self
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置QFluentWidgets的主题为自动
    setTheme(Theme.AUTO)  # 设置主题为自动（根据系统）

    login_app = LoginApp()
    login_app.show()
    sys.exit(app.exec())
