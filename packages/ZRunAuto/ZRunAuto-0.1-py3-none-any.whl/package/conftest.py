import json
import time
from typing import List, Union, Tuple, Mapping

import pytest
import os

from _pytest.config import Config, PytestPluginManager
from _pytest.main import Session
from _pytest.mark import Mark
from _pytest.nodes import Item
from _pytest.reports import CollectReport, TestReport

from ZRunAuto.config import cache_v
from ZRunAuto.config.logger import log
from ZRunAuto.config.mqtt_config import MqttConfig
from ZRunAuto.config.path import get_report_path
from enum import Enum


class Option(Enum):
    REPORT_OPTION = '--report'
    TASK_OPTION = '--task_id'
    MSG_OPTION = '--msg'
    ENV_OPTION = '--env'
    PUSH_OPTION = '--push'


def pytest_addoption(parser, pluginmanager: PytestPluginManager):
    print('REPORT_PATH')
    print(pluginmanager.hasplugin('alluredir'))
    print(pluginmanager.hasplugin('--alluredir'))

    parser.addoption(Option.REPORT_OPTION.value,
                     action="store_true",
                     default=False,
                     help="是否生成测试报告")
    parser.addoption(Option.TASK_OPTION.value,
                     action="store",
                     default=None,
                     help="任务id")
    parser.addoption(Option.MSG_OPTION.value,
                     action="store_true",
                     default=False,
                     help="是否通知")
    parser.addoption(Option.ENV_OPTION.value,
                     action="store",
                     default='request',
                     help="是否通知")
    parser.addoption(Option.PUSH_OPTION.value,
                     action="store",
                     default=False,
                     help="是否同步进度")
    parser.addini("-named",
                  help='参数的帮助提示信息',
                  type="string",
                  default="qa", )


# 初始化挂钩
def pytest_configure(config: Config):
    print("# 初始化挂钩pytest_configure")
    # config.addinivalue_line('addopts', '--alluredir={}'.format(REPORT_PATH))
    config.addinivalue_line('addopts', '--cmdopt={}'.format('dev'))
    # print('get_config21', config.getoption('--allure'))
    print("getpid", os.getpid())
    print('get-pytest_configure', config.getini('-named'))
    print('get-pytest_configure', config.getoption('--push'))

    task_id = config.getoption(Option.TASK_OPTION.value)
    if config.getoption(Option.PUSH_OPTION.value):
        # todo 连接mqtt服务器
        MqttConfig.run(task_id)


@pytest.fixture(scope='session', autouse=True)
def get_token():
    data = {
        'env': 'learn',
        'region': 'sun',
        'Cookie': "sid=96b5ccde02750c9865ffdd3aba265daf"
    }
    # cache_v.cache.set('token', data)
    # print('pyfixture', cache_v.cache.get('token'))


@pytest.fixture(scope='session', autouse=True)
def get_config(request):
    # print('get_config', config.config.getoption('--allure'))
    print('get_config', request.config.getini('addopts'))


# def pytest_load_initial_conftests(early_config, args, parser):
#     early_config.addinivalue_line('addopts', '--alluredir={}'.format(REPORT_PATH))
#     print('pytest_load_initial_conftests')
#     print(early_config)
#     print(args)
#     print(parser)


def pytest_collection(session: Session):  # 收集挂钩  session: Session

    print('session.collect()')
    print(session.collect())


# 自定义收集用例处理方式
def processing_data(items: List[Item]) -> dict:
    class_json = {

    }
    for item in items:  # type:Item
        print(item.name)
        print(item.parent.name)
        print(item.parent)
        print(item.parent.own_markers)
        print(item.own_markers)
        print(item.fspath)
        print(item.nodeid)
        kwargs = {}
        case = CaseBean()
        marks = item.own_markers  # type:List[Mark]
        if not marks:
            case.caseName = 'Is not set'
            case.author = 'Is not set'
        else:
            for mark in marks:  # type:Mark
                if mark.name == 'info':
                    kwargs = mark.kwargs
                    break

        if 'name' not in kwargs:
            case.caseName = 'Is not set'
        if 'author' not in kwargs:
            case.author = 'Is not set'

        # 如果键存在则打印 True，不存在则打印 False
        # if any([item.parent.name in d for d in class_json['transferCaseList']]):

        if class_json.get(item.parent.name) is None:
            class_json[item.parent.name] = []

        case.name = item.name
        case.nodeId = item.nodeid

        class_json[item.parent.name].append(case.__str__())
    request_param = {
        'transferCaseList': []
    }
    for i in class_json:
        kwargs = {
            'className': i,
            'caseInfoList': class_json[i],
        }
        request_param['transferCaseList'].append(kwargs)
    return request_param


# 在执行收集后调用。可以过滤或重新排序。
def pytest_collection_modifyitems(session: Session, config: Config, items: List[Item]):
    print('session.items()')
    print(items)
    request_param = processing_data(items)
    print("case.__str__()")
    print(request_param)
    print('pytest_collection_modifyitems-----')
    print(request_param)
    print(json.dumps(request_param))
    # 调用插入数据同步接口
    task_id = config.getoption('--task_id')
    REPORT_PATH, HTML_PATH = get_report_path(task_id=task_id)
    print(os.access(REPORT_PATH, os.W_OK))
    # if os.path.exists(REPORT_PATH) is False:
    #     os.makedirs(REPORT_PATH)
    # print(config.getoption('--allure'))
    # raise Interrupted

    # def pytest_report_header(config):


