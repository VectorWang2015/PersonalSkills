---
name: healthcare-valuation
description: |
  用户需要分析医疗机构估值或基本面时使用。触发器：用户说"分析这家医院/医疗公司""爱尔眼科怎么估值""医疗机构估值用什么方法"。不适用于：制药/器械/医保等非医疗机构分析。
source_book: 《医疗行业估值》 郑华 & 涂宏钢 (2020)
tags: [healthcare, hospital, clinic, valuation, DCF, medical]
---

# 医疗机构估值分析

## 定位

聚合 skill，医疗机构估值分析的唯一入口。按机构类型分发 9 个原子 skill。

## 执行流水线

```
第一层：行业与估值基础
├─ 医疗服务供需与竞争 (atomic/yi-liao-gong-xu-jing-zheng/SKILL.md)
├─ 估值方法选择 (atomic/valuation-method-choice/SKILL.md)
└─ 资本成本估算 (atomic/medical-capital-cost/SKILL.md)

第二层：核心估值执行
├─ 医院DCF估值框架 (atomic/yi-liao-dcf-valuation/SKILL.md)
├─ 医院财务四层分析 (atomic/si-ceng-cai-wu-fen-xi/SKILL.md)
└─ 医疗集团分部估值 (atomic/medical-group-valuation/SKILL.md)

第三层：专项估值
├─ 门诊/诊所估值 (atomic/outpatient-valuation/SKILL.md)
├─ 长期照护机构估值 (atomic/long-term-care-valuation/SKILL.md)
└─ 初创医疗机构估值 (atomic/startup-valuation/SKILL.md)
```

## 保存分析结果

分析完成后主动询问用户是否保存为 Markdown 文件到 `reports/<报告期>/`。
