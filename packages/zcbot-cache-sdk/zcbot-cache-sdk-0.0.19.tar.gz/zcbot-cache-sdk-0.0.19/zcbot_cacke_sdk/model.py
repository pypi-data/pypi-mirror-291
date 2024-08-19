from typing import Dict, List, Any, Union
from pydantic import BaseModel, Field

from .utils import current_timestamp10


class BaseCacheData(BaseModel):
    """
    通用缓存基础数据模型
    """
    cacheTime: int = Field(default_factory=current_timestamp10, description="缓存写入时间（并非数据更新时间）")
    cacheFrom: Union[str, Dict] = Field(default_factory=current_timestamp10, description="缓存来源")


class SkuModel(BaseCacheData):
    """
    缓存商品模型
    """
    sn: str = Field(None, description="唯一编号")
    url: str = Field(None, description="电商链接")
    ecSkuId: str = Field(None, description="电商编号")
    platCode: str = Field(None, description="电商平台编号")
    platName: str = Field(None, description="电商平台名称")
    skuName: str = Field(None, description="商品名称")
    salePrice: str = Field(None, description="销售价")
    promPrice: str = Field(None, description="促销价")
    originPrice: str = Field(None, description="市场价")
    cat1Id: str = Field(None, description="一级分类编号")
    cat1Name: str = Field(None, description="一级分类名称")
    cat2Id: str = Field(None, description="二级分类编号")
    cat2Name: str = Field(None, description="二级分类名称")
    cat3Id: str = Field(None, description="三级分类编号")
    cat3Name: str = Field(None, description="三级分类名称")
    shopId: str = Field(None, description="店铺编号")
    shopName: str = Field(None, description="店铺名称")
    shopType: str = Field(None, description="店铺类型")
    isSelf: str = Field(None, description="是否自营")
    brandId: str = Field(None, description="品牌Id")
    brandName: str = Field(None, description="品牌名称，来自采集")
    model: str = Field(None, description="型号")
    spec: str = Field(None, description="规格")
    color: str = Field(None, description="颜色")
    unit: str = Field(None, description="单位")
    soldCount: int = Field(None, description="销量")
    commentCount: str = Field(None, description="评论数")
    commentGoodRate: str = Field(None, description="好评率")
    currentCommentCount: str = Field(None, description="当前商品评论数")
    currentCommentGoodRate: str = Field(None, description="当前商品好评率")
    coverImgUrl: str = Field(None, description="首图链接")
    mainImages: List[str] = Field([], description="商品主图")
    detailImages: List[str] = Field(None, description="详情图")
    skuOptions: Union[Dict] = Field(None, description="商品选项")
    skuAttrs: Dict[str, Any] = Field(None, description="小字段")
    packAttrs: Union[str, Dict] = Field(None, description="包装参数")
    tags: Union[str, Dict] = Field(None, description="商品标签（如：包邮、新品、厂商配送等）")

    status: str = Field(None, description="商品状态")
    statusText: str = Field(None, description="商品状态")
    updateTime: int = Field(None, description="数据更新时间")

