# 维权案例数据库

## 一、数据库说明
本数据库收集整理快手平台发生的典型维权案例，所有案例均经过核实，并保留相关证据材料。

## 二、数据库结构
### 2.1 案例基础信息表 (cases)
- case_id: 案件编号（主键）
- title: 案件标题
- type: 案件类型
- platform: 发生平台
- amount: 涉案金额
- victim_count: 受害人数
- status: 案件状态
- punishment_result: 处罚结果
- created_at: 创建时间
- updated_at: 更新时间

### 2.2 证据材料表 (evidence)
- evidence_id: 证据编号（主键）
- case_id: 关联案件编号
- type: 证据类型
- file_path: 文件路径
- file_hash: 文件哈希值
- upload_time: 上传时间
- description: 证据描述

### 2.3 案件进展表 (case_progress)
- progress_id: 进展编号（主键）
- case_id: 关联案件编号
- stage: 进展阶段
- description: 进展描述
- result: 处理结果
- date: 进展时间
- operator: 操作人

### 2.4 焦点新闻表 (case_news)
- news_id: 新闻编号（主键）
- case_id: 关联案件编号
- title: 新闻标题
- source: 新闻来源
- url: 新闻链接
- publish_date: 发布时间
- summary: 新闻摘要
- importance: 重要程度

### 2.5 外部链接表 (external_links)
- link_id: 链接编号（主键）
- case_id: 关联案件编号
- title: 链接标题
- url: 链接地址
- type: 链接类型（新闻/判决书等）
- status: 链接状态
- archive_url: 存档链接（使用 Internet Archive 存档）
- last_check: 最后检查时间

## 三、相关链接资源

### 3.1 官方监管链接
- [国家市场监督管理总局](http://www.samr.gov.cn)
- [中国消费者协会](https://www.cca.org.cn)
- [北京市市场监督管理局](http://scjgj.beijing.gov.cn)
- [全国企业信用信息公示系统](https://www.gsxt.gov.cn)

### 3.2 法律文书链接
- [中国裁判文书网](https://wenshu.court.gov.cn)
- [北京法院网上诉讼服务](https://ssfw.bjcourt.gov.cn)
- [最高人民法院公告](https://www.court.gov.cn/fabu-gongao.html)

### 3.3 新闻媒体链接
- [央视网 - 315晚会](https://315.cctv.com)
- [新华网 - 消费维权](http://www.xinhuanet.com/fortune/315.htm)
- [人民网 - 舆情监测](http://yuqing.people.com.cn)
- [中国网 - 消费频道](http://consumption.china.com.cn)

### 3.4 平台相关链接
- [快手平台服务协议](https://www.kuaishou.com/about/policy)
- [快手平台商家规范](https://business.kuaishou.com/policy)
- [快手平台投诉通道](https://www.kuaishou.com/complain)
- [快手电商平台管理规范](https://business.kuaishou.com/business-guide)

### 3.5 存档服务
- [Internet Archive](https://web.archive.org)
- [Archive Today](https://archive.today)
- [中国数字时代](https://chinadigitaltimes.net)

## 四、案例分类
### 4.1 按产品类型
- 保健品类
- 食品类
- 药品类
- 化妆品类
- 医疗器械类
- 农产品类

### 4.2 按违法类型
- 虚假宣传
- 违禁产品
- 假冒伪劣
- 价格欺诈
- 虚假发货

## 五、数据维护
### 5.1 数据更新机制
- 案例信息实时更新
- 证据材料定期补充
- 进展情况及时跟踪
- 新闻报道动态采集
- 外部链接定期检查

### 5.2 数据质量控制
- 案例信息多源核实
- 证据材料完整性校验
- 文件哈希值验证
- 外部链接有效性检查
- 数据定期审核

### 5.3 数据安全保护
- 数据库定期备份
- 访问权限控制
- 操作日志记录
- 敏感信息加密
- 数据完整性校验

## 六、使用说明
### 6.1 数据访问
- 基础信息查询
- 证据材料下载
- 进展记录追踪
- 新闻报道关联
- 外部链接访问

### 6.2 数据导出
- 案例信息导出
- 证据材料打包
- 进展记录汇总
- 新闻报道集合
- 完整案例报告

### 6.3 数据分析
- 案例类型统计
- 涉案金额分析
- 处理效率评估
- 平台分布分析
- 趋势预测研究