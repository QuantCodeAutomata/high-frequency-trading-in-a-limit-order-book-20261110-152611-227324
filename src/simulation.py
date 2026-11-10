"""Monte Carlo simulation of the market-making strategies (Section 3.3).

Simulates ``n_paths`` independent mid-price / order-flow scenarios and
tracks, for each strategy, the market maker's cash wealth and inventory,
following the procedure stated in Section 3.3: "at time t, the agent's
quotes delta^a and delta^b are computed, given the state variables. At time
t + dt, the state variables are updated." Quotes at step t are therefore
computed only from the state at t (mid-price and inventory), before the
mid-price is advanced to t + dt, which rules out look-ahead.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from data.generate_synthetic import generate_order_arrival_uniforms, generate_price_shocks
from src.market_making import quotes, spread_constant


@dataclass
class SimulationResult:
    """Outcome of one Monte Carlo batch for a single strategy and gamma."""

    strategy: str
    gamma: float
    profit: np.ndarray            # shape (n_paths,): final P&L, X_T + q_T * s_T
    final_inventory: np.ndarray   # shape (n_paths,): final inventory q_T
    final_mid_price: np.ndarray   # shape (n_paths,): final mid-price s_T
    spread: float                 # constant spread component, Eq. (3.18) / Tables 1-3


def simulate_strategy(
    strategy: str,
    gamma: float,
    sigma: float,
    k: float,
    A: float,
    T: float,
    dt: float,
    s0: float,
    q0: float,
    n_paths: int,
    seed: int,
) -> SimulationResult:
    """Run ``n_paths`` Monte Carlo simulations of one quoting strategy.

    Parameters follow the notation of Section 3.3: ``s0`` initial mid-price,
    ``T`` trading horizon, ``sigma`` volatility, ``dt`` time step, ``q0``
    initial inventory, ``gamma`` risk aversion, ``k`` and ``A`` order-arrival
    intensity parameters (lambda(delta) = A * exp(-k * delta)).
    """
    if strategy not in ("inventory", "symmetric"):
        raise ValueError(f"unknown strategy: {strategy!r}")
    if dt <= 0 or T <= 0:
        raise ValueError("dt and T must be positive")
    if n_paths <= 0:
        raise ValueError("n_paths must be positive")

    n_steps = int(round(T / dt))
    assert abs(n_steps * dt - T) < 1e-9, "T must be an integer multiple of dt"

    rng = np.random.default_rng(seed)
    price_shocks = generate_price_shocks(n_steps, n_paths, sigma, dt, rng)
    u_ask, u_bid = generate_order_arrival_uniforms(n_steps, n_paths, rng)

    mid_price = np.full(n_paths, s0, dtype=float)
    inventory = np.full(n_paths, float(q0), dtype=float)
    cash = np.zeros(n_paths, dtype=float)

    for step in range(n_steps):
        t = step * dt
        tau = T - t  # time to maturity: quotes at t use only the state already realized at t

        ask_price, bid_price = quotes(strategy, mid_price, inventory, tau, gamma, sigma, k)

        # Distance of each quote to the mid-price drives the Poisson intensity
        # lambda(delta) = A * exp(-k * delta) of the corresponding market-order side.
        delta_a = ask_price - mid_price
        delta_b = mid_price - bid_price
        prob_ask = np.minimum(1.0, A * np.exp(-k * delta_a) * dt)
        prob_bid = np.minimum(1.0, A * np.exp(-k * delta_b) * dt)

        ask_executed = u_ask[step] < prob_ask
        bid_executed = u_bid[step] < prob_bid

        # Ask execution: agent sells, inventory decreases by one, cash increases by the ask price.
        # Bid execution: agent buys, inventory increases by one, cash decreases by the bid price.
        inventory = inventory - ask_executed.astype(float) + bid_executed.astype(float)
        cash = cash + ask_executed * ask_price - bid_executed * bid_price

        mid_price = mid_price + price_shocks[step]

    profit = cash + inventory * mid_price  # final P&L, Section 3.3
    return SimulationResult(
        strategy=strategy,
        gamma=gamma,
        profit=profit,
        final_inventory=inventory,
        final_mid_price=mid_price,
        spread=float(spread_constant(gamma, k)),
    )


def run_gamma_experiment(
    gamma: float,
    sigma: float,
    k: float,
    A: float,
    T: float,
    dt: float,
    s0: float,
    q0: float,
    n_paths: int,
    seed: int,
) -> dict[str, SimulationResult]:
    """Run both the 'inventory' and 'symmetric' strategies for one gamma value.

    Returns a dict {'inventory': SimulationResult, 'symmetric': SimulationResult}.
    Each strategy draws its own independent Monte Carlo sample (offset seed),
    consistent with the paper reporting only the mean/std of each strategy's
    P&L and final inventory across its own 1000 simulations (Section 3.3).
    """
    results: dict[str, SimulationResult] = {}
    for offset, strategy in enumerate(("inventory", "symmetric")):
        results[strategy] = simulate_strategy(
            strategy=strategy, gamma=gamma, sigma=sigma, k=k, A=A, T=T, dt=dt,
            s0=s0, q0=q0, n_paths=n_paths, seed=seed + offset,
        )
    return results


def summarize(result: SimulationResult) -> dict:
    """Mean/std of profit and final inventory, matching the columns of Tables 1-3."""
    return {
        "strategy": result.strategy,
        "gamma": result.gamma,
        "spread": result.spread,
        "profit_mean": float(np.mean(result.profit)),
        "profit_std": float(np.std(result.profit, ddof=1)),
        "final_q_mean": float(np.mean(result.final_inventory)),
        "final_q_std": float(np.std(result.final_inventory, ddof=1)),
    }
