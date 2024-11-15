import requests
import urllib.parse


class LoginManager:
    def __init__(self, login_url, headers):
        self.login_url = login_url
        self.headers = headers

    def login(self, username, password, ip_address, mac_address):
        """执行登录操作

        Args:
            username (str): 用户名
            password (str): 密码
            ip_address (str): IP 地址（从 utils 获取）
            mac_address (str): MAC 地址（从 utils 获取）

        Returns:
            tuple: (bool, str)，表示是否登录成功和返回的消息
        """

        # 构造请求数据
        data = {
            "wlanacname": "NFV-BASE",
            "vlan": "0",
            "userid": username,  # 用户名
            "passwd": password,  # 密码
            "wlanuserip": ip_address,  # 从 utils 获取的 IP 地址
            "mac": mac_address  # 从 utils 获取的 MAC 地址
        }

        # 对数据进行 URL 编码
        encoded_data = urllib.parse.urlencode(data)

        # 发送登录请求
        try:
            response = requests.post(self.login_url, headers=self.headers, data=encoded_data)

            # 处理服务器响应
            if "成功登陆" in response.text:
                return True, "登录成功"
            elif "帐号不存在" in response.text:
                return False, "帐号不存在"
            elif "密码错误" in response.text:
                return False, "认证失败"
            elif "认证失败" in response.text:
                return False, "认证失败"
            elif "系统错误" in response.text:
                return False, "参数错误"
            else:
                return False, "未知错误"

        except Exception as e:
            # 错误捕获
            return False, f"请求失败: {str(e)}"
