"""Synthetic inputs for the Avellaneda-Stoikov market-making simulation.

No market data is required for this replication: Section 3.3 of the paper
("Numerical simulations") states that the experiment "relies on simulated
stock price paths and synthetic Poisson arrivals of market orders". This
module generates the two independent random inputs the simulation consumes:

- the discretized mid-price shocks, following "the mid-price is updated by a
  random increment +/- sigma*sqrt(dt)" (Section 3.3);
- the uniform draws used to decide whether a market order reaches the
  agent's ask or bid quote, following "with probability lambda^a(delta^a) dt,
  the inventory variable decreases by one ... with probability
  lambda^b(delta^b) dt, the inventory increases by one" (Section 3.3).

Generation is separated from the sequential quote/execution logic in
``src.simulation``, which consumes these arrays to update the market maker's
state step by step.
"""
from __future__ import annotations

import numpy as np


def generate_price_shocks(
    n_steps: int, n_paths: int, sigma: float, dt: float, rng: np.random.Generator
) -> np.ndarray:
    """Random +/- sigma*sqrt(dt) mid-price increments (Section 3.3).

    Parameters
    ----------
    n_steps: number of simulation time steps.
    n_paths: number of independent Monte Carlo paths.
    sigma: mid-price volatility.
    dt: simulation time step.
    rng: numpy random Generator used for all draws.

    Returns
    -------
    Array of shape (n_steps, n_paths) with values in {-sigma*sqrt(dt), +sigma*sqrt(dt)}.
    """
    if n_steps <= 0 or n_paths <= 0:
        raise ValueError("n_steps and n_paths must be positive")
    if sigma <= 0 or dt <= 0:
        raise ValueError("sigma and dt must be positive")
    signs = rng.choice(np.array([-1.0, 1.0]), size=(n_steps, n_paths))
    return signs * sigma * np.sqrt(dt)


def generate_order_arrival_uniforms(
    n_steps: int, n_paths: int, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    """Independent uniform(0, 1) draws deciding ask- and bid-side executions.

    A market order is deemed to execute against the agent's ask (resp. bid)
    quote at a given step when the corresponding draw falls below the
    execution probability computed from the quote's distance to the
    mid-price (Section 3.3).

    Returns
    -------
    Tuple (u_ask, u_bid), each of shape (n_steps, n_paths).
    """
    if n_steps <= 0 or n_paths <= 0:
        raise ValueError("n_steps and n_paths must be positive")
    u_ask = rng.random((n_steps, n_paths))
    u_bid = rng.random((n_steps, n_paths))
    return u_ask, u_bid
