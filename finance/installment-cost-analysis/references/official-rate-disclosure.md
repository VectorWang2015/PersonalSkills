# Official annualized-rate disclosure rule

`verified_as_of: 2026-09-03`

Primary source: [中国人民银行公告〔2021〕第3号](https://xining.pbc.gov.cn/goutongjiaoliu/113456/113469/2025092212551432728/index.html)，成文日期2021年3月12日。

The announcement requires loan institutions to display annualized rates prominently and states:

- annualized rate uses all loan costs charged to the borrower and the principal actually occupied;
- loan costs include interest and directly related fees;
- installment repayment uses the remaining principal after each repayment;
- compound or simple calculation may be shown;
- compound calculation is the internal-rate-of-return method;
- a simple calculation must be identified as simple.

The official example with a 100,000 loan, a 1,000 upfront service fee, and twelve monthly payments of 8,833.3 reports about 12.80% under simple annualization and 13.58% using IRR. This demonstrates why upfront costs and compound treatment matter.

## Runtime use

- Use the actual loan offer and contract, not historical market-rate comparisons.
- Include all directly related costs and actual net proceeds.
- Use IRR/XIRR as the primary economic comparison; if showing simple annualization, label it.
- A compliance conclusion requires checking whether this announcement or related rules have changed since the verification date.