def pytest_report_teststatus(report: Union[CollectReport, TestReport], config: Config) -> Tuple[
    str, str, Union[str, Mapping[str, bool]]]:
    task_id = config.getoption(Option.TASK_OPTION.value)
    MqttConfig.publish_msg(task_id, report)
    print(report)


# 获取用例执行结果
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    收集用例执行结果
    :param terminalreporter:
    :param exitstatus:
    :param config:
    :return:
    """
    pass_num = len(terminalreporter.stats.get("passed", []))
    total_num = terminalreporter._numcollected
    fail_num = len(terminalreporter.stats.get("failed", []))
    skipp_num = len(terminalreporter.stats.get("skipped", []))
    print("捕捉用例的通过对象", pass_num)
    print("捕捉用例的失败对象", fail_num)
    print("捕捉用例的跳过对象", skipp_num)
    print("exitstatus", exitstatus)
    print("summary_config", config)

    # print("terminalreporter", terminalreporter.stats.get())
    faild_list = list()
    faild_object = terminalreporter.stats.get("failed", [])
    print("捕捉用例总数", total_num)
    print("捕捉所有对象", terminalreporter.stats)

    for i in faild_object:
        print("获取失败用例集对象i:", i, type(i))
        print("获取失败用例集对象名称location", i.location)
        faild_list.append(i.location[-1])
        print("获取失败用例集日志", i.longrepr)
    print("获取msg状态", config.getoption('--msg'), bool(config.getoption('--msg')))
    if config.getoption('--msg'):
        link = 'www.baidu.com'
        task_id = config.getoption('--task_id')
        local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        message = f'Test:Report:taskId:{task_id}\n运行环境:env\n用例总数  {total_num} 通过数:{pass_num}  ' \
                  f'失败数:{fail_num}\n报告链接:{link}' \
                  f'\n执行时间:{local_time}'
        phone = [18257161894]
        # ding_talk_push(message=message, phone=phone)


# # 获取当前文件夹下所有文件名
# file_list = os.listdir("auto/request")
# file_list = glob.glob('auto/request/base/request*')
# print(file_list)
#
#
# if __name__ == '__main__':
#     # 打印文件名
#     for file_name in file_list:
#         print(file_name)
#
# def pytest_collection_modifyitems(items):
#     for item in items:
#         item.name = item.name.encode("utf-8").decode("unicode_escape")
#         print("获取itemname", item.name)
#         item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
#

# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     # 获取钩子方法的调用结果
#     out = yield
#     # 获取执行结果内容
#     report = out.get_result()
#     print('测试报告：{}'.format(report))
#     print('当前执行步骤：{}'.format(report.when))
#     print('当前执行测试用例：{}'.format(report.nodeid))
#     print('当前用例描述：{}'.format(report.nodeid))
#     print('当前执行结果：{}'.format(report.outcome))
#     print('当前报错信息：{}'.format(report.longrepr))
#     print('执行时间：{}'.format(report.duration))


def pytest_sessionfinish(session):
    print('endpytest_sessionfinishpytest_sessionfinishpytest_sessionfinish')
    print(session.config)
    print(session.config)
    config = session.config
    if config.getoption('--report') and config.getoption('--task_id') is not None:
        task_id = config.getoption('--task_id')
        REPORT_PATH, HTML_PATH = get_report_path(task_id=task_id)
        print(os.access(REPORT_PATH, os.W_OK))
        if os.path.exists(REPORT_PATH) is False:
            os.makedirs(REPORT_PATH)
        allure = f'allure generate {REPORT_PATH} -o {HTML_PATH} --clean'
        print('执行报告输出')
        os.system(allure)
        # allure_open = f'allure base {HTML_PATH}'
        # os.system(allure_open)


def pytest_collect_file():
    pass
    # print('收集器1')


def pytest_unconfigure(config):
    """
    配置卸载完毕之后执行，所有测试用例执行之后执行
    """
    MqttConfig.stop()
    print('所有用例执行完成执行')
    print(type(config.option))
    print(config.option.file_or_dir)
    print(config.args)
    print(config.getoption('--report') == 'True')
    print(config.getoption('--report'))
    if config.getoption('--report') == 'True' and config.getoption('--task_id') is not None:
        task_id = config.getoption('--task_id')
        REPORT_PATH, HTML_PATH = get_report_path(task_id=task_id)
        # print(os.access(REPORT_PATH, os.W_OK))
        # if os.path.exists(REPORT_PATH) is False:
        #     os.makedirs(REPORT_PATH)
        # allure = f'allure generate {REPORT_PATH} -o {HTML_PATH} --clean'
        # print('执行报告输出')
        # os.system(allure)


# 获取运行环境
@pytest.fixture(scope='session', autouse=True)
def get_run_env(request):
    log.info("pytestfixture:{}", request.config.getoption('env'))
    cache_v.cache.set('env', request.config.getoption('env'))
    return request.config.getoption('env')


# '--collect-only 只收集'
# '--env=prod' 环境,
# ''--report'' 是否输出报告,
# ''--msg'' 是否输出报告,
# ''--push'' 是否推送测试进度,
if __name__ == '__main__':
    pytest.main(
        ['./auto/request/sun/base/test_base.py', '-v', '--task_id=57111111111111111111111',
         '--alluredir=./report/57/results', '-q', '--push=true'])

# allure = f'allure generate {REPORT_PATH} -o {HTML_PATH} --clean'
# print('执行报告输出')
# os.system(allure)
