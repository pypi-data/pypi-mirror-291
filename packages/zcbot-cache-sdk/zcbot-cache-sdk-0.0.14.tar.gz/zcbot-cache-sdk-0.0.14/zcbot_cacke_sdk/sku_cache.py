import logging
from pymongo import MongoClient
from redis import Redis
from pymongo import UpdateOne
from typing import List
from zcbot_cacke_sdk.constant import ZCBOT_CACHE_MONGO_URL, ZCBOT_CACHE_MONGO_DATABASE, ZCBOT_CACHE_REDIS_URL
from zcbot_cacke_sdk.utils import singleton
from zcbot_cacke_sdk.model import SkuModel


@singleton
class SkuCache(object):
    logger = logging.getLogger(__name__)
    cache_sku_key = 'zcbot:cache:sku'

    def __init__(self, mongo_url: str = None, mongo_database: str = None, redis_url: str = None):
        self.mongo_url = mongo_url or ZCBOT_CACHE_MONGO_URL
        self.mongo_database = mongo_database or ZCBOT_CACHE_MONGO_DATABASE
        self.sku_collection = 'cache_sku_pool'
        self.mongo_client = MongoClient(self.mongo_url)
        self.redis_url = redis_url or ZCBOT_CACHE_REDIS_URL
        self.rds_client = Redis.from_url(url=self.redis_url, decode_responses=True)

    def contains(self, ids: List[str]):
        """
        判断是否存在
        根据id列表判断商品池是否包含
        """
        # 使用pipeline来优化多个SISMEMBER命令的执行
        with self.rds_client.pipeline() as pipe:
            # 创建一个与id列表大小相同的列表，用于存储结果
            results = [None] * len(ids)
            # 构建pipeline中的命令
            for index, _id in enumerate(ids):
                pipe.sismember(self.cache_sku_key, _id)
            # 执行pipeline中的所有命令，并获取结果
            for index, result in enumerate(pipe.execute()):
                results[index] = result

        # 根据结果将存在的ID和不存在的ID分别放入两个列表中
        existing_ids = [_id for index, _id in enumerate(ids) if results[index]]
        non_existing_ids = [_id for index, _id in enumerate(ids) if not results[index]]

        return existing_ids, non_existing_ids

    def get(self, ids: List[str]):
        """
        获取缓存数据
        根据id列表获取缓存数据
        """
        try:
            documents = []
            rs = self.mongo_client.get_database(self.mongo_database).get_collection(self.sku_collection).find(
                {'_id': {'$in': ids}}
            )
            for document in rs:
                documents.append(document)
            return documents
        except Exception as e:
            self.logger.error(e)

    def save(self, sku_list: List[SkuModel], sku_ids: List[str] = None):
        """
        写入缓存数据
        将商品数据写入缓存（mongo+redis）
        """
        try:
            update_bulk = []
            if not sku_list:
                raise ValueError("商品数据不能为空")
            if not sku_ids:
                sku_ids = [sku.sn for sku in sku_list if sku.sn]
            if not sku_ids or len(sku_ids) != len(sku_list):
                raise ValueError("商品数据与有效编码编码数量不一致")
            # MongoDB插入操作
            for sku in sku_list:
                _data = sku.dict()
                _data['_id'] = sku.sn
                update_bulk.append(UpdateOne(
                    filter={'_id': sku.sn},
                    update={'$set': _data},
                    upsert=True
                ))
            if update_bulk:
                collection = self.mongo_client.get_database(self.mongo_database).get_collection(self.sku_collection)
                collection.bulk_write(update_bulk)
            # Redis插入操作
            self.rds_client.sadd(self.cache_sku_key, *sku_ids)
        except Exception as e:
            self.logger.error(e)
