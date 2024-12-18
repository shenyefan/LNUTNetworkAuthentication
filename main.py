import sys
import requests
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer, QThread, Signal
from qfluentwidgets import Theme, setTheme, InfoBar, InfoBarPosition
from LoginWindow import Ui_Form
from utils.config_manager import ConfigManager
from utils.login_manager import LoginManager
from utils.network import get_ip_address, get_mac_address, is_network_connected, ping_test


class NetworkWorker(QThread):
    network_status = Signal(bool, bool)  # 添加一个额外的参数

    def __init__(self, target, parent=None):
        super().__init__(parent)
        self.target = target

    def run(self):
        """同时执行Ping测试和网络连接检测"""
        success_ping = ping_test(self.target)
        success_network = is_network_connected()
        self.network_status.emit(success_ping, success_network)


class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 初始化配置管理器和登录管理器
        self.config_manager = ConfigManager()
        self.login_manager = LoginManager(
            login_url="http://10.9.18.71/portalAuthAction.do",
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            }
        )

        # 连接信号和槽
        self.ui.button_login.clicked.connect(self.login)
        self.ui.button_logout.clicked.connect(self.logout)

        # 保存倒计时定时器的实例
        self.timer = None
        self.user_action_triggered = False  # 新增标志位

        # 加载保存的用户名和密码
        self.load_credentials()

        # 使用定时器在主界面显示后进行网络检测
        QTimer.singleShot(100, self.check_network_status)

    def load_credentials(self):
        """加载保存的用户名和密码"""
        credentials = self.config_manager.load_credentials()
        self.ui.input_username.setText(credentials.get("username", ""))
        self.ui.input_password.setText(credentials.get("password", ""))
        self.ui.checkbox_autologin.setChecked(credentials.get("autologin", False))

    def save_credentials(self):
        """保存用户名和密码"""
        self.config_manager.save_credentials(
            username=self.ui.input_username.text(),
            password=self.ui.input_password.text(),
            autologin=self.ui.checkbox_autologin.isChecked()
        )

    def check_network_status(self):
        """检查网络状态"""
        self.show_info_bar("状态", "检测网络连接中", "info")
        # 启动后台线程检测网络
        self.network_worker = NetworkWorker('10.9.18.71', self)
        self.network_worker.network_status.connect(self.handle_network_status)  # 连接信号到处理槽
        self.network_worker.start()

    def handle_network_status(self, success_ping, success_network):
        if success_ping:
            if success_network:
                self.show_info_bar("状态", "网络已连接", "success")
                self.toggle_login_ui(False)
                self.start_close_timer()
            else:
                self.show_info_bar("状态", "校园网未登录", "warning")
                if self.ui.checkbox_autologin.isChecked():
                    if self.user_action_triggered:
                        return  # 如果用户动作触发，则不执行后续操作
                    QTimer.singleShot(1000, self.login)
        else:
            self.show_info_bar("状态", "未连接到校园网", "error")
            self.start_close_timer()

    def login(self):
        self.user_action_triggered = True  # 设置标志位
        self.show_info_bar("状态", "尝试登录中", "info")
        """执行登录操作"""
        self.toggle_all_ui(False)
        ip_address = get_ip_address()
        mac_address = get_mac_address()

        success, message = self.login_manager.login(
            username=self.ui.input_username.text(),
            password=self.ui.input_password.text(),
            ip_address=ip_address,
            mac_address=mac_address
        )

        print(f"服务器响应内容: {message}")

        if success:
            self.show_info_bar("登录成功", "将在5秒后关闭", "success")
            self.toggle_logout_ui(True)
            self.save_credentials()
            self.start_close_timer()
        else:
            self.show_info_bar("登录失败", message, "error")
            QTimer.singleShot(1000, lambda: self.toggle_all_ui(True))

    def logout(self):
        self.user_action_triggered = True  # 设置标志位
        """执行下线操作"""
        self.toggle_all_ui(False)
        # 中断任何现存的关闭倒计时
        if self.timer and self.timer.isActive():
            self.timer.stop()
            self.show_info_bar("状态", "关闭操作已取消", "info")
        url = "http://10.9.11.145/cgi-bin/wlogout.cgi"
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                self.show_info_bar("状态", "下线成功", "success")
            else:
                self.show_info_bar("下线失败", f"HTTP状态码: {response.status_code}", "error")
        except Exception as e:
            self.show_info_bar("请求失败", f"错误: {e}", "error")
        finally:
            QTimer.singleShot(1000, lambda: self.toggle_all_ui(True))

    def toggle_all_ui(self, enable):
        """切换UI控件的可用状态"""
        self.ui.button_login.setEnabled(enable)
        self.ui.button_logout.setEnabled(enable)
        self.ui.input_username.setEnabled(enable)
        self.ui.input_password.setEnabled(enable)
        self.ui.checkbox_autologin.setEnabled(enable)

    def toggle_logout_ui(self, enable):
        """切换UI控件的可用状态"""
        self.ui.button_logout.setEnabled(enable)

    def toggle_login_ui(self, enable):
        """切换UI控件的可用状态"""
        self.ui.button_login.setEnabled(enable)
        self.ui.input_username.setEnabled(enable)
        self.ui.input_password.setEnabled(enable)
        self.ui.checkbox_autologin.setEnabled(enable)

    def close_application(self):
        """关闭应用程序"""
        self.show_info_bar("提示", "关闭中...", "info")
        QTimer.singleShot(1000, QApplication.instance().quit)

    def show_info_bar(self, title, content, bar_type="info"):
        """统一展示提示信息的 InfoBar"""
        bar_types = {
            "success": InfoBar.success,
            "info": InfoBar.info,
            "warning": InfoBar.warning,
            "error": InfoBar.error
        }
        bar_function = bar_types.get(bar_type, InfoBar.info)
        bar_function(
            title=title,
            content=content,
            position=InfoBarPosition.TOP_RIGHT,
            duration=3000,
            parent=self
        )

    def start_close_timer(self):
        """开始关闭应用程序的倒计时"""
        if self.timer:
            self.timer.stop()  # 停止任何现有的定时器
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.close_application)
        self.timer.start(5000)  # 5秒后触发


if __name__ == "__main__":
    app = QApplication(sys.argv)
    setTheme(Theme.AUTO)
    login_app = LoginApp()
    login_app.show()
    sys.exit(app.exec())
