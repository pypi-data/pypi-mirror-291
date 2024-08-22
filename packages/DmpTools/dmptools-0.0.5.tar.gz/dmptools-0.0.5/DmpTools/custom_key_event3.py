import time, pyperclip

import datetime
import pandas as pd
import traceback
from pynput import keyboard
from playwright.sync_api import Playwright, sync_playwright, expect
from pynput.mouse import Button, Controller
import streamlit as st
import threading
from browser_manager import refresh_scrape_browser_on_this_port_win
from playwright._impl._api_types import Error as PlaywrightErrorss

# 刷新浏览器
def refresh_browser():
    headless=True
    refresh_button=st.button(label='刷新浏览器')
    if refresh_button:
        try:
            from pynput.keyboard import Controller as Controllerkey, Key
            keyboard1 = Controllerkey()
            # 模拟组合键操作（Ctrl+C）
            keyboard1.press(Key.ctrl)
            keyboard1.press(Key.shift)
            keyboard1.press(Key.alt)
            keyboard1.press('q')
            # time.sleep(0.1)
            keyboard1.release('q')
            keyboard1.release(Key.ctrl)
            keyboard1.release(Key.alt)
            keyboard1.release(Key.shift)
        except Exception as e:
            print(e)
            # pass
        refresh_scrape_browser_on_this_port_win(headless)

