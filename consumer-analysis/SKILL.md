---
name: consumer-analysis
description: |
  用户需要分析消费行业公司基本面时使用。触发器：用户说"分析这家消费品公司""帮我看看茅台的竞争力""消费股怎么分析"。不适用于：非消费行业公司分析、纯技术面分析。
source_book: 《吴劲草讲消费行业》 吴劲草 (2022)
tags: [consumer, brand, channel, supply-chain, fundamental-analysis]
---

# 消费行业公司分析

## 定位

聚合 skill，消费行业公司基本面分析的唯一入口。按品牌-渠道-供应链三角框架编排 9 个原子 skill。

## 执行流水线

```
第一层：分类与赛道
├─ 品牌-渠道-供应链三角分类 (atomic/ing-pai-qu-dao-ong-ying-lian-san-jia/SKILL.md)
└─ 行业赛道分析 (atomic/ing-hang-ye-sai-dao-fen-xi/SKILL.md)

第二层：核心竞争力
├─ 品牌分级与品牌力 (atomic/ping-pai-fen-ji/SKILL.md)
├─ 品牌计分板 (atomic/ing-pai-ji-fen-ban/SKILL.md)
├─ 渠道变革分析 (atomic/u-dao-bian-ge-fen-xi/SKILL.md)
└─ 供应链分析 (atomic/ong-ying-lian-fen-xi/SKILL.md)

第三层：增长与财务
├─ 消费品增长三逻辑 (atomic/ing-zeng-zhan-san-luo-ji/SKILL.md)
└─ 消费品公司财务分析 (atomic/ai-wu-ong-si-cai-wu-fen-xi/SKILL.md)

第四层：估值
└─ 消费品企业估值方法 (atomic/iao-fei-pin-qi-ye-gu-zhi/SKILL.md)
```

## 保存分析结果

分析完成后主动询问用户是否保存为 Markdown 文件到 `books/xiao-fei-pin/analyses/`。
