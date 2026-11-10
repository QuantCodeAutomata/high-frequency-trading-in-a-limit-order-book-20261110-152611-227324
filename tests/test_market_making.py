"""Unit tests for the closed-form quoting formulas (src/market_making.py)."""
import numpy as np
import pytest

from src.market_making import quotes, reservation_price, spread_constant, spread_time_varying


def test_spread_constant_matches_table_values():
    """Reported 'Spread' column of Tables 1-3: 1.29 (gamma=0.1), 1.33 (gamma=0.01), 1.15 (gamma=0.5)."""
    assert spread_constant(0.1, 1.5) == pytest.approx(1.29, abs=0.01)
    assert spread_constant(0.01, 1.5) == pytest.approx(1.33, abs=0.01)
    assert spread_constant(0.5, 1.5) == pytest.approx(1.15, abs=0.01)


def test_spread_constant_requires_positive_params():
    with pytest.raises(ValueError):
        spread_constant(0.0, 1.5)
    with pytest.raises(ValueError):
        spread_constant(0.1, 0.0)


def test_spread_time_varying_decreases_to_constant_at_maturity():
    """delta_a + delta_b = gamma*sigma^2*(T-t) + constant; at t=T the inventory term vanishes."""
    gamma, sigma, k = 0.1, 2.0, 1.5
    full_at_start = spread_time_varying(1.0, gamma, sigma, k)
    full_at_end = spread_time_varying(0.0, gamma, sigma, k)
    assert full_at_start > full_at_end
    assert full_at_end == pytest.approx(spread_constant(gamma, k))


def test_reservation_price_shifts_down_for_long_inventory():
    """r(s,t) = s - q*gamma*sigma^2*(T-t), Eq. (3.17): a long position lowers the indifference price."""
    s, gamma, sigma, tau = 100.0, 0.1, 2.0, 0.5
    r_long = reservation_price(s, inventory=5.0, gamma=gamma, sigma=sigma, time_to_maturity=tau)
    r_flat = reservation_price(s, inventory=0.0, gamma=gamma, sigma=sigma, time_to_maturity=tau)
    r_short = reservation_price(s, inventory=-5.0, gamma=gamma, sigma=sigma, time_to_maturity=tau)
    assert r_long < r_flat < r_short


def test_reservation_price_equals_mid_price_at_maturity():
    assert reservation_price(100.0, 7.0, 0.1, 2.0, time_to_maturity=0.0) == pytest.approx(100.0)


def test_inventory_quotes_centered_on_reservation_price():
    s, q, tau, gamma, sigma, k = 100.0, 3.0, 0.5, 0.1, 2.0, 1.5
    ask, bid = quotes("inventory", s, q, tau, gamma, sigma, k)
    r = reservation_price(s, q, gamma, sigma, tau)
    spread = spread_time_varying(tau, gamma, sigma, k)
    assert ask == pytest.approx(r + spread / 2.0)
    assert bid == pytest.approx(r - spread / 2.0)
    assert ask > bid


def test_symmetric_quotes_centered_on_mid_price():
    s, q, tau, gamma, sigma, k = 100.0, 3.0, 0.5, 0.1, 2.0, 1.5
    ask, bid = quotes("symmetric", s, q, tau, gamma, sigma, k)
    spread = spread_time_varying(tau, gamma, sigma, k)
    assert ask == pytest.approx(s + spread / 2.0)
    assert bid == pytest.approx(s - spread / 2.0)


def test_inventory_and_symmetric_quotes_differ_for_nonzero_inventory():
    s, q, tau, gamma, sigma, k = 100.0, 5.0, 0.5, 0.1, 2.0, 1.5
    ask_inv, bid_inv = quotes("inventory", s, q, tau, gamma, sigma, k)
    ask_sym, bid_sym = quotes("symmetric", s, q, tau, gamma, sigma, k)
    assert ask_inv != ask_sym
    assert bid_inv != bid_sym
    # Both strategies use the identical spread, only centered differently.
    assert (ask_inv - bid_inv) == pytest.approx(ask_sym - bid_sym)


def test_quotes_rejects_unknown_strategy():
    with pytest.raises(ValueError):
        quotes("unknown", 100.0, 0.0, 0.5, 0.1, 2.0, 1.5)


def test_quotes_vectorized_over_paths():
    s = np.array([100.0, 101.0, 99.0])
    q = np.array([0.0, 2.0, -2.0])
    ask, bid = quotes("inventory", s, q, 0.5, 0.1, 2.0, 1.5)
    assert ask.shape == (3,)
    assert bid.shape == (3,)
    assert np.all(ask > bid)
