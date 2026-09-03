# Revision 2 发布评测

截至 2026-09-03，隔离匿名聚合评测解盲结果为：

| 评测臂 | 分数 |
|---|---:|
| revision 2 candidate | 99 |
| old skill | 94 |
| no skill | 92.5 |

该结果支持 `consumer-analysis` 根入口以 `active` 状态发布。分数只适用于完整聚合 skill，不是六个内部 reference 的逐项分数，也不改变它们当前未声明逐卡发布状态的边界。可见 `test-prompts.json` 仍是开发回归集；未来 revision 必须另用未泄漏样例评测。