def browser_operations():
    print("快捷键线程已启动")
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.connect_over_cdp('http://localhost:26666/')
        except:
            print("未找到浏览器，请先刷新浏览器")
            return
        context = browser.contexts[0]
        global mouse
        flag = False
        for page in context.pages:
            if page.title() == "IT数据中台":
                flag = True
                while True:
                    if command_queue:
                        try:
                            command = command_queue.pop(0)
                            endTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                            with open(f"log/IT数据中台小工具{endTime}.txt", "a", encoding="utf8") as f:
                                f.write(command+ "\n")
                            global dict_label_name
                            if command == 'finish':
                                page.get_by_role("button", name="本页完成").click(timeout=200)
                            if command == 'cancelth':
                                mouse.press(Button.right)
                                mouse.release(Button.right)
                                page.get_by_text("取消关联表头").hover(timeout=200)
                                page.get_by_text("全部表头", ).click(timeout=200)
                            if command == 'biloc':
                                mouse = Controller()
                                mouse.press(Button.right)
                                mouse.release(Button.right)
                                page.get_by_text("双向定位", exact=True).click(timeout=500)
                            if command == 'label1':
                                mouse.press(Button.right)
                                mouse.release(Button.right)
                                label_name=dict_label_name['label1']
                                # page.get_by_text("关联表头").nth(0).hover(timeout=200)
                                # selector = f'div[title="{label_name}"].sheet-btn-text'
                                # page.query_selector(selector).click(timeout=200)
                                page.wait_for_selector('//div[@class="table-body"]//div[@class="sheet-btn" and contains(text(),"关联表头") and not(contains(text(),"取消"))]').click()
                                selector = f'div[title="{label_name}"].sheet-btn-text'
                                page.wait_for_selector(selector).click()
                            if command == 'label2':
                                mouse.press(Button.right)
                                mouse.release(Button.right)
                                label_name=dict_label_name['label2']
                                # page.get_by_text("关联表头").nth(0).hover(timeout=200)
                                # selector = f'div[title="{label_name}"].sheet-btn-text'
                                # page.query_selector(selector).click(timeout=200)
                                page.wait_for_selector('//div[@class="table-body"]//div[@class="sheet-btn" and contains(text(),"关联表头") and not(contains(text(),"取消"))]').click()
                                selector = f'div[title="{label_name}"].sheet-btn-text'
                                page.wait_for_selector(selector).click()
                            if command == 'label3':
                                mouse.press(Button.right)
                                mouse.release(Button.right)
                                label_name = dict_label_name['label3']
                                # page.get_by_text("关联表头").nth(0).hover(timeout=200)
                                # selector = f'div[title="{label_name}"].sheet-btn-text'
                                # page.query_selector(selector).click(timeout=200)
                                page.wait_for_selector('//div[@class="table-body"]//div[@class="sheet-btn" and contains(text(),"关联表头") and not(contains(text(),"取消"))]').click()
                                selector = f'div[title="{label_name}"].sheet-btn-text'
                                page.wait_for_selector(selector).click()
                            if command == 'label4':
                                mouse.press(Button.right)
                                mouse.release(Button.right)
                                label_name = dict_label_name['label4']
                                # page.get_by_text("关联表头").nth(0).hover(timeout=200)
                                # selector = f'div[title="{label_name}"].sheet-btn-text'
                                # page.query_selector(selector).click(timeout=200)
                                page.wait_for_selector('//div[@class="table-body"]//div[@class="sheet-btn" and contains(text(),"关联表头") and not(contains(text(),"取消"))]').click()
                                selector = f'div[title="{label_name}"].sheet-btn-text'
                                page.wait_for_selector(selector).click()
                            if command == 'label5':
                                mouse.press(Button.right)
                                mouse.release(Button.right)
                                label_name = dict_label_name['label5']
                                # page.get_by_text("关联表头").nth(0).hover(timeout=200)
                                # selector = f'div[title="{label_name}"].sheet-btn-text'
                                # page.query_selector(selector).click(timeout=200)
                                page.wait_for_selector('//div[@class="table-body"]//div[@class="sheet-btn" and contains(text(),"关联表头") and not(contains(text(),"取消"))]').click()
                                selector = f'div[title="{label_name}"].sheet-btn-text'
                                page.wait_for_selector(selector).click()
                            if command == 'label6':
                                mouse.press(Button.right)
                                mouse.release(Button.right)
                                label_name = dict_label_name['label6']
                                # page.get_by_text("关联表头").nth(0).hover(timeout=200)
                                # selector = f'div[title="{label_name}"].sheet-btn-text'
                                # page.query_selector(selector).click(timeout=200)
                                page.wait_for_selector('//div[@class="table-body"]//div[@class="sheet-btn" and contains(text(),"关联表头") and not(contains(text(),"取消"))]').click()
                                selector = f'div[title="{label_name}"].sheet-btn-text'
                                page.wait_for_selector(selector).click()
                            if command == 'label7':
                                mouse.press(Button.right)
                                mouse.release(Button.right)
                                label_name = dict_label_name['label7']
                                # page.get_by_text("关联表头").nth(0).hover(timeout=200)
                                # selector = f'div[title="{label_name}"].sheet-btn-text'
                                # page.query_selector(selector).click(timeout=200)
                                page.wait_for_selector('//div[@class="table-body"]//div[@class="sheet-btn" and contains(text(),"关联表头") and not(contains(text(),"取消"))]').click()
                                selector = f'div[title="{label_name}"].sheet-btn-text'
                                page.wait_for_selector(selector).click()
                            if command == 'label8':
                                mouse.press(Button.right)
                                mouse.release(Button.right)
                                label_name = dict_label_name['label8']
                                # page.get_by_text("关联表头").nth(0).hover(timeout=200)
                                # selector = f'div[title="{label_name}"].sheet-btn-text'
                                # page.query_selector(selector).click(timeout=200)
                                page.wait_for_selector('//div[@class="table-body"]//div[@class="sheet-btn" and contains(text(),"关联表头") and not(contains(text(),"取消"))]').click()
                                selector = f'div[title="{label_name}"].sheet-btn-text'
                                page.wait_for_selector(selector).click()
                            if command == 'label9':
                                mouse.press(Button.right)
                                mouse.release(Button.right)
                                label_name = dict_label_name['label9']
                                # page.get_by_text("关联表头").nth(0).hover(timeout=200)
                                # selector = f'div[title="{label_name}"].sheet-btn-text'
                                # page.query_selector(selector).click(timeout=200)
                                page.wait_for_selector('//div[@class="table-body"]//div[@class="sheet-btn" and contains(text(),"关联表头") and not(contains(text(),"取消"))]').click()
                                selector = f'div[title="{label_name}"].sheet-btn-text'
                                page.wait_for_selector(selector).click()
                            if command == 'label10':
                                mouse.press(Button.right)
                                mouse.release(Button.right)
                                label_name = dict_label_name['label10']
                                # page.get_by_text("关联表头").nth(0).hover(timeout=200)
                                # selector = f'div[title="{label_name}"].sheet-btn-text'
                                # page.query_selector(selector).click(timeout=200)
                                page.wait_for_selector('//div[@class="table-body"]//div[@class="sheet-btn" and contains(text(),"关联表头") and not(contains(text(),"取消"))]').click()
                                selector = f'div[title="{label_name}"].sheet-btn-text'
                                page.wait_for_selector(selector).click()
                            if command == 'select_folders_keyword':
                                root_dir_name = page.query_selector('//div[@class="operate"]/button[1]/span').text_content().strip()
                                if root_dir_name:
                                    keyword = pyperclip.paste()
                                    print(keyword)
                                    root_dir_expand_ele = page.wait_for_selector(
                                        f'//div[@role="tree"]/div[@role="treeitem"]/div/div/span[@title="{root_dir_name}"]/ancestor::div[@role="treeitem"]/div/span')
                                    root_dir_expand_ele_attr = root_dir_expand_ele.get_attribute("class")
                                    if "expanded" not in root_dir_expand_ele_attr:
                                        root_dir_expand_ele.click(position={"x": 6, "y": 12}, force=True)
                                        page.wait_for_load_state(state='load')

                                    for i in range(4):
                                        try:
                                            xpath = f'//div[@role="tree"]/div[@role="treeitem"]/div/div/span[@title="{root_dir_name}"]/../../..' + '/div[@class="el-tree-node__children"]/div[@role="treeitem"]' * i + '/div/span[contains(@class,"el-tree-node") and not(contains(@class, "expanded")) and not(contains(@class, "is-leaf"))]'
                                            while True:
                                                try:
                                                    ele_list = page.query_selector_all(xpath)
                                                    if ele_list:
                                                        for ele in ele_list:
                                                            ele.click(position={"x": 6, "y": 12}, force=True, no_wait_after=False)
                                                            page.wait_for_load_state(state="load")
                                                        time.sleep(0.2)
                                                    else:
                                                        break
                                                except PlaywrightErrorss as es:
                                                    if ("Target page, context or browser has been closed" in es.message) or ("Execution context was destroyed, most likely because of a navigation" in es.message):
                                                        raise es
                                                    else:
                                                        traceback.print_exc()
                                                except:
                                                    traceback.print_exc()
                                            if i < 3:
                                                xpath_ = f'//div[@role="tree"]/div[@role="treeitem"]/div/div/span[@title="{root_dir_name}"]/../../..' + '/div[@class="el-tree-node__children"]/div[@role="treeitem"]' * (i + 1) + '/div/span[contains(@class,"el-tree-node")]'
                                                page.wait_for_selector(xpath_, timeout=5000)
                                        except PlaywrightErrorss as es:
                                            if ("Target page, context or browser has been closed" in es.message) or ("Execution context was destroyed, most likely because of a navigation" in es.message):
                                                raise es
                                            else:
                                                traceback.print_exc()
                                        except:
                                            traceback.print_exc()
                                    if not keyword:
                                        continue
                                    while True:
                                        try:
                                            ele = page.query_selector(f'//div[@role="tree"]/div[@role="treeitem"]/div/div/span[@title="{root_dir_name}"]/ancestor::div[@role="treeitem"]//div[@role="treeitem"]/div/span[contains(@class, "el-tree-node__expand-icon")]/following-sibling::div[@data-id]/span[contains(@name,"{keyword}")]/../../label[not(contains(@class,"is-checked"))]')
                                            if ele:
                                                ele.click(position={"x": 6, "y": 7}, force=True)
                                                page.wait_for_load_state(state='load')
                                                time.sleep(0.02)
                                            else:
                                                break
                                        except PlaywrightErrorss as es:
                                            if ("Target page, context or browser has been closed" in es.message) or ("Execution context was destroyed, most likely because of a navigation" in es.message):
                                                raise es
                                            else:
                                                traceback.print_exc()
                                        except:
                                            traceback.print_exc()
                                else:
                                    print("请先选择一级目录文件夹")
                            if command == 'select_folders_quantity':
                                folders_quantity = dict_label_name['select_folders_quantity']
                                root_dir_name = page.query_selector('//div[@class="operate"]/button[1]/span').text_content().strip()
                                print(root_dir_name)
                                if root_dir_name:
                                    keyword = pyperclip.paste()
                                    print(keyword)
                                    root_dir_expand_ele = page.wait_for_selector(
                                        f'//div[@role="tree"]/div[@role="treeitem"]/div/div/span[@title="{root_dir_name}"]/ancestor::div[@role="treeitem"]/div/span')
                                    root_dir_expand_ele_attr = root_dir_expand_ele.get_attribute("class")
                                    if "expanded" not in root_dir_expand_ele_attr:
                                        root_dir_expand_ele.click(position={"x": 6, "y": 12}, force=True)
                                        page.wait_for_load_state(state='load')

                                    for i in range(4):
                                        try:
                                            xpath = f'//div[@role="tree"]/div[@role="treeitem"]/div/div/span[@title="{root_dir_name}"]/../../..' + '/div[@class="el-tree-node__children"]/div[@role="treeitem"]' * i + '/div/span[contains(@class,"el-tree-node") and not(contains(@class, "expanded")) and not(contains(@class, "is-leaf"))]'
                                            while True:
                                                try:
                                                    ele_list = page.query_selector_all(xpath)
                                                    print(ele_list)
                                                    if ele_list:
                                                        for ele in ele_list:
                                                            ele.click(position={"x": 6, "y": 12}, force=True, no_wait_after=False)
                                                            page.wait_for_load_state(state="load")
                                                        time.sleep(0.2)
                                                    else:
                                                        break
                                                except PlaywrightErrorss as es:
                                                    if ("Target page, context or browser has been closed" in es.message) or ("Execution context was destroyed, most likely because of a navigation" in es.message):
                                                        raise es
                                                    else:
                                                        traceback.print_exc()
                                                except:
                                                    traceback.print_exc()
                                            if i < 3:
                                                xpath_ = f'//div[@role="tree"]/div[@role="treeitem"]/div/div/span[@title="{root_dir_name}"]/../../..' + '/div[@class="el-tree-node__children"]/div[@role="treeitem"]' * (i + 1) + '/div/span[contains(@class,"el-tree-node")]'
                                                page.wait_for_selector(xpath_, timeout=5000)
                                        except PlaywrightErrorss as es:
                                            if ("Target page, context or browser has been closed" in es.message) or ("Execution context was destroyed, most likely because of a navigation" in es.message):
                                                raise es
                                            else:
                                                traceback.print_exc()
                                        except:
                                            traceback.print_exc()

                                    while True:
                                        try:
                                            click_num = 0
                                            click_ele_list = page.query_selector_all(
                                                f'//div[@role="tree"]/div[@role="treeitem"]/div/div/span[@title="{root_dir_name}"]/ancestor::div[@role="treeitem"]//div[@role="treeitem"]//span[contains(@class,"is-leaf")]/following-sibling::label[not(contains(@class,"is-checked"))]')
                                            num_ele_list = page.query_selector_all(
                                                f'//div[@role="tree"]/div[@role="treeitem"]/div/div/span[@title="{root_dir_name}"]/ancestor::div[@role="treeitem"]//div[@role="treeitem"]//span[contains(@class,"is-leaf")]/following-sibling::label[not(contains(@class,"is-checked"))]/following-sibling::div/span[@class="num-color"]')
                                            for click_ele, num_ele in zip(click_ele_list, num_ele_list):
                                                num = int(num_ele.text_content().strip("（").strip("）"))
                                                cflag = False
                                                if "大于等于" in folders_quantity:
                                                    quantity = int(folders_quantity.replace("大于等于", "").strip())
                                                    if num >= quantity:
                                                        cflag = True
                                                elif "大于" in folders_quantity:
                                                    quantity = int(folders_quantity.replace("大于", "").strip())
                                                    if num > quantity:
                                                        cflag = True
                                                elif "小于等于" in folders_quantity:
                                                    quantity = int(folders_quantity.replace("小于等于", "").strip())
                                                    if num <= quantity:
                                                        cflag = True
                                                elif "小于" in folders_quantity:
                                                    quantity = int(folders_quantity.replace("小于", "").strip())
                                                    if num < quantity:
                                                        cflag = True
                                                elif "等于" in folders_quantity:
                                                    quantity = int(folders_quantity.replace("等于", "").strip())
                                                    if num == quantity:
                                                        cflag = True
                                                print(num)
                                                if cflag:
                                                    click_ele.click(position={"x": 6, "y": 7}, force=True)
                                                    click_num += 1
                                                    page.wait_for_load_state(state='load')
                                                    time.sleep(0.02)
                                                    break
                                            if not click_num:
                                                break
                                        except PlaywrightErrorss as es:
                                            if ("Target page, context or browser has been closed" in es.message) or ("Execution context was destroyed, most likely because of a navigation" in es.message):
                                                raise es
                                            else:
                                                traceback.print_exc()
                                        except:
                                            traceback.print_exc()
                                else:
                                    print("请先选择一级目录文件夹")

                            if command == 'expand_all_folders':
                                for i in range(4):
                                    xpath = '//div[@role="tree"]/div[@role="treeitem"]' + '/div[@class="el-tree-node__children"]/div[@role="treeitem"]' * i + '/div/span[contains(@class,"el-tree-node") and not(contains(@class, "expanded")) and not(contains(@class, "is-leaf"))]'
                                    while True:
                                        try:
                                            ele_list = page.query_selector_all(xpath)
                                            if ele_list:
                                                for ele in ele_list:
                                                    # start_time = time.time()
                                                    ele.click(position={"x": 6, "y": 12}, force=True, no_wait_after=True)
                                                    page.wait_for_load_state(state="load")
                                                    # end_time = time.time()
                                                    # with open('log.txt', 'a', encoding='utf-8')as f:
                                                    #     f.write(f"{num}:{end_time - start_time}\n")
                                                    # num += 1
                                                time.sleep(0.2)
                                                # time.sleep(0.5)
                                            else:
                                                break
                                        except PlaywrightErrorss as es:
                                            if ("Target page, context or browser has been closed" in es.message) or ("Execution context was destroyed, most likely because of a navigation" in es.message):
                                                raise es
                                            else:
                                                traceback.print_exc()
                                        except:
                                            traceback.print_exc()
                                    if i < 3:
                                        try:
                                            xpath_ = '//div[@role="tree"]/div[@role="treeitem"]' + '/div[@class="el-tree-node__children"]/div[@role="treeitem"]' * (i + 1) + '/div/span[contains(@class,"el-tree-node")]'
                                            page.wait_for_selector(xpath_, timeout=5000)
                                        except PlaywrightErrorss as es:
                                            if ("Target page, context or browser has been closed" in es.message) or ("Execution context was destroyed, most likely because of a navigation" in es.message):
                                                raise es
                                            else:
                                                traceback.print_exc()
                                        except:
                                            traceback.print_exc()
                            if command == 'quit':
                                print("退出程序")
                                break
                            if command == 'internal_quit':
                                print("退出程序")
                                break
                        except PlaywrightErrorss as es:
                            if ("Target page, context or browser has been closed" in es.message) or ("Execution context was destroyed, most likely because of a navigation" in es.message):
                                browser = playwright.chromium.connect_over_cdp('http://localhost:26666/')
                                context = browser.contexts[0]
                                for page_ in context.pages:
                                    if page_.title() == "IT数据中台":
                                        page = page_
                                        break
                                command_queue.append(command)
                            else:
                                print(es)
                        except Exception as e:
                            print(e)
                    else:
                        time.sleep(0.1)
        if not flag:
            print("未找到IT数据中台页面，请检查是否在浏览器中登录智慧云并打开相应页面")

