# Mic
Mic

###功能特性
* 响应式
* 开源
* 集成社交媒体组件
* 无限分类
* 无限商品
* 无限厂家
* 自定义样式
* 多语言支持
* 多货币支持
* 评论商品
* 商品评分
* 下载商品
* 自动调整图片大小
* 多税率支持
* 相关商品推荐
* SEO（搜索引擎优化）
* 销售报表
* 心愿单
* 商品建议
* 商品分组
* 地址簿
* 用户属性（卖家&买家）
* 商品条形码
* 后台管理面板
* 用户订单列表（标记订单状态）
* 商品价格
* 虚拟商品
* 免费商品模块
* 用户积分
* 虚拟商品交付
* 动态商品规格
* 公司简介
* 购物车
* 用户喜好控制
* 用户通知
* 公司信息CMS
* 动态面包屑


###使用Flask-Migrate

在命令提示行中
```
python manager.py db init # 来创建迁移仓库,

python manager.py db migrate -m "initial migration" # 创建迁移脚本, 在数据库结构有变动后创建迁移脚本

python manager.py db upgrade # 更新数据库
```


###Flask-Uploads
API Doc: http://pythonhosted.org/Flask-Uploads/