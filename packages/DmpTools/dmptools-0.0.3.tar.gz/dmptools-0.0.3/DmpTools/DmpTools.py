# -*- coding: utf-8 -*-
import sys, os
import time
sys.path.append( os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, os.path.join( os.path.dirname(os.path.abspath(__file__)),"streamlit")   )
import traceback
import os,re
from clazz import demo
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEnginePage, QWebEngineProfile,QWebEngineDownloadItem
import datetime
import StreamlitServerrun

class DmpTools(QMainWindow, demo.FunctionObject):
    def __init__(self,token = ""):
        super().__init__()
        try:
            self.min_version = "0.2.0.24"
            # self.min_version = "0.2.0.9"
            self.startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.token = token
            self.FunctionName = "IT数据中台小工具"
            self.description = '''
=================================================
功能介绍：IT数据中台校对模块快捷键以及聚类快速检索移动图片
包名：DmpTools
版本号：0.0.3
作者：彭程，李坤
教程地址：https://XXX.com/
=================================================
'''


            self.mainfolder = os.path.dirname(__file__)
            self.img_folder = os.path.join(self.mainfolder, "icons")
            self.startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.setWindowTitle('IT数据中台聚类快速检索移动图片')
            self.setGeometry(150, 50, 900, 600)
            # 设置窗口图标
            self.setWindowIcon(
                QIcon(os.path.join(self.img_folder, "logo.png")))
            # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 使得窗口始终保持在最前面
            self.setStyleSheet('QMainWindow::title { min-height: 300px; min-width: 1000px; }')  # 设置标题栏中图标的大小

            # 创建标签控件
            self.tab_page = QTabWidget()
            self.tab_page.setTabsClosable(True)
            self.tab_page.setMovable(True)
            self.tab_page.setStyleSheet("""
                QTabBar::tab{
                    min-width:200px;
                    max-width:200px;
                    text-align:left;
                }
                QTabBar::tab:selected{
                    background-color:rgb(132,171,208)
    
                }
            """)
            self.tab_page.setTabShape(QTabWidget.Triangular)
            self.tab_page.tabCloseRequested.connect(self.close_tab)

            # 创建浏览页
            self.browser1 = WebEngineView(self.tab_page)
            self.browser1.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
            self.browser1.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
            self.browser1.settings().setAttribute(
                QWebEngineSettings.FullScreenSupportEnabled, True)


            self.browser1.setUrl(QUrl(f"http://localhost:8503/"))
            # 页面加载完成后注入 Polyfill
            self.browser1.page().loadFinished.connect(self.on_load_finished)
            # self.browser1.page().loadFinished.connect(self.on_load_finished2)
            self.browser1.loadFinished.connect(self.check_page_loaded)
            self.setCentralWidget(self.tab_page)
            self.tab_page.addTab(self.browser1, "功能页面")

            # 下载跳转
            profile1 = QWebEngineProfile.defaultProfile()
            profile1.downloadRequested.connect(self.download_requested5)
            self.browser1.loadFinished.connect(self.page_loaded)
            self.center()

            pattern = re.compile('版本号.*?((\d.){2}\d)\s')
            packageVersion = re.search(pattern, self.description).group(1)
            self.endTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            self.FunctionLog(330, self.token, '',1,1,self.startTime, self.endTime,"IT数据中台聚类快速检索移动图片", packageVersion)
        except:
            self.endTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            with open(f"./log/IT数据中台聚类快速检索移动图片{self.endTime}.txt", "a", encoding="utf8") as f:
                traceback.print_exc(file= f)
            traceback.print_exc()



    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # 停止 Streamlit 服务
        self.Streamlitrun.stop()
        super().closeEvent(a0)

    def on_load_finished(self, ok):
        if ok:
            # 编写 polyfill 代码
            polyfill_code = """  
            (function() {  
                if (!Array.prototype.at) {  
                    Object.defineProperty(Array.prototype, 'at', {  
                        value: function(index) {  
                            if (index < 0) index += this.length;  
                            return this[index >= 0 ? index : undefined];  
                        },  
                        writable: true,  
                        enumerable: false,  
                        configurable: true  
                    });  
                }  
            })();
            String.prototype.replaceAll = function(search, replacement) {
              var target = this;
              return target.split(search).join(replacement);
            };
              
            """
            # 在页面上执行 JavaScript 代码来注入 polyfill
            self.browser1.page().runJavaScript(polyfill_code)

    # 点击唤起工具箱
    def show(self):
        flag = True
        for cur_v, min_v in zip(self.version.split('.'), self.min_version.split('.')):
            if int(cur_v)< int(min_v):
                flag = False
                break
        if flag:
            try:
                self.Streamlitrun = StreamlitServerrun.StreamlitServersubprocess(r".\clazz\DmpTools\custom_key_event.py",  '8503')
                self.Streamlitrun.start()
                time.sleep(3)
                super().show()
                self.browser1.reload()
            except:
                traceback.print_exc()
                self.endTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                with open(f"./log/IT数据中台聚类快速检索移动图片失败日志{self.endTime}.txt", "a", encoding="utf8") as f:
                    traceback.print_exc(file= f)
                traceback.print_exc()
        else:
            msg_box = QMessageBox(QMessageBox.Question, "提示", f"当前工具箱版本过低，请升级至{self.min_version}及以上版本")
            msg_box.setStandardButtons(QMessageBox.Yes)
            msg_box.setWindowFlags(msg_box.windowFlags())
            timer = QTimer()
            timer.setSingleShot(True)
            timer.timeout.connect(msg_box.button(QMessageBox.Yes).click)
            timer.start(30 * 1000)
            msg_box.exec_()

    def showEvent(self, a0: QtGui.QShowEvent):
        super().showEvent(a0)

    # 关闭Tab页
    def close_tab(self):
        pass

    def download_requested5(self, download: QWebEngineDownloadItem):
        # 获取下载请求的相关信息
        # url = download.url()
        file_name_defined = download.path().split("/")[-1]
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        # 打开文件对话框
        flag1=file_dialog.getExistingDirectory(self, "浏览", "./")


        if os.path.exists(flag1) and len(flag1.split('/'))>1:
            if flag1.split('/')[1]!='':

                file_name=os.path.join(flag1, file_name_defined)
                # 设置下载保存路径
                download.setPath(file_name)

                # 开始下载
                download.accept()
                self.progressBarshow=initUIprogressBar()
                self.progressBarshow.center()
                self.progressBarshow.show()
                download.downloadProgress.connect(self.print_progress)
            else:
                QMessageBox.information(self, "下载错误", "请勿保存在磁盘根目录！", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "下载错误", "没有保存成功！", QMessageBox.Ok)

    def page_loaded(self):
        # 网页加载完成后的处理
        pass


    def print_progress(self,received,total):
        if total>0:
            progress = round(received / total*100,2)  # 计算进度百分比
            self.progressBarshow.downloadprogressBar.setValue(progress)
            print("Download progress: {}%".format(progress))
            if self.progressBarshow.downloadprogressBar.value()==100:
                self.progressBarshow.close_window()
                QMessageBox.information(self, "下载成功", "下载完成！", QMessageBox.Ok)


    def center(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = int((screen.width() - size.width()) / 2)
        newTop = int((screen.height() - size.height()) / 2)
        self.move(newLeft, newTop)


    def close_window(self):
        self.close()

    #重新加载网页
    def check_page_loaded(self, success):
        if not success:
            # 页面加载失败，可以尝试重新加载
            print("Page load failed, reloading...")
            self.browser1.reload()
        else:
            print("Page loaded successfully!")

class WebEngineView(QWebEngineView):
    def __init__(self, *args) -> None:
        QWebEngineView.__init__(self, *args)
        self.tab = self.parent()

    def createWindow(self, QWebEnginePage_WebWindowType):
        if QWebEnginePage_WebWindowType == QWebEnginePage.WebBrowserTab:
            self.new_webview = WebEngineView(self.tab)
            profile = self.new_webview.page().profile()
            # 或者强制将所有 Cookies 保存为持久性的（不推荐，除非有明确的需求）
            profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
            self.new_webview.setAttribute(Qt.WA_DeleteOnClose, True)
            self.new_webview.settings().setAttribute(
                QWebEngineSettings.PluginsEnabled, True)
            self.new_webview.settings().setAttribute(
                QWebEngineSettings.JavascriptEnabled, True)
            self.new_webview.settings().setAttribute(
                QWebEngineSettings.FullScreenSupportEnabled, True)
            self.ix = self.tab.addTab(self.new_webview, "loading...")
            self.tab.setCurrentIndex(self.ix)
            self.new_webview.loadFinished.connect(self.load_finish)
            self.new_webview.page().loadFinished.connect(self.on_load_finished)
            # self.new_webview.page().loadFinished.connect(self.on_load_finished2)

            return self.new_webview
        return super(WebEngineView, self).createWindow(QWebEnginePage_WebWindowType)

    # 当网页加载成功时，需要执行的代码
    def load_finish(self, *args):
        try:
            title = self.new_webview.page().title()
            if "http" in title:
                return
            self.tab.setTabText(self.ix, title)
            # self.new_webview.page().loadFinished.connect(self.on_load_finished)
        except Exception as e:
            print(e)

    #禁用右击菜单
    def contextMenuEvent(self, event):
        pass

    def on_load_finished(self, ok):
        if ok:
            # 编写 polyfill 代码
            polyfill_code = """  
            (function() {  
                if (!Array.prototype.at) {  
                    Object.defineProperty(Array.prototype, 'at', {  
                        value: function(index) {  
                            if (index < 0) index += this.length;  
                            return this[index >= 0 ? index : undefined];  
                        },  
                        writable: true,  
                        enumerable: false,  
                        configurable: true  
                    });  
                }  
            })();  
            String.prototype.replaceAll = function(search, replacement) {
              var target = this;
              return target.split(search).join(replacement);
            };                
            """
            # 在页面上执行 JavaScript 代码来注入 polyfill
            self.new_webview.page().runJavaScript(polyfill_code)


class initUIprogressBar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUIprogressBar()

    def initUIprogressBar(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.setWindowTitle('下载进度')
        self.setGeometry(500, 500, 400, 300)
        self.downloadprogressBar = QProgressBar(self)
        self.downloadprogressBar.setGeometry(300, 40, 250, 35)
        layout.addWidget(self.downloadprogressBar)
        layout.setAlignment(Qt.AlignCenter)  # 设置布局为居中对齐

        self.downloadprogressBar.setAlignment(Qt.AlignCenter)  # 设置对齐方式为居中对齐
        # 设置进度条样式
        self.downloadprogressBar.setStyleSheet("""  
                    QProgressBar {
                        border: 2px solid grey;
                        border-radius: 5px;
                    }

                    QProgressBar::chunk {
                        background-color: #05B8CC;
                        width: 20px;
                    }
        """)

    def center(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = int((screen.width() - size.width()) / 2)
        newTop = int((screen.height() - size.height()) / 2)
        self.move(newLeft, newTop)

    def close_window(self):
        self.close()





