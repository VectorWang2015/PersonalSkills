# 医疗机构类型路由

`cap.medical-institution-valuation.institution-specific-adjustments` · revision 2

只读取与目标实体或分部匹配的文件。混合集团先读 `medical-group.md`，再按每个分部加载其他类型。

| 类型 | 读取 | 决定性变量 |
|---|---|---|
| 医院或专科医院 | [hospital.md](hospital.md) | 科室/患者/支付、质量与效率、单一用途资产、维持和合规资本支出 |
| 成熟门诊、诊所、医生集团、日间手术中心 | [outpatient-day-surgery.md](outpatient-day-surgery.md) | 医生报酬、患者与商誉可转移性、专科/手术量、支付和应急支持 |
| 护理院、住宿型长期医疗照护机构 | [long-term-care.md](long-term-care.md) | 可用/占用床日、护理等级、支付/补贴、人员标准和医院合作 |
| 多实体医疗集团、剥离或分支估值 | [medical-group.md](medical-group.md) | 所有权/控制/合同、母体支持、担保、内部交易、独立与集团价值 |

初创或尚未形成稳定经营的数据不足机构，先判断是否应使用 [`../startup-round-valuation.md`](../startup-round-valuation.md)。名称相似不等于法律类型相同；牌照、登记、医保和税务属性必须按基准日官方材料确认。

## 共同执行

1. 确认机构类型、实体和交易范围。
2. 运行对应专属尽调并记录来源、`as_of` 和可转移性。
3. 将每个类型变量映射到患者量、价格/支付、成本、资本支出、营运资本、折现率或权益桥。
4. 混合业务分部建模，抵销内部交易，独立价值与协同价值分开。
5. 当前规则不能核验时只做情景或停止。

共同经营预测见 [`../operating-driver-forecast.md`](../operating-driver-forecast.md)，正常化见 [`../financial-normalization.md`](../financial-normalization.md)。
