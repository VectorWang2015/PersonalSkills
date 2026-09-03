# v3 发布评测记录

截至 2026-09-03，独立匿名聚合评测解盲结果为：

| 评测臂 | 分数 |
|---|---:|
| merged v3 candidate | 98 |
| old skill | 97 |
| no skill | 96.5 |

该结果支持 `financial-statement-analysis` v3 根入口以 `active` 状态发布，包级行为评测门已通过。

分数只适用于完整聚合 skill，不能拆分给七项内部能力；七项内部能力因未做逐卡独立评测继续保持 `draft`。可见 `test-prompts.json` 仍是开发回归集，未来 revision 需要新的隔离样例。
