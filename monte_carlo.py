import numpy as np
from dcf_model import calculate_dcf
from fundamental_analysis import simulate_wacc


def run_monte_carlo(
    revenue_0,
    assumptions,
    tax_rate,
    starting_nwc,
    terminal_growth,
    years,
    debt,
    equity,
    risk_free_rate,
    beta,
    equity_risk_premium,
    pre_tax_cost_of_debt,
    num_simulations=1000,
    seed=42
):
    rng = np.random.default_rng(seed)

    simulated_values = []

    for _ in range(num_simulations):

        growth_sample = rng.normal(
            assumptions["growth_mean"],
            assumptions["growth_std"]
        )

        margin_sample = rng.normal(
            assumptions["margin_mean"],
            assumptions["margin_std"]
        )

        capex_sample = rng.normal(
            assumptions["capex_mean"],
            assumptions["capex_std"]
        )

        da_sample = rng.normal(
            assumptions["da_mean"],
            assumptions["da_std"]
        )

        nwc_sample = rng.normal(
            assumptions["nwc_mean"],
            assumptions["nwc_std"]
        )

        wacc_sample = simulate_wacc(
            rng=rng,
            risk_free_rate=risk_free_rate,
            beta=beta,
            equity_risk_premium=equity_risk_premium,
            pre_tax_cost_of_debt=pre_tax_cost_of_debt,
            tax_rate=tax_rate,
            debt=debt,
            equity=equity
)

        growth_sample = np.clip(
            growth_sample,
            -0.05,
            0.20
        )

        margin_sample = np.clip(
            margin_sample,
            0.05,
            0.30
        )

        capex_sample = np.clip(
            capex_sample,
            0.01,
            0.15
        )

        da_sample = np.clip(
            da_sample,
            0.01,
            0.10
        )

        nwc_sample = np.clip(
            nwc_sample,
            0.01,
            0.30
        )

        wacc_sample = np.clip(
            wacc_sample,
            0.07,
            0.15
        )

        value = calculate_dcf(
            revenue_0=revenue_0,
            growth=growth_sample,
            ebit_margin=margin_sample,
            tax_rate=tax_rate,
            capex_pct=capex_sample,
            da_pct=da_sample,
            nwc_pct=nwc_sample,
            starting_nwc=starting_nwc,
            wacc=wacc_sample,
            terminal_growth=terminal_growth,
            years=years
        )

        simulated_values.append(value)

    return np.array(simulated_values)