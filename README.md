# Monte Carlo DCF Valuation Engine

A probabilistic enterprise valuation framework combining fundamental financial analysis, FCFF-based DCF valuation, stochastic WACC modeling, Monte Carlo simulation, downside-risk analysis, and sensitivity analysis.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-orange)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-red)

## Overview

Traditional DCF models usually produce a single valuation based on a fixed set of assumptions.

This project treats valuation as a probability distribution.

Instead of asking:

> What is the value of the company?

the model asks:

> What does the distribution of possible valuations look like when the underlying assumptions are uncertain?

The framework takes historical financial data, extracts operating characteristics, builds an FCFF DCF model, introduces uncertainty into both operating assumptions and the cost of capital, and runs Monte Carlo simulations to generate a distribution of possible enterprise values.

## Key Features

- Fundamental financial statement analysis
- Historical operating and financial ratios
- Forecast assumption extraction
- FCFF-based DCF valuation
- Proper change in net working capital treatment
- CAPM-based cost of equity
- WACC calculation
- Stochastic WACC simulation
- Monte Carlo valuation
- Value at Risk analysis
- Conditional Value at Risk
- Revenue growth sensitivity analysis
- EBIT margin sensitivity analysis
- WACC sensitivity analysis
- WACC versus terminal growth matrix
- Valuation heatmap
- 3D DCF valuation surface
- Equity value per share
- Margin-of-safety analysis
- Reproducible simulations using a fixed random seed

## Model Architecture

    Historical Financial Statements
                  |
                  v
        Fundamental Analysis
                  |
          +-------+-------+
          |               |
          v               v
    Operating Metrics   WACC Inputs
          |               |
          v               v
    Forecast Inputs    CAPM + Debt Cost
          |               |
          +-------+-------+
                  |
                  v
          Monte Carlo Engine
                  |
                  v
             FCFF DCF Model
                  |
         +--------+--------+
         |        |        |
         v        v        v
      Valuation  Risk   Sensitivity
     Distribution Metrics Analysis
         |        |        |
         +--------+--------+
                  |
                  v
         Equity Value / Share
                  |
                  v
           Margin of Safety

## Fundamental Analysis

The model calculates historical financial and operating metrics from the input financial statements.

### Operating Metrics

- Revenue growth
- EBITDA margin
- EBIT margin
- Net profit margin
- Free cash flow
- Free cash flow margin
- CFO / PAT
- ROIC
- ROE
- Asset turnover
- CapEx / Revenue
- Depreciation / Revenue

### Capital Structure and Credit Metrics

- Debt / Equity
- Debt / EBITDA
- Net Debt / EBITDA
- Interest coverage
- Net working capital
- NWC / Revenue

Historical observations are used to estimate the central tendency and dispersion of forecast assumptions.

## FCFF DCF Model

The core valuation engine uses an unlevered Free Cash Flow to Firm framework.

    FCFF = NOPAT + D&A - CapEx - Change in NWC

where:

    NOPAT = EBIT x (1 - Tax Rate)

The model explicitly accounts for the change in net working capital rather than treating total NWC as an annual cash outflow.

Future FCFF is discounted using WACC.

    PV of FCFF = FCFF / (1 + WACC)^t

Enterprise value is calculated as:

    Enterprise Value =
    Present Value of Forecast FCFF
    +
    Present Value of Terminal Value

## Terminal Value

Terminal value is calculated using the Gordon Growth Model.

    Terminal Value =
    FCFF in the following year
    --------------------------
    WACC - Terminal Growth

The terminal value is then discounted back to present value.

The model enforces the condition:

    WACC > Terminal Growth

to avoid an invalid terminal value calculation.

## WACC

Cost of equity is calculated using CAPM.

    Cost of Equity =
    Risk-Free Rate + Beta x Equity Risk Premium

After-tax cost of debt:

    After-Tax Cost of Debt =
    Pre-Tax Cost of Debt x (1 - Tax Rate)

WACC combines the cost of equity and after-tax cost of debt using debt and equity weights.

Using the included illustrative dataset, the deterministic WACC is approximately:

10.96%

## Stochastic WACC

One of the main features of the project is stochastic WACC.

Instead of treating WACC as a fixed number throughout the Monte Carlo simulation, the model introduces uncertainty into the underlying cost-of-capital inputs.

The simulation samples:

- Risk-free rate
- Beta
- Equity risk premium
- Pre-tax cost of debt

