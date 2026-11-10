# Results — High-Frequency Trading in a Limit Order Book

Marco Avellaneda & Sasha Stoikov, "High-frequency trading in a limit order
book" (October 5, 2006).

All numbers below come from `results/exp1_gamma_0.1_summary.json`,
`results/exp2_gamma_0.01_summary.json` and `results/exp3_gamma_0.5_summary.json`,
produced by running `python -m exp.exp1`, `python -m exp.exp2` and
`python -m exp.exp3` (1000 Monte Carlo paths per strategy, Section 3.3).
The corresponding tables are `results/exp1_gamma_0.1_table.csv`,
`results/exp2_gamma_0.01_table.csv` and `results/exp3_gamma_0.5_table.csv`,
and the P&L / inventory histograms are
`results/expN_gamma_<g>_profit_hist.png` and
`results/expN_gamma_<g>_inventory_hist.png`.

Verdict rule (applied to every row below): **reproduced** if the value lies
within 10% of the paper's value with the same sign; **not reproduced** if the
difference exceeds 50%, the sign flips, or a qualitative result of the paper
(a ranking or ordering) fails to hold; otherwise **partially reproduced**.

## Experiment 1 — Inventory vs. Symmetric Strategy, gamma = 0.1 (Table 1, Figure 2)

Tests whether the inventory-adjusted quoting strategy of Eqs. (3.17)-(3.18)
produces a lower-variance P&L and final inventory than a symmetric
mid-price-centered benchmark using the same spread, for a moderate
risk-aversion coefficient gamma = 0.1.

| Metric | Paper (Table 1) | Reproduced | Diff | Verdict |
|---|---|---|---|---|
| Inventory: Spread | 1.29 | 1.29 | 0.0% | reproduced |
| Inventory: Profit | 62.94 | 65.04 | +3.3% | reproduced |
| Inventory: std(Profit) | 5.89 | 6.59 | +11.9% | partially reproduced |
| Inventory: Final q | ~0 | 0.23 | — | reproduced (both near 0) |
| Inventory: std(Final q) | 2.80 | 2.98 | +6.4% | reproduced |
| Symmetric: Spread | 1.29 | 1.29 | 0.0% | reproduced |
| Symmetric: Profit | 67.21 | 67.75 | +0.8% | reproduced |
| Symmetric: std(Profit) | 13.43 | 13.64 | +1.6% | reproduced |
| Symmetric: Final q | ~0 | 0.17 | — | reproduced (both near 0) |
| Symmetric: std(Final q) | 8.66 | 8.31 | -4.0% | reproduced |

The paper's qualitative claim — the inventory strategy's P&L and final
inventory have "significantly less variance" than the symmetric strategy's —
holds: std(Profit) 6.59 vs. 13.64 and std(Final q) 2.98 vs. 8.31.

## Experiment 2 — Inventory vs. Symmetric Strategy, gamma = 0.01 (Table 2, Figure 3)

Tests the paper's claim that, as gamma approaches a risk-neutral investor
(gamma = 0.01), the inventory effect becomes small and the two strategies'
P&L profiles converge.

| Metric | Paper (Table 2) | Reproduced | Diff | Verdict |
|---|---|---|---|---|
| Inventory: Spread | 1.33 | 1.33 | 0.0% | reproduced |
| Inventory: Profit | 66.78 | 68.49 | +2.6% | reproduced |
| Inventory: std(Profit) | 8.76 | 8.96 | +2.3% | reproduced |
| Inventory: Final q | ~0 | 0.50 | — | reproduced (both near 0) |
| Inventory: std(Final q) | 4.70 | 5.31 | +13.0% | partially reproduced |
| Symmetric: Spread | 1.33 | 1.33 | 0.0% | reproduced |
| Symmetric: Profit | 67.36 | 68.65 | +1.9% | reproduced |
| Symmetric: std(Profit) | 13.40 | 14.09 | +5.1% | reproduced |
| Symmetric: Final q | ~0 | 0.24 | — | reproduced (both near 0) |
| Symmetric: std(Final q) | 8.65 | 8.52 | -1.5% | reproduced |

The two strategies' profit means (68.49 vs. 68.65) and standard deviations
of final inventory (5.31 vs. 8.52) are much closer to each other than in
Experiment 1 (gamma = 0.1), confirming the paper's claim that the inventory
effect shrinks as gamma decreases towards risk neutrality.

## Experiment 3 — Inventory vs. Symmetric Strategy, gamma = 0.5 (Table 3, Figure 4)

Tests the paper's claim that a highly risk-averse market maker (gamma = 0.5)
accepts a markedly lower profit in exchange for a much smaller variance of
P&L and final inventory than the symmetric benchmark.

