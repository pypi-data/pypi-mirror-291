import requests

from ZRunAuto.config import cache_v
from ZRunAuto.config.logger import log
from requests import Session, Response


def is_None(cookies):
    """判断cookies是否为空"""
    if cookies is None or len(cookies) == 0:
        return True
    else:
        return False


def get_token(config, data: dict):
    """config:BaseRequest"""
    request_session = config.request_type.session  # type:Session
    envs = config.env_param  # type: dict
    if data.get('is_login') and is_None(request_session.cookies):
        # 获取不同业务配置的登录函数
        login = envs.get('login')
        # 获取自定义登录参数 目前支持 自定义用户'key=login'
        ext = data.get('data').get('ext')
        ext_login = None
        # 存在自定义login时,获取login value用户信息登录
        if 'login' in ext:
            ext_login = ext.get('login')
        response = login(ext_login)  # type: Response
        # 获取不同业务配置的登录cookies,放入session中
        cookies_dict = requests.utils.dict_from_cookiejar(response.cookies)
        # 将字典转为CookieJar：
        cookies = requests.utils.cookiejar_from_dict(cookies_dict, cookiejar=None, overwrite=True)
        # 其中cookie_dict是要转换字典 转换完之后就可以把它赋给cookies 并传入到session中了
        request_session.cookies = cookies
        log.info("获取一次token:{}", cookies)
        token1 = response.headers.get('Set-Cookie')
        cache_v.cache.set('token', token1)


"""全局登录夹具装饰器"""


def fixture_session(env):
    def wra(func):
        def wrapper(*args, **kwargs):
            base_request = args[0]
            base_env = base_request.env_param
            base_params = kwargs['http_data']
            log.info('进入登录前置票判断token:{} cookies:{} 运行环境：{}-{}是否需要登录:{}',
                     cache_v.cache.get('token'), base_request.request_type.session.cookies, base_env['appName'],
                     base_env['runEnv'],
                     base_params['is_login'])
            # log.info('进入登录前置票判断token:{} 运行环境：{}-{}是否需要登录:{}',
            #          cache_v.cache.get('token'), kwargs['param']['appName'], kwargs['param']['runEnv'],
            #          kwargs['param']['is_login'])
            # if cache_v.cache.get('token') is None:
            get_token(base_request, base_params)
            f = func(*args, **kwargs)
            return f

        return wrapper

    return wra


# def moduleName(name):
#     """全局夹具装饰器"""
#
#     def wrapper(*args, **kwargs):
#         log.info('进入登录前置票判断token:{} 运行环境：{}-{}是否需要登录:{}',
#                  cache_v.cache.get('token'), kwargs['appName'], kwargs['runEnv'],
#                  kwargs['is_login'])
#         # if cache_v.cache.get('token') is None:
#         get_token(args[0], **kwargs)
#         func(*args, **kwargs)
#
#     return wrapper


def api_set(path, method, description=None, is_login=True, api_type='auto'):
    if description == "" or description is None:
        description = 'not_set'

    def wra(func):
        def wrapper(*args, **kwargs):
            if len(args) >= 2:
                kwargs['data'] = args[1]
            else:
                kwargs['data'] = {}
            if kwargs == {} or 'ext' not in kwargs:
                kwargs['ext'] = {}

            http_data = {
                'data': {
                    'api_path': path,
                    'method': method,
                    'json': kwargs['data'],
                    'ext': kwargs['ext']
                },
                'description': description,
                'is_login': is_login,
                'api_type': api_type
            }
            kwargs['data'] = http_data
            f = func(args, **kwargs)
            return f

        return wrapper

    return wra
