import configparser
import os

class ConfigManager:
    """用于管理配置文件的类"""

    def __init__(self, config_file="./config.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()

        # 如果配置文件存在，则加载配置
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)

    def load_credentials(self):
        """加载保存的用户名和密码"""
        credentials = {}
        if 'Credentials' in self.config:
            credentials['username'] = self.config['Credentials'].get('username', '')
            credentials['password'] = self.config['Credentials'].get('password', '')
            credentials['autologin'] = self.config['Credentials'].get('autologin', 'false') == 'true'
        return credentials

    def save_credentials(self, username, password, autologin=False):
        """保存用户名和密码到配置文件"""
        if 'Credentials' not in self.config:
            self.config['Credentials'] = {}

        self.config['Credentials']['username'] = username
        self.config['Credentials']['password'] = password
        self.config['Credentials']['autologin'] = 'true' if autologin else 'false'

        # 保存配置到文件
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        print(f"已保存用户名: {username}, 自动登录状态: {autologin}")

    def get(self, section, option, default=None):
        """获取配置项的值"""
        return self.config.get(section, option, fallback=default)

    def set(self, section, option, value):
        """设置配置项的值"""
        if section not in self.config:
            self.config.add_section(section)
        self.config.set(section, option, value)

        # 保存配置到文件
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