def on_activate_finish():
    command_queue.append('finish')

def on_activate_cancelth():
    command_queue.append('cancelth')

def on_activate_biloc():
    command_queue.append('biloc')

def on_activate_label1():
    command_queue.append('label1')

def on_activate_label2():
    command_queue.append('label2')

def on_activate_label3():
    command_queue.append('label3')

def on_activate_label4():
    command_queue.append('label4')

def on_activate_label5():
    command_queue.append('label5')

def on_activate_label6():
    command_queue.append('label6')

def on_activate_label7():
    command_queue.append('label7')

def on_activate_label8():
    command_queue.append('label8')

def on_activate_label9():
    command_queue.append('label9')

def on_activate_label10():
    command_queue.append('label10')

def on_activate_quit():
    command_queue.append('quit')
    raise keyboard.Listener.StopException

def on_activate_internal_quit():
    print("退出程序")
    command_queue.append('internal_quit')
    raise keyboard.Listener.StopException

def on_activate_select_folders_keyword():
    command_queue.append('select_folders_keyword')

def on_activate_select_folders_quantity():
    command_queue.append('select_folders_quantity')

def on_activate_expand_all_folders():
    command_queue.append('expand_all_folders')

dict_func={
    'on_activate_finish': on_activate_finish,
    'on_activate_cancelth': on_activate_cancelth,
    'on_activate_biloc': on_activate_biloc,
    'on_activate_label1': on_activate_label1,
    'on_activate_label2': on_activate_label2,
    'on_activate_label3': on_activate_label3,
    'on_activate_label4': on_activate_label4,
    'on_activate_label5': on_activate_label5,
    'on_activate_label6': on_activate_label6,
    'on_activate_label7': on_activate_label7,
    'on_activate_label8': on_activate_label8,
    'on_activate_label9': on_activate_label9,
    'on_activate_label10': on_activate_label10,
    'on_activate_quit': on_activate_quit,
    'on_activate_select_folders_keyword': on_activate_select_folders_keyword,
    'on_activate_select_folders_quantity': on_activate_select_folders_quantity,
    'on_activate_expand_all_folders': on_activate_expand_all_folders
}

