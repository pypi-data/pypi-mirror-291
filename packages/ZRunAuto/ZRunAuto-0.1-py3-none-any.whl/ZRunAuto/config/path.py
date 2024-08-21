import os

log_file_name = "test_log"
report = "report"
project_name = 'bigsun-python'
# 获取当前目录
cur_path = os.path.abspath(os.path.dirname(__file__))

# 获取根目录
dir = cur_path[:cur_path.find(project_name)]

my_log_file_path = os.path.join(dir, project_name, log_file_name)

CONFIG_PATH = os.path.join(dir, project_name, 'config.ini')


def get_report_path(task_id):
    REPORT_PATH = os.path.join(dir, project_name, report, str(task_id), 'results')
    HTML_PATH = os.path.join(dir, project_name, report, str(task_id), 'html')
    return REPORT_PATH, HTML_PATH
