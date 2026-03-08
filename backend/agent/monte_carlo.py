"""Monte Carlo projection engine for Project SAGE.

Runs 10,000 simulations across three scenarios (base, optimistic, stress)
to project portfolio value through retirement.
"""

import numpy as np

NUM_SIMULATIONS = 10_000

# Return and volatility assumptions by risk profile and scenario
ASSUMPTIONS = {
    "conservative": {
        "base":       {"mean_return": 0.050, "volatility": 0.08},
        "optimistic": {"mean_return": 0.065, "volatility": 0.07},
        "stress":     {"mean_return": 0.025, "volatility": 0.12},
    },
    "moderate": {
        "base":       {"mean_return": 0.065, "volatility": 0.12},
        "optimistic": {"mean_return": 0.085, "volatility": 0.10},
        "stress":     {"mean_return": 0.030, "volatility": 0.18},
    },
    "aggressive": {
        "base":       {"mean_return": 0.080, "volatility": 0.16},
        "optimistic": {"mean_return": 0.100, "volatility": 0.14},
        "stress":     {"mean_return": 0.035, "volatility": 0.22},
    },
}

INFLATION_RATE = 0.025


def run_monte_carlo_simulation(
    portfolio_value: float,
    annual_contribution: float,
    annual_withdrawal: float,
    years_to_retirement: int,
    years_in_retirement: int,
    risk_profile: str = "moderate",
) -> dict:
    """Run Monte Carlo simulation across three scenarios.

    Returns percentile outcomes and probability of success for each scenario.
    """
    profile = ASSUMPTIONS.get(risk_profile, ASSUMPTIONS["moderate"])
    total_years = years_to_retirement + years_in_retirement

    results = {}
    for scenario_name, params in profile.items():
        scenario_result = _run_scenario(
            portfolio_value=portfolio_value,
            annual_contribution=annual_contribution,
            annual_withdrawal=annual_withdrawal,
            years_to_retirement=years_to_retirement,
            years_in_retirement=years_in_retirement,
            total_years=total_years,
            mean_return=params["mean_return"],
            volatility=params["volatility"],
        )
        results[scenario_name] = scenario_result

    results["parameters"] = {
        "portfolio_value": portfolio_value,
        "annual_contribution": annual_contribution,
        "annual_withdrawal": annual_withdrawal,
        "years_to_retirement": years_to_retirement,
        "years_in_retirement": years_in_retirement,
        "risk_profile": risk_profile,
        "num_simulations": NUM_SIMULATIONS,
        "inflation_rate": INFLATION_RATE,
    }

    return results


def _run_scenario(
    portfolio_value: float,
    annual_contribution: float,
    annual_withdrawal: float,
    years_to_retirement: int,
    years_in_retirement: int,
    total_years: int,
    mean_return: float,
    volatility: float,
) -> dict:
    """Run a single scenario with NUM_SIMULATIONS paths."""
    np.random.seed(None)  # fresh seed each run

    # Generate random returns: shape (NUM_SIMULATIONS, total_years)
    returns = np.random.normal(mean_return, volatility, (NUM_SIMULATIONS, total_years))

    # Track portfolio value over time
    portfolios = np.zeros((NUM_SIMULATIONS, total_years + 1))
    portfolios[:, 0] = portfolio_value

    for year in range(total_years):
        # Inflation-adjusted contribution/withdrawal
        inflation_factor = (1 + INFLATION_RATE) ** year

        if year < years_to_retirement:
            # Accumulation phase: contributions
            cash_flow = annual_contribution * inflation_factor
        else:
            # Distribution phase: withdrawals (negative)
            cash_flow = -annual_withdrawal * inflation_factor

        # Apply return and cash flow
        portfolios[:, year + 1] = portfolios[:, year] * (1 + returns[:, year]) + cash_flow

        # Floor at zero (can't go negative)
        portfolios[:, year + 1] = np.maximum(portfolios[:, year + 1], 0)

    # Final values
    final_values = portfolios[:, -1]
    retirement_values = portfolios[:, years_to_retirement]

    # Probability of success = portfolio > 0 at end
    success_count = np.sum(final_values > 0)
    probability_of_success = round(float(success_count / NUM_SIMULATIONS * 100), 1)

    # Percentile outcomes
    percentiles = {
        "p10": round(float(np.percentile(final_values, 10)), 0),
        "p25": round(float(np.percentile(final_values, 25)), 0),
        "p50": round(float(np.percentile(final_values, 50)), 0),
        "p75": round(float(np.percentile(final_values, 75)), 0),
        "p90": round(float(np.percentile(final_values, 90)), 0),
    }

    retirement_percentiles = {
        "p10": round(float(np.percentile(retirement_values, 10)), 0),
        "p25": round(float(np.percentile(retirement_values, 25)), 0),
        "p50": round(float(np.percentile(retirement_values, 50)), 0),
        "p75": round(float(np.percentile(retirement_values, 75)), 0),
        "p90": round(float(np.percentile(retirement_values, 90)), 0),
    }

    # Year-by-year median trajectory for charting
    median_trajectory = [round(float(np.median(portfolios[:, y])), 0) for y in range(total_years + 1)]

    return {
        "probability_of_success": probability_of_success,
        "final_value_percentiles": percentiles,
        "at_retirement_percentiles": retirement_percentiles,
        "median_trajectory": median_trajectory,
        "mean_return": mean_return,
        "volatility": volatility,
    }
