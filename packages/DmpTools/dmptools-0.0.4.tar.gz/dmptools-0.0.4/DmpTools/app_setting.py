import os
# 运行模式 streamlit pyqt
run_mode ='pyqt'
# run_mode ='streamlit'

base_path_streamlit='./'
# base_path_pyqt='./clazz/data_process_project_template'
base_path_pyqt=r'./clazz/DmpTools'

def path_with_run_mode(path1):
    if run_mode=='streamlit':
        base_path = base_path_streamlit
        file_path_fix = os.path.join(base_path, path1)
        return file_path_fix
    elif run_mode=='pyqt':
        base_path = base_path_pyqt
        file_path_fix = os.path.join(base_path, path1)
        return file_path_fix
    else:
        raise ValueError('run_mode must be streamlit or pyqt')