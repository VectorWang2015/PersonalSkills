# v7 发布评测记录

截至 2026-09-03，独立匿名聚合评测解盲结果为：

| 评测臂 | 分数 |
|---|---:|
| v7 candidate | 97.5 |
| no skill | 96.5 |
| old skill | 96 |

该结果支持 `insurance-comprehensive-analysis` v7 根入口以 `active` 状态发布，包级 `fresh-v7-holdout` 门已通过。

该结果是完整 skill 的聚合分数，不是七项内部能力的逐卡分数。七项内部能力继续保持 `draft`，逐卡增益仍需单独的定向评测或消融。可见 `test-prompts.json` 仍是开发回归集，未来 revision 需使用新的隔离留出。