#
# def refresh_browser():
#     headless=True
#     refresh_button=st.button(label='刷新浏览器')
#     from browser_manager import refresh_scrape_browser_on_this_port_win
#     if refresh_button:
#         refresh_scrape_browser_on_this_port_win(headless)

def refresh_info_dict(container):
    container.download_button(label="下载模版", data=open("clazz/DmpTools/快捷键列表.xlsx", 'rb'),
                          file_name="快捷键列表.xlsx",
                          mime="application/octet-stream",
                          help="""
                            快捷键格式要求：\n
                                1 功能类按钮需要用<>\n
                                2 多个快捷键用+连接\n
                                3 字母及数字按钮无需<>\n
                                举例：<Ctrl>+<Shift>+j\n
                                注：若不生效可能与浏览器、应用程序冲突所致，注意规避
                            """)

    file = container.file_uploader("上传表格文件", type=["csv", "xlsx"])
    # 将两个列表转换为字典
    global dict_hotkey
    dict_hotkey = {}
    if file:
        df = pd.read_excel(file, dtype=str)
        # 在Streamlit应用中显示DataFrame
        container.write(df)
        df = df.dropna(subset=['快捷键键位（按照格式自定义）'])
        # 获取第一列数据
        hotkey = df.iloc[:, 0].tolist()
        # 获取第二列数据
        command = df.iloc[:, 1].tolist()
        dict_hotkey0 = dict(zip(hotkey, command))
        global dict_label_name
        dict_label_name = {}
        for key in dict_hotkey0:
            dict_hotkey.update({key: dict_func[dict_hotkey0[key]]})
        dict_hotkey.update({'<ctrl>+<shift>+<alt>+q': on_activate_internal_quit})
        print(dict_hotkey)
        for key in command:
            if 'on_activate_label' in key or "folders_quantity" in key:
                print(key)
                label_name = key.replace('on_activate_', '')
                # dict_label_name[label_name]=df[df.iloc[:, 1] == key].iloc[0, 2]
                print(df[df.iloc[:, 1] == key].iloc[0, 3])
                dict_label_name.update({label_name: df[df.iloc[:, 1] == key].iloc[0, 3]})