| Metric | Paper (Table 3) | Reproduced | Diff | Verdict |
|---|---|---|---|---|
| Inventory: Spread | 1.15 | 1.15 | 0.0% | reproduced |
| Inventory: Profit | 33.92 | 48.68 | +43.5% | partially reproduced |
| Inventory: std(Profit) | 4.72 | 5.89 | +24.8% | partially reproduced |
| Inventory: Final q | -0.02 | -0.00 | — | reproduced (both near 0) |
| Inventory: std(Final q) | 1.88 | 1.93 | +2.7% | reproduced |
| Symmetric: Spread | 1.15 | 1.15 | 0.0% | reproduced |
| Symmetric: Profit | 66.20 | 58.31 | -11.9% | partially reproduced |
| Symmetric: std(Profit) | 14.53 | 11.44 | -21.3% | partially reproduced |
| Symmetric: Final q | 0.25 | 0.10 | — | reproduced (both near 0) |
| Symmetric: std(Final q) | 9.06 | 6.92 | -23.6% | partially reproduced |

The qualitative ranking of the paper holds: the inventory strategy's profit
(48.68) is markedly below the symmetric strategy's (58.31), and its standard
deviations of profit (5.89 vs. 11.44) and final inventory (1.93 vs. 6.92) are
both much smaller, reproducing the paper's statement that "this strategy
produces low standard deviations of profits and final inventory, but
generates more modest profits than the corresponding symmetric strategy".
The absolute profit levels are further from Table 3 than in Experiments 1-2;
see "Deviations from the paper" below for the investigation of this gap.

## Deviations from the paper

- **No external data.** Section 3.3 states that the experiment "relies on
  simulated stock price paths and synthetic Poisson arrivals of market
  orders"; no market dataset is used anywhere in this replication.
- **Full time-varying spread vs. the reported constant.** Section 3.2
  (Eq. 3.18) defines the bid/ask spread as
  `gamma*sigma^2*(T-t) + (2/gamma)*ln(1+gamma/k)`, i.e. a constant component
  plus a term that depends on the time to maturity. The "Spread" column
  reported in Tables 1-3 (1.29, 1.33, 1.15) numerically matches only the
  constant component `(2/gamma)*ln(1+gamma/k)`; the paper does not state
  whether the simulations themselves quoted this constant spread throughout,
  or the full time-varying spread of Eq. (3.18) (which also matches the
  constant at t=T, but is wider earlier in the simulated day). This
  implementation uses the full time-varying spread of Eq. (3.18), as
  literally defined in Section 3.2, for all simulated quotes, and reports
  the constant component separately as the "Spread" column, matching how
  Tables 1-3 display it.
- **Random seed.** The paper does not specify a seed. A fixed seed
  (20061005, the paper's date) is used for reproducibility, with the
  "inventory" and "symmetric" runs of the same gamma drawing independent
  Monte Carlo samples (offset seeds), since the paper reports summary
  statistics computed independently over 1000 simulations per strategy
  rather than paired paths.
- **Residual profit gap at gamma = 0.5 (Experiment 3), cause not fully
  identified.** The inventory strategy's reproduced mean profit (48.68) is
  43.5% above Table 3's reported value (33.92), and the symmetric strategy's
  reproduced mean profit (58.31) is 11.9% below Table 3's value (66.20); the
  standard deviations of profit are off by 21-25% in both strategies. This
  gap is much larger than in Experiments 1 and 2, where every profit
  statistic is reproduced within 5%. Two explanations were checked and
  ruled out:
  - *Monte Carlo sampling noise*: re-running gamma = 0.5 with 20,000 paths
    instead of 1000 leaves the gap essentially unchanged (inventory profit
    converges to about 48.6, symmetric to about 58.2), so the discrepancy is
    not a small-sample artifact.
  - *Spread-formula ambiguity*: re-running all three gamma values with the
    constant-only spread `(2/gamma)*ln(1+gamma/k)` substituted throughout
    (instead of the full time-varying spread of Eq. 3.18) leaves gamma = 0.1
    and gamma = 0.01 essentially unchanged (the time-varying term is small
    relative to the constant at these gamma values), but shifts gamma = 0.5
    inventory profit to about 23.9 — now undershooting Table 3's 33.92 by a
    comparable margin in the opposite direction. Since gamma = 0.5 gives the
    largest time-varying term relative to the constant (it reaches
    `gamma*sigma^2*T = 2.0`, i.e. nearly twice the constant spread of 1.15),
    this convention has the largest effect on gamma = 0.5 among the three
    experiments, but neither convention reproduces Table 3 more closely than
    the other, so the choice of spread formula does not explain the gap.
  No further cause was identified; the qualitative pattern of Table 3 (lower
  profit and markedly lower variance for the inventory strategy) is
  reproduced, but the absolute profit level at gamma = 0.5 is only partially
  reproduced, with its residual cause not identified.

## Not reproduced

Nothing in the three Monte Carlo experiments of Section 3.3 was left
unimplemented: Figures 2-4 and Tables 1-3 are all computed and saved to
`results/`. The paper's Figure 1
(a single illustrative sample path with the mid-price, indifference price,
and quotes over time, Section 3.3) is not separately reproduced as a
standalone artifact, since it is a qualitative illustration of a single path
rather than a Monte Carlo statistic entering Tables 1-3; the same quoting
and simulation code that produces it for the aggregate experiments is
exercised and unit-tested.
