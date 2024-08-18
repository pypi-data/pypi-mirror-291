import os

ZCBOT_CACHE_MONGO_URL = os.getenv('ZCBOT_CACHE_MONGO_URL') or 'mongodb://cache_read:cache_read_zsodata@zcbot-inner.mongodb.rds.aliyuncs.com:3717'
ZCBOT_CACHE_MONGO_DATABASE = os.getenv('ZCBOT_CACHE_MONGO_DATABASE') or 'zcbot_caches'

ZCBOT_CACHE_REDIS_URL = os.getenv('ZCBOT_CACHE_REDIS_URL') or 'redis://:Dangerous!@redis_host:6379/8'
