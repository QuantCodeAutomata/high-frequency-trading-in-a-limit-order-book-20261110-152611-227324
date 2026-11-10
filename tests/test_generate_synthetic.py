"""Unit tests for the synthetic-input generators (data/generate_synthetic.py)."""
import numpy as np
import pytest

from data.generate_synthetic import generate_order_arrival_uniforms, generate_price_shocks


def test_price_shocks_shape_and_support():
    rng = np.random.default_rng(0)
    sigma, dt = 2.0, 0.005
    shocks = generate_price_shocks(n_steps=50, n_paths=200, sigma=sigma, dt=dt, rng=rng)
    assert shocks.shape == (50, 200)
    expected_step = sigma * np.sqrt(dt)
    assert np.all(np.isclose(np.abs(shocks), expected_step))


def test_price_shocks_both_signs_present():
    rng = np.random.default_rng(1)
    shocks = generate_price_shocks(n_steps=200, n_paths=200, sigma=2.0, dt=0.005, rng=rng)
    assert np.any(shocks > 0)
    assert np.any(shocks < 0)


def test_price_shocks_rejects_invalid_params():
    rng = np.random.default_rng(0)
    with pytest.raises(ValueError):
        generate_price_shocks(0, 10, 2.0, 0.005, rng)
    with pytest.raises(ValueError):
        generate_price_shocks(10, 10, -1.0, 0.005, rng)


def test_order_arrival_uniforms_shape_and_range():
    rng = np.random.default_rng(2)
    u_ask, u_bid = generate_order_arrival_uniforms(n_steps=100, n_paths=50, rng=rng)
    assert u_ask.shape == (100, 50)
    assert u_bid.shape == (100, 50)
    for arr in (u_ask, u_bid):
        assert np.all(arr >= 0.0) and np.all(arr < 1.0)


def test_order_arrival_uniforms_are_independent_streams():
    rng = np.random.default_rng(3)
    u_ask, u_bid = generate_order_arrival_uniforms(n_steps=1000, n_paths=10, rng=rng)
    assert not np.array_equal(u_ask, u_bid)
