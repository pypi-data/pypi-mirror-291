import subprocess
import time

class StreamlitServersubprocess():
    def __init__(self, script_path, port_number):
        self.script_path = script_path
        self.port_number = port_number
        self.streamlit_process = None
    #
    def start(self):
        # 启动 Streamlit 服务
        self.streamlit_process=subprocess.Popen([r'.\pyhton3864\python','-m',"streamlit", "run", self.script_path, "--server.port", str(self.port_number),"--server.headless",'true'])

    def stop(self):
        # 停止 Streamlit 服务
        if self.streamlit_process is not None:
            self.streamlit_process.terminate()
            self.streamlit_process.wait()
            self.streamlit_process = None

# def start_streamlit_app(script_path):
#     # 指定的端口号
#     port_number = 8502
#     # 启动 Streamlit 服务
#     # streamlit_process = subprocess.Popen(["streamlit", "run", script_path])
#     streamlit_process = subprocess.Popen(["streamlit", "run", script_path, "--server.port", str(port_number),"--server.headless",'true'])
#     # streamlit_process = subprocess.Popen(["streamlit", "run", script_path, "--server.port", str(port_number)])
#
#     try:
#         # 让 Streamlit 服务运行一段时间，或者等待某些条件发生
#         time.sleep(100)  # 假设我们让 Streamlit 运行 10 秒
#
#         # 停止 Streamlit 服务
#         streamlit_process.terminate()  # 尝试优雅地停止进程
#         streamlit_process.wait()  # 等待进程结束
#     # """启动 Streamlit 应用"""
#     # try:
#     #     # 使用 subprocess 运行 streamlit run 命令
#     #     subprocess.run(["streamlit", "run", script_path], check=True)
#     except streamlit_process.CalledProcessError as e:
#         print(f"Streamlit 应用启动失败: {e}")
#
# if __name__ == "__main__":
#     # 假设你的 Streamlit 应用脚本名为 app.py，并且与当前脚本在同一目录下
#     start_streamlit_app("home_page_main.py")