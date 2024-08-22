import json, copy, math
import threading, time, requests, traceback
import pandas as pd
from playwright.sync_api import sync_playwright
from playwright._impl._api_types import TimeoutError
import streamlit as st

# 搜索并移动文件
def search_and_move_file(page, src_file_path, des_file_path, kws, container):
    folder_level = dict()
    src_file_list = src_file_path.split("/")
    des_file_list = des_file_path.split("/")
    if len(des_file_list) < 3:
        container.error("目标文件夹不能是一级文件夹和二级文件夹")
        return
    page.query_selector('//div[@id="tab-task-list" and text()="任务列表"]').click()
    time.sleep(1)
    with page.expect_response(
            "https://it-plat.rongdasoft.com/gateway/it-plat-parse-service/api/cluster/treeDir") as resp:
        page.query_selector('//div[@id="tab-extraction-verification" and text()="抽取校对"]').click()
    response = resp.value
    headers = response.request.all_headers()
    headers = {key: value for key, value in headers.items() if not key.startswith(':')}
    post_data = response.request.post_data_json
    response_data = response.json().get("data")
    des_folder_id_msg_list = ergodic_folder(copy.deepcopy(response_data), post_data, headers, des_file_list, folder_level, False)
    des_folder_id_msg_list = [i for i in des_folder_id_msg_list if "handled" not in i and i.get("name") == des_file_list[-1]]
    print("目标文件夹信息：", des_folder_id_msg_list)
    if not des_folder_id_msg_list:
        container.error("目标文件夹不存在，请重新输入")
        return
    else:
        des_folder_id_msg = des_folder_id_msg_list[0]
    folder_id_msg_list = ergodic_folder(copy.deepcopy(response_data), post_data, headers, src_file_list, folder_level)
    print("原路径文件夹信息：", folder_id_msg_list)
    if not folder_id_msg_list:
        container.error("原路径文件夹不存在，请重新输入")
        return
    folder_id_name_dict = {folder_id_msg.get("id"): folder_id_msg.get("name") for folder_id_msg in folder_id_msg_list}
    for id, name in folder_id_name_dict.items():
        if name == src_file_list[-1]:
            folder_id = id
    for kw in kws:
        label, include_keyword, exclude_keyword = kw
        if not include_keyword:
            include_keyword = ""
        if not exclude_keyword:
            exclude_keyword = ""
        include_keyword = ','.join([i for i in include_keyword.split(' ') if i])
        exclude_keyword = ','.join([i for i in exclude_keyword.split(' ') if i])
        container.info(f"开始执行{label}关键词，关键词内容为：包含关键词：{include_keyword}，排除关键词：{exclude_keyword}")
        try:
            folder_dict = get_file_list(folder_id, post_data, include_keyword, exclude_keyword, headers)
            # print("搜索出来的文件信息：", folder_dict)
            if not folder_dict:
                container.info("无搜索结果，如有需要，请检查关键词之后重新输入")
                continue
            screened_folder_dict = {item[0]:item[1] for item in folder_dict.items() if item[0] in folder_id_name_dict.keys()}
            screened_file_msg_dict = screen_file(screened_folder_dict, post_data, include_keyword, exclude_keyword, headers)
            print("搜索出来的原路径文件夹下的文件信息：", json.dumps(screened_file_msg_dict, ensure_ascii=False))
            if not screened_file_msg_dict:
                container.info("无搜索结果，如有需要，请检查关键词之后重新输入")
                continue
            move_file(des_folder_id_msg, folder_id_msg_list, screened_file_msg_dict, headers, folder_level, container)
            container.info(f"第{label}组关键词执行成功")
        except:
            container.error(f"{label}关键词执行失败")
    container.info("执行完毕")

# 保存文件层级
def save_folder_level(response_data, folder_level):
    for per_data in response_data:
        parent_id = per_data.get("parentId")
        id = per_data.get("id")
        if parent_id == "0":
            folder_level[id] = 1
        else:
            folder_level[id] = folder_level.get(parent_id) + 1

# 遍历文件夹，获取文件夹id
def ergodic_folder(response_data, post_data, headers, file_list, folder_level, get_all=True):
    save_folder_level(response_data, folder_level)
    if not get_all:
        file_list = file_list[:-1]
    for file_name in file_list:
        response_data = get_folder_id(response_data, post_data, headers, file_name)
        save_folder_level(response_data, folder_level)
    if get_all:
        for per_id_msg in response_data:
            if "handled" not in per_id_msg:
                response_data = get_folder_id(response_data, post_data, headers)
                save_folder_level(response_data, folder_level)
    return response_data

