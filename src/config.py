"""Parameters for the Monte Carlo market-making experiments.

All values are taken from Avellaneda & Stoikov (2006), "High-frequency
trading in a limit order book", Section 3.3 ("Numerical simulations"),
unless stated otherwise. Experiments 1-3 share the same market-simulation
parameters and differ only in the risk-aversion coefficient gamma.
"""

# --- Shared simulation parameters (Section 3.3) ---
S0 = 100.0       # initial mid-price, Section 3.3
T = 1.0          # terminal time / trading horizon, Section 3.3
SIGMA = 2.0      # volatility of the mid-price random walk, Section 3.3
DT = 0.005       # simulation time step, Section 3.3
Q0 = 0.0         # initial inventory, Section 3.3
K = 1.5          # order-arrival intensity decay parameter, Section 3.3
A = 140.0        # order-arrival intensity scale parameter, Section 3.3
N_PATHS = 1000   # number of Monte Carlo paths ("we then run 1000 simulations"), Section 3.3

# Random seed: not specified in the paper. Fixed here for reproducibility;
# each experiment offsets it so the three gamma values use independent streams.
SEED = 20061005  # date of the paper (2006-10-05), used only as a fixed, documented seed

# --- Experiment 1: gamma = 0.1 (Table 1, Figure 2) ---
GAMMA_EXP1 = 0.1   # risk-aversion coefficient, Section 3.3 / Table 1

# --- Experiment 2: gamma = 0.01, close to risk-neutral (Table 2, Figure 3) ---
GAMMA_EXP2 = 0.01  # risk-aversion coefficient, Section 3.3 / Table 2

# --- Experiment 3: gamma = 0.5, highly risk-averse (Table 3, Figure 4) ---
GAMMA_EXP3 = 0.5   # risk-aversion coefficient, Section 3.3 / Table 3
