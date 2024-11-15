import socket
import uuid
import requests
import subprocess
import os

def get_ip_address():
    """获取本机IP地址"""
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(f"IP: {ip_address}")
        return ip_address
    except Exception as e:
        print(f"获取IP地址失败: {e}")  # 保留详细错误日志
        return None

def get_mac_address():
    """获取本机MAC地址"""
    try:
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                        for elements in range(0, 2 * 6, 2)][::-1])
        print(f"MAC: {mac}")
        return mac
    except Exception as e:
        print(f"获取MAC地址失败: {e}")  # 保留详细错误日志
        return None

def is_network_connected():
    """检查网络连接是否正常"""
    try:
        response = requests.get('http://www.gstatic.com/generate_204', timeout=3)
        if response.status_code == 204:
            return True
        else:
            print(f"网络未连接，HTTP状态码: {response.status_code}")  # 保留详细错误日志
            return False
    except requests.RequestException as e:
        print(f"网络请求异常: {e}")  # 保留详细错误日志
        return False

def ping_test(target):
    """执行Ping测试"""
    success = False
    for i in range(5):
        try:
            param = '-n' if os.name == 'nt' else '-c'
            command = ['ping', param, '1', target]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                print(f"第 {i + 1} 次 Ping {target} 成功")
                success = True
                break
            else:
                print(f"第 {i + 1} 次 Ping {target} 失败，返回码: {result.returncode}")  # 保留详细错误日志
        except Exception as e:
            print(f"Ping 失败: {e}")  # 保留详细错误日志
    return success
