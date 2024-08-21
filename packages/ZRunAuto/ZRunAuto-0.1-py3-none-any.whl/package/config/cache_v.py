# 创建缓存对象
import os
import sys

from cacheout import Cache

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)





cache = Cache()