# 获取文件夹Id
def get_folder_id(response_data, post_data, headers, file_name=''):
    url = r'https://it-plat.rongdasoft.com/gateway/it-plat-parse-service/api/cluster/treeDir'
    if file_name:
        id_msg_list = [per_res_data for per_res_data in response_data if per_res_data.get("name") == file_name]
    else:
        id_msg_list = response_data
    supplemented_id_msg_list = list()
    for id_msg in id_msg_list:
        if "handled" not in id_msg:
            post_data["parentId"] = id_msg.get("id")
            response = requests.post(url=url, headers=headers, json=post_data)
            response_data = response.json().get("data")
            id_msg.update({"handled": True})
            supplemented_id_msg_list.extend(response_data)
    id_msg_list.extend(supplemented_id_msg_list)
    return id_msg_list

# 查询结果所在文件夹
def get_file_list(folder_id, post_data, include_keyword, exclude_keyword, headers):
    url = r'https://it-plat.rongdasoft.com/gateway/it-plat-parse-service/api/imageParseTaskSearch/searchStatistics'
    post_data = {"hasSelectCurrentFolder": False, "currentFolderId": folder_id, "parentId": folder_id,
                 "categoryResultFolderId": folder_id, "imageSelectScope": "", "orgId": post_data.get("orgId"),
                 "projectId":  post_data.get("projectId"), "ibsaasProjectId": post_data.get("ibsaasProjectId"),
                 "imageContentMustKeyWords": [include_keyword, exclude_keyword]}
    response = requests.post(url=url, headers=headers, json=post_data)
    folder_data = response.json().get("data")
    id_list = folder_data.get("folderIdList")
    name_list = folder_data.get("folderNameList")
    if id_list and name_list:
        folder_dict = {id:name for id, name in zip(id_list, name_list)}
    else:
        folder_dict = {}
    return folder_dict

# 查询结果信息
def screen_file(screened_folder_dict, post_data, include_keyword, exclude_keyword, headers):
    url = r'https://it-plat.rongdasoft.com/gateway/it-plat-parse-service/api/imageParseTaskSearch/search'
    file_msg_dict = dict()
    for folder_id, folder_name in screened_folder_dict.items():
        for i in range(10000):
            post_data = {"categoryResultFolderId": folder_id, "orgId": post_data.get("orgId"), "imageSelectScope": "",
                         "projectId": post_data.get("projectId"), "ibsaasProjectId": post_data.get("ibsaasProjectId"),
                         "pageNum": i, "pageSize": 50, "imageContentMustKeyWords": [include_keyword, exclude_keyword], "pageOrder": "ASC"}
            response = requests.post(url=url, headers=headers, json=post_data)
            file_data = response.json().get("data")
            total = int(file_data.get("total"))
            if folder_id not in file_msg_dict:
                file_msg_dict[folder_id] = file_data.get("records")
            else:
                file_msg_dict[folder_id].extend(file_data.get("records"))
            if total <= (i+1)*50:
                break
    return file_msg_dict

# 移动文件
def move_file(des_folder_id_msg, folder_id_msg_list, screened_file_msg_dict, headers, folder_level, container):
    num_per_times = 500
    des_folder_id = des_folder_id_msg.get("id")
    url = r'https://it-plat.rongdasoft.com/gateway/it-plat-parse-service/api/cluster/imageMove'
    for src_folder_id, file_msg_list in screened_file_msg_dict.items():
        if folder_level.get(src_folder_id) > 3:
            for folder_id_msg in folder_id_msg_list:
                if folder_id_msg.get("id") == src_folder_id:
                    src_p_folder_id = folder_id_msg.get("parentId")
        else:
            src_p_folder_id = src_folder_id
        image_list = [i.get("id") for i in file_msg_list]
        times_ = math.ceil(len(image_list) / num_per_times)
        for i in range(times_):
            from_ = i * num_per_times
            if i != times_ - 1:
                to_ = (i + 1) * num_per_times
                image_list_ = image_list[from_:to_]
            else:
                to_ = len(image_list)
                image_list_ = image_list[from_:]

            post_data = {"oldFolderId": src_folder_id, "oldThreeParentId": src_p_folder_id, "newFolderId": des_folder_id,
                         "newThreeParentId":  des_folder_id if folder_level.get(des_folder_id)==3 else des_folder_id_msg.get("parentId"),
                         "imageParseIdList": image_list_}
            print(post_data)
            try:
                response = requests.post(url=url, headers=headers, json=post_data)
                if response.json().get("success"):
                    container.info(f"第{from_+1}张到第{to_}张图片移动成功")
                else:
                    container.error(f"第{from_+1}张到第{to_}张图片移动失败")
            except:
                container.error(f"第{from_+1}张到第{to_}张图片移动失败")

