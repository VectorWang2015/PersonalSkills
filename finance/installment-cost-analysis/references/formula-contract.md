# Installment annualized-cost formula contract

## Sign and cash-flow convention

- Borrower receives money: positive.
- Borrower pays money or fees: negative.
- Upfront fees paid on disbursement date are included as a same-date negative cash flow, reducing net proceeds.
- Aggregate flows on the same date before solving.
- A conventional loan must have one sign change after aggregation; otherwise IRR can have multiple or no roots and this script stops.

## Primary calculation

For dated flows `(date_i, cash_i)`, solve the effective annual rate `r > -1`:

```text
Σ cash_i / (1 + r)^((date_i - date_0).days / day_count_basis) = 0
```

The script defaults to actual/365. Report the basis.

For equally spaced periods, solve periodic IRR `q`:

```text
Σ cash_t / (1 + q)^t = 0
```

Then:

```text
nominal annual rate = q × periods_per_year
effective annual rate = (1 + q)^periods_per_year - 1
```

Nominal and effective are different outputs and must not share one label.
The script checks that actual date intervals are close to the declared frequency; irregular schedules receive XIRR only.

## Source-book approximation

The book derives:

```text
simple annualized approximation = 24 × x × y / (x + 1)
```

where `x` is the number of monthly periods and `y` is the fee charged each period as a fraction of original principal.

Use only if all hold:

- monthly periods;
- equal principal repayment;
- the same per-period fee on original principal;
- no upfront or other directly related cost;
- no early repayment or balloon payment;
- the user accepts a simple average-balance approximation.

For the book's `12000`, 12 periods, `0.66%` per period example:

- book simple approximation: about `14.6215%`;
- periodic IRR nominal annualization: about `14.3106%`;
- periodic IRR effective annualization: about `15.2876%`.

These are not interchangeable. Exact dated XIRR also varies with actual dates.

## Input JSON

```json
{
  "perspective": "borrower",
  "all_direct_loan_costs_included": true,
  "day_count_basis": 365,
  "regular_periodic": true,
  "periods_per_year": 12,
  "cashflows": [
    {"date": "2026-01-01", "amount": 12000},
    {"date": "2026-02-01", "amount": -1079.2}
  ],
  "book_approximation": {
    "periods": 12,
    "fee_rate_per_period": 0.0066
  }
}
```

Include all remaining payments; the shortened array above illustrates fields only.

## Stop conditions

- `all_direct_loan_costs_included` is not true;
- actual net proceeds or any payment amount/date is missing;
- cash flows are non-conventional and can have multiple roots;
- the user asks to apply the book shortcut to irregular or changing payments;
- early-settlement costs materially change the requested scenario but are unavailable.
