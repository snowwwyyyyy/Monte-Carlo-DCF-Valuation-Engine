import pandas as pd
from pathlib import Path
import numpy as np

def calculate_ratios(df):
    df = df.copy()

    # Growth
    df["revenue_growth"] = df["revenue"].pct_change()

    # Profitability
    df["ebitda_margin"] = df["ebitda"] / df["revenue"]
    df["ebit_margin"] = df["ebit"] / df["revenue"]
    df["net_profit_margin"] = df["pat"] / df["revenue"]

    # Cash flow
    df["fcf"] = df["cash_from_operations"] - df["capex"]
    df["fcf_margin"] = df["fcf"] / df["revenue"]
    df["cfo_to_pat"] = df["cash_from_operations"] / df["pat"]

    # Capital efficiency
    df["roic"] = (
        df["ebit"] * (1 - 0.25)
        / (df["equity"] + df["net_debt"])
    )
    df["net_working_capital"] = (
    df["current_assets"] - df["current_liabilities"]
)

    df["nwc_to_revenue"] = (
    df["net_working_capital"] / df["revenue"]
)

    df["depreciation_to_revenue"] = (
    df["depreciation"] / df["revenue"]
)
    df["roe"] = df["pat"] / df["equity"]

    df["asset_turnover"] = df["revenue"] / df["total_assets"]

    # Capital expenditure
    df["capex_to_revenue"] = df["capex"] / df["revenue"]

    # Leverage
    df["debt_to_equity"] = df["total_debt"] / df["equity"]
    df["debt_to_ebitda"] = df["total_debt"] / df["ebitda"]
    df["net_debt_to_ebitda"] = df["net_debt"] / df["ebitda"]

    # Interest coverage
    df["interest_coverage"] = df["ebit"] / df["interest_expense"]
        

    return df


BASE_DIR = Path(__file__).resolve().parent

df = pd.read_csv(BASE_DIR / "financials.csv")

df = calculate_ratios(df)

print("\nFundamental Analysis\n")

print(
    df[
        [
            "year",
            "revenue_growth",
            "ebitda_margin",
            "ebit_margin",
            "net_profit_margin",
            "fcf",
            "fcf_margin",
            "cfo_to_pat",
            "roic",
            "roe",
            "asset_turnover",
            "debt_to_equity",
            "debt_to_ebitda",
            "net_debt_to_ebitda",
            "interest_coverage"
        ]
    ].round(4)
)

def get_forecast_assumptions(df):
    historical_growth = df["revenue_growth"].dropna()
    historical_margin = df["ebit_margin"].dropna()
    historical_capex = df["capex_to_revenue"].dropna()
    historical_da = df["depreciation_to_revenue"].dropna()
    historical_nwc = df["nwc_to_revenue"].dropna()

    assumptions = {
        "growth_mean": historical_growth.mean(),
        "growth_std": historical_growth.std(),

        "margin_mean": historical_margin.mean(),
        "margin_std": historical_margin.std(),

        "capex_mean": historical_capex.mean(),
        "capex_std": historical_capex.std(),

        "da_mean": historical_da.mean(),
        "da_std": historical_da.std(),

        "nwc_mean": historical_nwc.mean(),
        "nwc_std": historical_nwc.std()
    }

    return assumptions

assumptions = get_forecast_assumptions(df)

def calculate_wacc(
    risk_free_rate,
    beta,
    equity_risk_premium,
    pre_tax_cost_of_debt,
    tax_rate,
    debt,
    equity
):
    """
    Calculate WACC using CAPM for cost of equity.
    """

    total_capital = debt + equity

    if total_capital <= 0:
        raise ValueError("Debt + equity must be greater than zero.")

    cost_of_equity = (
        risk_free_rate
        + beta * equity_risk_premium
    )

    after_tax_cost_of_debt = (
        pre_tax_cost_of_debt * (1 - tax_rate)
    )

    equity_weight = equity / total_capital
    debt_weight = debt / total_capital

    wacc = (
        equity_weight * cost_of_equity
        + debt_weight * after_tax_cost_of_debt
    )

    return wacc

def simulate_wacc(
    rng,
    risk_free_rate,
    beta,
    equity_risk_premium,
    pre_tax_cost_of_debt,
    tax_rate,
    debt,
    equity
):
    """
    Generate one stochastic WACC scenario by sampling
    the major cost-of-capital inputs.
    """

    rf_sample = rng.normal(
        risk_free_rate,
        0.005
    )

    beta_sample = rng.normal(
        beta,
        0.10
    )

    erp_sample = rng.normal(
        equity_risk_premium,
        0.01
    )

    debt_cost_sample = rng.normal(
        pre_tax_cost_of_debt,
        0.01
    )

    rf_sample = np.clip(
        rf_sample,
        0.03,
        0.12
    )

    beta_sample = np.clip(
        beta_sample,
        0.50,
        1.50
    )

    erp_sample = np.clip(
        erp_sample,
        0.03,
        0.10
    )

    debt_cost_sample = np.clip(
        debt_cost_sample,
        0.03,
        0.15
    )

    return calculate_wacc(
        risk_free_rate=rf_sample,
        beta=beta_sample,
        equity_risk_premium=erp_sample,
        pre_tax_cost_of_debt=debt_cost_sample,
        tax_rate=tax_rate,
        debt=debt,
        equity=equity
    )

print("\nForecast Assumptions\n")

for key, value in assumptions.items():
    print(f"{key}: {value:.4f}")

if __name__ == "__main__":
    wacc = calculate_wacc(
        risk_free_rate=0.07,
        beta=1.0,
        equity_risk_premium=0.06,
        pre_tax_cost_of_debt=0.07,
        tax_rate=0.25,
        debt=310,
        equity=870
    )

    print("Calculated WACC:", round(wacc, 4))