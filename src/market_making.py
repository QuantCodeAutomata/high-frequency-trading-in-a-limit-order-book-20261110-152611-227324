"""Closed-form quoting formulas from Avellaneda & Stoikov (2006).

Implements the approximate indifference (reservation) price and bid/ask
spread obtained from the first-order asymptotic expansion in the inventory
q, Section 3.2 ("Asymptotic expansion in q"), Equations (3.17)-(3.18). These
drive both the "inventory" strategy and the benchmark "symmetric" strategy
of Section 3.3, which uses the same spread centered on the mid-price.

No third-party quantitative library implements these paper-specific
closed-form expressions, so they are implemented directly from the equations
(custom implementation, paper Eqs. 3.17-3.18).
"""
from __future__ import annotations

import numpy as np

ArrayLike = np.ndarray | float


def reservation_price(
    mid_price: ArrayLike, inventory: ArrayLike, gamma: float, sigma: float, time_to_maturity: ArrayLike
) -> ArrayLike:
    """Indifference (reservation) price r(s,t) = s - q*gamma*sigma^2*(T-t), Eq. (3.17)."""
    return mid_price - inventory * gamma * (sigma ** 2) * time_to_maturity


def spread_constant(gamma: float, k: float) -> float:
    """Constant component of the optimal spread, (2/gamma)*ln(1+gamma/k), Eq. (3.18).

    This is the value reported as "Spread" in Tables 1-3 of Section 3.3: the
    paper's reported spreads (1.29 for gamma=0.1, 1.33 for gamma=0.01, 1.15
    for gamma=0.5) match this constant component rather than the full
    time-varying spread gamma*sigma^2*(T-t) + (2/gamma)*ln(1+gamma/k), which
    also includes the inventory-sensitivity term that vanishes at t=T.
    """
    if gamma <= 0 or k <= 0:
        raise ValueError("gamma and k must be positive")
    return (2.0 / gamma) * np.log(1.0 + gamma / k)


def spread_time_varying(time_to_maturity: ArrayLike, gamma: float, sigma: float, k: float) -> ArrayLike:
    """Full bid/ask spread delta_a + delta_b, Eq. (3.18).

    delta_a + delta_b = gamma*sigma^2*(T-t) + (2/gamma)*ln(1+gamma/k)
    """
    return gamma * (sigma ** 2) * time_to_maturity + spread_constant(gamma, k)


def quotes(
    strategy: str,
    mid_price: ArrayLike,
    inventory: ArrayLike,
    time_to_maturity: ArrayLike,
    gamma: float,
    sigma: float,
    k: float,
):
    """Ask and bid quotes for the 'inventory' or 'symmetric' strategy.

    Both strategies use the identical spread of Eq. (3.18); they differ only
    in what the spread is centered on: the reservation price r(s,t) for the
    "inventory" strategy, or the mid-price s for the "symmetric" strategy
    (Section 3.3).
    """
    spread = spread_time_varying(time_to_maturity, gamma, sigma, k)
    if strategy == "inventory":
        center = reservation_price(mid_price, inventory, gamma, sigma, time_to_maturity)
    elif strategy == "symmetric":
        center = mid_price
    else:
        raise ValueError(f"unknown strategy: {strategy!r}, expected 'inventory' or 'symmetric'")
    ask_price = center + spread / 2.0
    bid_price = center - spread / 2.0
    return ask_price, bid_price