def start_hotkey(container):
    refresh_button = container.button(label='快捷键，启动！')
    if refresh_button:
        try:
            from pynput.keyboard import Controller as Controllerkey, Key
            keyboard1 = Controllerkey()
            # 模拟组合键操作（Ctrl+C）
            keyboard1.press(Key.ctrl)
            keyboard1.press(Key.shift)
            keyboard1.press(Key.alt)
            keyboard1.press('q')
            # time.sleep(0.1)
            keyboard1.release('q')
            keyboard1.release(Key.ctrl)
            keyboard1.release(Key.alt)
            keyboard1.release(Key.shift)
        except Exception as e:
            print(e)
        global dict_hotkey
        if dict_hotkey:
            if check_run_env(container):
                # dict_hotkey.update({'<ctrl>+<shift>+<alt>+q': on_activate_internal_quit})
                browser_thread = threading.Thread(target=browser_operations)
                browser_thread.start()
                with keyboard.GlobalHotKeys(dict_hotkey) as h:
                    h.join()
        else:
            container.error("请先上传快捷键表格文件")

# 检查浏览器
def check_run_env(container):
    flag = False
    cnt_goal=0
    with sync_playwright() as playwright:
        try:
            try:
                browser = playwright.chromium.connect_over_cdp('http://localhost:26666/')
            except:
                container.error("未找到浏览器，请先刷新浏览器")
                return flag
            context = browser.contexts[0]
            global mouse
            for page in context.pages:
                if page.title() == "IT数据中台":
                    cnt_goal+=1
                    # flag = True
                if cnt_goal>1:
                    break

            if cnt_goal > 1:
                container.error("存在多个IT数据中台页面，请关闭多余页面")
            # if not flag:
            if cnt_goal==0:
                container.error("未找到IT数据中台页面，请检查是否在浏览器中登录智慧云并打开相应页面")
            if cnt_goal==1:
                flag = True
            return flag
        except Exception:
            container.error("遇到问题请联系IT数据中台-李坤")
            endTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            with open(f"log/IT数据中台小工具{endTime}.txt", "a", encoding="utf8") as f:
                traceback.print_exc(file=f)
            return flag

def hotkey_action():
    expander2 = st.expander("数据处理页面快捷键", expanded=True)
    try:
        global mouse
        mouse = Controller()
        global command_queue
        command_queue = []
        refresh_info_dict(expander2)
        start_hotkey(expander2)
    except Exception:
        expander2.error("遇到问题请联系IT数据中台-李坤")
        endTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        with open(f"log/IT数据中台小工具{endTime}.txt", "a", encoding="utf8") as f:
            traceback.print_exc(file=f)




def run():
    # refresh_browser()
    hotkey_action()

if __name__=='__main__':
    run()
    # expand_all_folders(1)