Each sampled set of inputs produces a new WACC.

This allows valuation uncertainty to come from both operating assumptions and capital-market assumptions.

## Monte Carlo Simulation

The model runs 1,000 valuation scenarios.

Each simulation samples operating assumptions including:

- Revenue growth
- EBIT margin
- CapEx / Revenue
- D&A / Revenue
- NWC / Revenue

The model also samples the inputs used to construct WACC.

Each scenario is then passed through the DCF engine to produce an enterprise valuation.

Repeating this process produces a full valuation distribution rather than a single point estimate.

The simulation uses a fixed random seed for reproducibility.

    Simulations: 1,000
    Seed: 42

## Example Results

Using the included illustrative financial dataset:

| Metric | Result |
|---|---:|
| Deterministic Enterprise Value | ₹2,683 Cr |
| Monte Carlo Mean | ₹2,743 Cr |
| Monte Carlo Median | ₹2,712 Cr |
| Standard Deviation | ₹357 Cr |
| 5th Percentile | ₹2,225 Cr |
| 25th Percentile | ₹2,497 Cr |
| 75th Percentile | ₹2,950 Cr |
| 95th Percentile | ₹3,371 Cr |
| Lower-Tail CVaR | ₹2,112 Cr |

The deterministic DCF and Monte Carlo median are relatively close, providing a useful sanity check for the simulation framework.

## Downside Risk

The project evaluates the lower tail of the valuation distribution rather than focusing only on the mean.

### Value at Risk

The 5th percentile is used as a downside valuation threshold.

5% VaR: ₹2,225 Cr

### Conditional Value at Risk

Lower-tail CVaR measures the average valuation of the worst 5% of simulated outcomes.

Lower-Tail CVaR: ₹2,112 Cr

This provides additional information about the severity of extreme downside scenarios.

## Equity Valuation

The simulated enterprise values are converted into illustrative equity values and per-share valuations.

| Metric | Result |
|---|---:|
| Mean Value / Share | ₹50.86 |
| Median Value / Share | ₹50.24 |
| 5th Percentile | ₹40.50 |
| 95th Percentile | ₹63.41 |
| Illustrative Market Price | ₹38.00 |

Approximately 97.7% of simulations produce a value above the illustrative market price.

## Margin of Safety

The model also evaluates the margin of safety implied by each simulated valuation.

| Metric | Result |
|---|---:|
| Median Margin of Safety | 24.36% |
| Mean Margin of Safety | 23.84% |
| Simulations with at least 25% MOS | 47.90% |

This turns the valuation distribution into a probabilistic measure of downside protection under the model assumptions.

## Sensitivity Analysis

DCF valuation is highly sensitive to key assumptions.

The project evaluates the impact of changes in revenue growth, EBIT margin, WACC, and terminal growth.

### Revenue Growth

| Growth | Enterprise Value |
|---:|---:|
| 5.0% | ₹2,115 Cr |
| 7.5% | ₹2,300 Cr |
| 10.0% | ₹2,498 Cr |
| 12.5% | ₹2,709 Cr |
| 15.0% | ₹2,934 Cr |

### EBIT Margin

| EBIT Margin | Enterprise Value |
|---:|---:|
| 12.0% | ₹1,361 Cr |
| 15.0% | ₹1,942 Cr |
| 18.0% | ₹2,524 Cr |
| 21.0% | ₹3,105 Cr |
| 24.0% | ₹3,687 Cr |

### WACC

| WACC | Enterprise Value |
|---:|---:|
| 8.0% | ₹4,171 Cr |
| 9.0% | ₹3,432 Cr |
| 10.0% | ₹2,905 Cr |
| 11.0% | ₹2,510 Cr |
| 12.0% | ₹2,204 Cr |

The sensitivity results demonstrate the nonlinear relationship between discount rates and DCF valuation.

## WACC and Terminal Growth Matrix

The model evaluates the interaction between WACC and terminal growth.

| WACC / Growth | 2.0% | 2.5% | 3.0% | 3.5% | 4.0% |
|---|---:|---:|---:|---:|---:|
| 8.0% | 3556 | 3836 | 4171 | 4581 | 5093 |
| 9.0% | 3009 | 3204 | 3432 | 3701 | 4024 |
| 10.0% | 2599 | 2742 | 2905 | 3093 | 3313 |
| 11.0% | 2281 | 2389 | 2510 | 2648 | 2805 |
| 12.0% | 2027 | 2111 | 2204 | 2308 | 2426 |

