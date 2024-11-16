import socket
import uuid
import requests


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
        response = requests.get('https://www.gstatic.com/generate_204', timeout=3)
        if response.status_code == 204:
            return True
        else:
            print(f"网络未连接，HTTP状态码: {response.status_code}")  # 保留详细错误日志
            return False
    except requests.RequestException as e:
        print(f"网络请求异常: {e}")  # 保留详细错误日志
        return False

def ping_test(target, timeout=2):
    """执行Ping测试"""
    success = False
    for i in range(5):
        try:
            # 尝试通过 socket 连接目标主机
            with socket.create_connection((target, 80), timeout):
                print(f"第 {i + 1} 次 Ping {target} 成功")
                success = True
                break
        except (socket.timeout, socket.error) as e:
            print(f"第 {i + 1} 次 Ping {target} 失败: {e}")
    return success