def browser_operations(container):
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.connect_over_cdp('http://localhost:26666/')
        except:
            container.error("未找到浏览器，请先刷新浏览器")
            return
        context = browser.contexts[0]
        flag = False
        for page in context.pages:
            if page.title() == "IT数据中台":
                flag = True
                try:
                    src_file_path = st.session_state.info_dict.get("src_file_path", "")
                    des_file_path = st.session_state.info_dict.get("des_file_path", "")

                    kw_df = st.session_state.info_dict.get("editor_df")
                    labels = kw_df.index.values.tolist()
                    include_kws = kw_df["第一步"].values.tolist()
                    exclude_kws = kw_df["第二步"].values.tolist()
                    effective_kws = list()
                    for label, include_kw, exclude_kw in zip(labels, include_kws, exclude_kws):
                        if include_kw or exclude_kw:
                            effective_kws.append([label, include_kw, exclude_kw])

                    if effective_kws and src_file_path and des_file_path:
                        if len(src_file_path) > 100:
                            container.error(f"原路径过长，超过100个字符，请重新选择原路径")
                            return
                        if len(des_file_path) > 100:
                            container.error(f"目标路径过长，超过100个字符，请重新选择目标路径")
                            return
                        container.info(f"共{len(effective_kws)}组关键词待执行操作")
                        try:
                            search_and_move_file(page, src_file_path, des_file_path, effective_kws, container)
                        except TimeoutError:
                            container.error("执行超时")
                        except Exception as e:
                            container.error(f"执行失败，报错内容：{e}")
                    else:
                        if not src_file_path:
                            container.error("请输入原路径文件夹")
                        if not des_file_path:
                            container.error("请输入移入目标文件夹")
                        if not effective_kws:
                            container.error("未找到有效关键词，请重新输入")
                        return
                except Exception as e:
                    container.error(f"执行失败，报错内容：{e}")
        if not flag:
            container.error("未找到IT数据中台页面，请检查是否在浏览器中登录智慧云并打开相应页面")

# # 刷新浏览器
# def refresh_browser():
#     headless=True
#     refresh_button=st.button(label='刷新浏览器')
#     from browser_manager import refresh_scrape_browser_on_this_port_win
#     if refresh_button:
#         refresh_scrape_browser_on_this_port_win(headless)

# 执行操作
def search_and_move_file_action():
    expander1 = st.expander("聚类快速检索移动图片", expanded=True)
    try:
        if not hasattr(st.session_state, "clicked"):
            st.session_state.clicked = False
        if not hasattr(st.session_state, "info_dict"):
            st.session_state.info_dict = dict()
        st.session_state.info_dict["src_file_path"] = expander1.text_input("请输入原路径文件夹（全路径）")
        st.session_state.info_dict["des_file_path"] =  expander1.text_input("请输入移入目标文件夹（全路径）")
        kw_df = pd.DataFrame(
            data=[
                ["1", "", ""],
                ["2", "", ""],
                ["3", "", ""],
                ["4", "", ""],
                ["5", "", ""],
            ],
            columns=["组别","第一步", "第二步"]
        )
        kw_df.set_index("组别", inplace=True, drop=True)
        # width 702
        st.session_state.info_dict["editor_df"] = expander1.data_editor(data=kw_df, disabled=["组别"], width=702, column_config={
                                        "第一步": st.column_config.TextColumn(label="包含关键词", width="medium",  help="检索图片中（图片名与解析结果）包含以下所有关键字(多个关键词请用空格拼接，如'合同 发票')", default="", max_chars=100),
                                        "第二步": st.column_config.TextColumn(label="排除关键词", width="medium", help="在上步的检索范围内去除图片名与解析结果包含以下关键字(多个关键词请用空格拼接，如'合同 发票')", default="", max_chars=100),
                                   })
        button = expander1.button(label='开始移动')
        if button:
            expander1.info("正在运行，请勿重复点击<开始移动>按钮")
            browser_operations(expander1)
    except Exception as e:
        expander1.error(e)

def run():
    # refresh_browser()
    search_and_move_file_action()


if __name__=='__main__':
    run()