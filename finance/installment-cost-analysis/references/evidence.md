# Source evidence and revision lineage

## Original-book evidence

Source: 价投谷子地《看透银行：投资银行股从入门到精通》，第2章2.4“信用卡分期费率探讨”。

- TXT lines 287-288: the 12,000 / 12-period / 79.2 fee example and the time-value problem.
- TXT lines 294-302: variables `L`, `x`, `y` and derivation of `24xy/(x+1)`.
- TXT lines 303-309: historical fee examples and the link to bank revenue classification.
- EPUB: `text/part0007.html#cha2_2_1_4`.

Source fingerprints and rights notes are in [source-manifest.json](source-manifest.json).

## Legacy capability retained

Alias: `legacy.installment-apr-calculation`.

Retained:

- clear explanation that fees charged on original principal while principal amortizes understate the apparent cost;
- book formula and worked example;
- boundaries for balloon, interest-only, changing-fee, and early-repayment products.

Removed or revised:

- “true APR” label for the book shortcut;
- fixed comparisons with historical mortgage, consumer-loan, money-market, or penalty rates;
- `APR > 12%` as automatically expensive and `<6%` as suspicious;
- claim that the shortcut approximately equals IRR for all standard products;
- claim that product APR is required to determine a bank's accounting classification.

## Revision-2 extension

The IRR/XIRR, complete-cost, actual-net-proceeds, sign, date, multiple-root, and missing-input rules are operational extensions supported by the current People's Bank of China disclosure rule. They are not attributed to the book author.

## Independent evaluation

- Round 1 tested regular monthly cash flows, actual-date XIRR, upfront fees, irregular payments, missing costs, balloon repayment, bank-report routing, and borrowing-advice boundaries. Candidate and legacy outputs tied at 97/100; no-skill scored 96/100.
- Round 2 tested a non-conventional cash flow with two valid annual roots (10% and 20%), a fee-complete product comparison, early-settlement uncertainty, and shortcut misuse. All three arms scored 100/100.
- The released skill additionally provides a deterministic calculator with seven passing tests, including rejection of multiple sign changes and incomplete all-cost assertions. This reproducible tool is the incremental utility used to break the behavioral tie; no claim is made that the prose response alone outperformed every baseline.

Full anonymous outputs and judging records are archived under `books/kan-tou-yin-hang/.book2skill/refresh-2026-09-03/` outside the runtime skill.
