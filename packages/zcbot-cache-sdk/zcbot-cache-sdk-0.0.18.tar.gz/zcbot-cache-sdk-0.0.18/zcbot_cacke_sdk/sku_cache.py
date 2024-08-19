import logging
from pymongo import MongoClient
from redis import Redis
from pymongo import UpdateOne
from typing import List
from zcbot_cacke_sdk.constant import ZCBOT_CACHE_MONGO_URL, ZCBOT_CACHE_MONGO_DATABASE, ZCBOT_CACHE_REDIS_URL
from zcbot_cacke_sdk.model import SkuModel


class SkuCache(object):
    logger = logging.getLogger(__name__)

    def __init__(self, mongo_url: str = None, mongo_database: str = None, redis_url: str = None):
        self.batch_size = 5000

        self.mongo_url = mongo_url or ZCBOT_CACHE_MONGO_URL
        self.mongo_database = mongo_database or ZCBOT_CACHE_MONGO_DATABASE
        self.mongo_client = MongoClient(self.mongo_url)
        self.mongo_sku_collection = self.mongo_client.get_database(self.mongo_database).get_collection('cache_sku_pool')
        self.mongo_update_bulk = []

        self.redis_url = redis_url or ZCBOT_CACHE_REDIS_URL
        self.rds_client = Redis.from_url(url=self.redis_url, decode_responses=True)
        self.rds_cache_sku_key = 'zcbot:cache:sku'
        self.rds_update_bulk = []

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
                pipe.sismember(self.rds_cache_sku_key, _id)
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
            rs = self.mongo_sku_collection.find(
                {'_id': {'$in': ids}}
            )
            for document in rs:
                documents.append(document)
            return documents
        except Exception as e:
            self.logger.error(e)

    def batch_save(self, sku_list: List[SkuModel]):
        for sku in sku_list:
            self.save(sku)

        self.flush()

    def save(self, sku: SkuModel):
        """
        写入缓存数据
        将商品数据写入缓存（mongo+redis）
        """
        try:
            # 基本要求
            if not sku or not sku.sn and not sku.skuName:
                return
            _data = sku.dict(exclude_unset=True)
            _data['_id'] = sku.sn
            self.mongo_update_bulk.append(UpdateOne(
                filter={'_id': sku.sn, 'updateTime': {'$gt': sku.updateTime}},
                update={'$set': _data},
                upsert=True
            ))
            self.rds_update_bulk.append(sku.sn)
            # 缓冲保存
            if self.mongo_update_bulk and len(self.mongo_update_bulk) >= self.batch_size:
                # Mongo保存操作
                self.mongo_sku_collection.bulk_write(self.mongo_update_bulk)
                self.logger.info(f'数据写入: {len(self.mongo_sku_collection)}')
                self.mongo_update_bulk.clear()
                # Redis插入操作
                self.rds_client.sadd(self.rds_cache_sku_key, *self.rds_update_bulk)
                self.logger.info(f'缓存写入: {len(self.mongo_sku_collection)}')
                self.rds_update_bulk.clear()
        except Exception as e:
            self.logger.error(e)

    def flush(self):
        # flush
        if self.mongo_update_bulk:
            self.mongo_sku_collection.bulk_write(self.mongo_update_bulk)
            self.logger.info(f'flush数据写入: {len(self.mongo_sku_collection)}')
            self.mongo_update_bulk.clear()
            # Redis插入操作
            self.rds_client.sadd(self.rds_cache_sku_key, *self.rds_update_bulk)
            self.logger.info(f'flush缓存写入: {len(self.mongo_sku_collection)}')
            self.rds_update_bulk.clear()
