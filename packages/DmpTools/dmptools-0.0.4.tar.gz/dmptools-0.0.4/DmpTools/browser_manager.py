# --coding:utf-8--
import subprocess
import socket
import psutil
# 输入Chrome浏览器所在路径
def create_browser_remote(port,headless=True):
    # chrome_path = r"C:\chromium-1045\chrome-win\Chrome.exe"
    chrome_path = r"browser\ms-playwright\chromium-1045\chrome-win\Chrome.exe"
    webset = '--new-window "https://ibsaaspre.rongdasoft.com/"'
    debugging_port = f'--remote-debugging-port={port}'

    if not headless:
        # 设置为无头模式
        is_headless = '--headless'
    else:
        # 设置为有头模式
        is_headless = ''

    # 启动Chrome浏览器
    command = f"{chrome_path} {webset} {debugging_port} {is_headless}"

    # command = f"{chrome_path} {debugging_port}"
    subprocess.Popen(command, shell=True)


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_by_port(port):
    # 获取所有网络连接
    connections = psutil.net_connections()
    # 遍历网络连接
    for conn in connections:
        if conn.status == psutil.CONN_LISTEN and conn.laddr.port == port:
            # 找到占用端口的进程
            proc = psutil.Process(conn.pid)
            # 杀死进程
            proc.kill()
            print(f"Process {proc.pid} (Name: {proc.name()}) using port {port} has been killed.")
            break  # 假设端口只被一个进程占用，找到后即可退出

def refresh_scrape_browser_on_this_port_win(headless=False,port='26666'):
    # 检查端口是否被占用
    if is_port_in_use(int(port)):
        # 杀死占用端口的进程
        kill_process_by_port(int(port))

    # 启动浏览器
    create_browser_remote(port,headless)



if __name__ == "__main__":
    refresh_scrape_browser_on_this_port_win(headless=True)
    # main()