The project also visualizes this relationship using a heatmap and a 3D valuation surface.

## Visualizations

The project generates several visual outputs.

### Monte Carlo Valuation Distribution

Displays the distribution of simulated enterprise values and the resulting valuation range.

### WACC and Terminal Growth Heatmap

Shows how enterprise value changes as the discount rate and terminal growth assumptions vary.

### 3D DCF Valuation Surface

Visualizes the nonlinear relationship between:

- WACC
- Terminal growth
- Enterprise value

## Repository Structure

    Monte-Carlo-DCF-Valuation-Engine/
    |
    +-- dcf_model.py
    +-- fundamental_analysis.py
    +-- monte_carlo.py
    +-- main.py
    +-- financials.csv
    +-- requirements.txt
    +-- README.md
    |
    +-- outputs/

### dcf_model.py

Contains the core FCFF DCF valuation engine.

### fundamental_analysis.py

Handles:

- Financial ratio calculations
- Forecast assumption extraction
- WACC calculation
- Stochastic WACC generation

### monte_carlo.py

Runs the probabilistic valuation engine.

### main.py

Coordinates:

- Financial data loading
- Fundamental analysis
- Forecast assumptions
- Deterministic DCF
- Monte Carlo simulation
- Risk analysis
- Sensitivity analysis
- Equity valuation
- Visualization

### financials.csv

Contains the financial statement inputs used by the model.

## Reproducibility

The Monte Carlo engine uses NumPy's seeded random number generator.

    rng = np.random.default_rng(seed)

Using the same seed and assumptions produces reproducible simulations.

Default configuration:

    Simulations: 1,000
    Seed: 42

## Technology Stack

- Python 3.11+
- NumPy
- Pandas
- Matplotlib

The project combines concepts from:

- Corporate finance
- Financial statement analysis
- Quantitative finance
- Probability and statistics
- Numerical computing
- Risk modeling
- Valuation analytics

## Running the Project

Clone the repository:

    git clone https://github.com/snowwwyyyyy/Monte-Carlo-DCF-Valuation-Engine.git

Enter the project directory:

    cd Monte-Carlo-DCF-Valuation-Engine

Install dependencies:

    pip install -r requirements.txt

Run the model:

    python main.py

## Limitations

This project is intended as a research and educational valuation framework.

The included financial dataset is illustrative and is designed to demonstrate the modeling architecture.

Current limitations include:

- Limited historical observations
- Forecast distributions derived from a small sample
- Independent sampling of operating assumptions
- Deterministic terminal growth
- Simplified capital structure assumptions
- Modeling assumptions for WACC uncertainty
- No explicit correlation matrix between operating variables
- No macroeconomic regime-switching model
- No automated real-time financial data pipeline
- No historical DCF forecast backtesting

The results should therefore be interpreted as outputs of the model under its assumptions rather than predictions of actual market prices.

## Future Extensions

### Correlated Monte Carlo Inputs

Introduce a covariance or correlation matrix to model relationships between revenue growth, margins, CapEx, working capital, and WACC.

### Stochastic Terminal Growth

Model terminal growth as a probability distribution instead of a single deterministic assumption.

### Market-Derived WACC

Replace illustrative inputs with market-derived:

- Treasury yields
- Equity beta
- Equity risk premium
- Current borrowing costs
- Market capitalization
- Market-value debt

### Automated Financial Data Pipeline

Automatically retrieve financial statements and market data instead of relying on manually supplied CSV inputs.

### Economic Regime Modeling

Introduce different economic regimes such as expansion, normal growth, slowdown, and recession, with regime-dependent financial assumptions.

### Historical Backtesting

Compare historical DCF estimates with subsequent realized valuations and measure forecast error, calibration, bias, and confidence-interval coverage.

## Why This Project?

A conventional DCF model produces a point estimate.

A probabilistic DCF asks a broader question:

> Given uncertainty in the assumptions, what is the distribution of possible valuations?

This project combines fundamental analysis, corporate valuation, probability, statistics, and quantitative modeling into a single reproducible framework.

The objective is not to create a false sense of precision.

It is to make valuation uncertainty explicit, quantify downside risk, and understand which assumptions have the greatest influence on enterprise value.

## Disclaimer

This repository is for educational and research purposes only.

The valuations generated by this model depend on the assumptions and methodology used. They should not be interpreted as financial advice, investment recommendations, or guarantees of future asset prices.
