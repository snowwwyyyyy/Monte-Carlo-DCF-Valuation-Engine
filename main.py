import numpy as np
import matplotlib.pyplot as plt
from dcf_model import calculate_dcf

revenue_0 = 1000.0
growth = 0.1
ebit_margin = 0.18
tax_rate = 0.25

capex_pct = 0.05
da_pct = 0.03
nwc_pct = 0.01

wacc = 0.1
terminal_growth = 0.03
years = 5

revenue = revenue_0

revenues = []
fcffs = []

for year in range(1, years + 1):
    revenue *= (1 + growth)
    revenues.append(revenue)

    ebit = revenue * ebit_margin
    tax = ebit * tax_rate
    nopat = ebit - tax

    capex = revenue * capex_pct
    depreciation = revenue * da_pct
    change_nwc = revenue * nwc_pct

    fcff = nopat + depreciation - capex - change_nwc
    fcffs.append(fcff)

    print(f"Year {year}: Revenue = {revenue:.2f}, FCFF = {fcff:.2f}")

pv_fcffs = []

for year, fcff in enumerate(fcffs, start=1):
    pv = fcff / ((1 + wacc) ** year)
    pv_fcffs.append(pv)

    print(f"Year {year}: PV of FCFF = {pv:.2f} cr")

fcff_next = fcffs[-1] * (1 + terminal_growth)
terminal_value = fcff_next / (wacc - terminal_growth)

pv_terminal_value = terminal_value / ((1 + wacc) ** years)

enterprise_value = sum(pv_fcffs) + pv_terminal_value

print("\n --- DCF VALUATION ---")
print(f"Terminal Value = {terminal_value:.2f} cr")
print(f"PV of Terminal Value = {pv_terminal_value:.2f} cr")
print(f"Enterprise Value = {enterprise_value:.2f} cr")


# test_value = calculate_dcf(
#     growth=0.10,
#     ebit_margin=0.18,
#     wacc=0.10,
#     terminal_growth=0.03
# )

# print("Reusable DCF value:", round(test_value, 2), "Cr")

rng = np.random.default_rng(42)


# num_simulations = 1000
# simulated_values = []

# for i in range(num_simulations):
#     growth_sample = rng.normal(loc=0.10, scale=0.02)
#     value = calculate_dcf(
#         growth=growth_sample,
#         ebit_margin=0.18,
#         wacc=0.10,
#         terminal_growth=0.03
#     )
#     simulated_values.append(value)

# print("Number of Simulations:", len(simulated_values))
# print("First 5 Valuations:")
# for i, val in enumerate(simulated_values[:5]):
#     print(round(value, 2), "Cr")




num_simulations = 1000
simulated_values = []

for i in range(num_simulations):

    
    growth_sample = rng.normal(0.10, 0.02)
    margin_sample = rng.normal(0.18, 0.015)
    wacc_sample = rng.normal(0.10, 0.01)

    
    growth_sample = np.clip(growth_sample, -0.05, 0.20)
    margin_sample = np.clip(margin_sample, 0.05, 0.30)
    wacc_sample = np.clip(wacc_sample, 0.07, 0.15)

    
    value = calculate_dcf(
    revenue_0=revenue_0,
    growth=growth_sample,
    ebit_margin=margin_sample,
    tax_rate=tax_rate,
    capex_pct=capex_pct,
    da_pct=da_pct,
    nwc_pct=nwc_pct,
    wacc=wacc_sample,
    terminal_growth=0.03,
    years=years
    )


    simulated_values.append(value)

# print(
    #     f"Simulation {i + 1}: "
    #     f"Growth = {growth_sample:.2%}, "
    #     f"Value = {value:.2f} Cr"
    # )

values = np.array(simulated_values)

print("\n--- MONTE CARLO RESULTS ---")
print("Mean valuation:", round(np.mean(values), 2), "Cr")
print("Median valuation:", round(np.median(values), 2), "Cr")
print("Standard deviation:", round(np.std(values), 2), "Cr")

print("5th percentile:", round(np.percentile(values, 5), 2), "Cr")
print("25th percentile:", round(np.percentile(values, 25), 2), "Cr")
print("75th percentile:", round(np.percentile(values, 75), 2), "Cr")
print("95th percentile:", round(np.percentile(values, 95), 2), "Cr")


var_5 = np.percentile(values, 5)

worst_5_percent = values[values <= var_5]

cvar_5 = np.mean(worst_5_percent)

print("\n--- DOWNSIDE VALUATION RISK ---")
print("5th percentile (VaR threshold):",
      round(var_5, 2), "Cr")

print("Lower-tail CVaR (worst 5% average):",
      round(cvar_5, 2), "Cr")




base_growth = 0.10
base_margin = 0.18
base_wacc = 0.10
terminal_growth = 0.03

print("\n--- SENSITIVITY ANALYSIS ---")



print("\nRevenue Growth")

for g in [0.05, 0.075, 0.10, 0.125, 0.15]:
    ev = calculate_dcf(
        revenue_0=revenue_0,
        growth=g,
        ebit_margin=base_margin,
        tax_rate=tax_rate,
        capex_pct=capex_pct,
        da_pct=da_pct,
        nwc_pct=nwc_pct,
        wacc=base_wacc,
        terminal_growth=terminal_growth,
        years=years
    )
    print(f"Growth: {g:.1%} | EV: ₹{ev:.2f} Cr")





print("\nEBIT Margin")

for margin in [0.12, 0.15, 0.18, 0.21, 0.24]:
    ev = calculate_dcf(
        revenue_0=revenue_0,
        growth=base_growth,
        ebit_margin=margin,
        tax_rate=tax_rate,
        capex_pct=capex_pct,
        da_pct=da_pct,
        nwc_pct=nwc_pct,
        wacc=base_wacc,
        terminal_growth=terminal_growth,
        years=years
    )

    print(f"Margin: {margin:.1%} | EV: ₹{ev:.2f} Cr")



print("\nWACC")

for w in [0.08, 0.09, 0.10, 0.11, 0.12]:
    
    ev = calculate_dcf(
    revenue_0=revenue_0,
    growth=base_growth,
    ebit_margin=base_margin,
    tax_rate=tax_rate,
    capex_pct=capex_pct,
    da_pct=da_pct,
    nwc_pct=nwc_pct,
    wacc=w,
    terminal_growth=terminal_growth,
    years=years
)

    print(f"WACC: {w:.1%} | EV: ₹{ev:.2f} Cr")




# STEP 22: Two-variable sensitivity matrix

wacc_values = [0.08, 0.09, 0.10, 0.11, 0.12]
terminal_growth_values = [0.02, 0.025, 0.03, 0.035, 0.04]

print("\n--- WACC x TERMINAL GROWTH MATRIX ---")

print("WACC / Growth", end="")

for tg in terminal_growth_values:
    print(f"\t{tg:.1%}", end="")

print()

for w in wacc_values:
    print(f"{w:.1%}", end="")

    for tg in terminal_growth_values:
        if w <= tg:
            print("\tN/A", end="")
        else:
            ev = calculate_dcf(
                revenue_0=revenue_0,
                growth=base_growth,
                ebit_margin=base_margin,
                tax_rate=tax_rate,
                capex_pct=capex_pct,
                da_pct=da_pct,
                nwc_pct=nwc_pct,
                wacc=w,
                terminal_growth=tg,
                years=years
            )

            print(f"\t{ev:.0f}", end="")

    print()



# STEP 23: Visual WACC x terminal-growth heatmap

wacc_values = [0.08, 0.09, 0.10, 0.11, 0.12]
terminal_growth_values = [0.02, 0.025, 0.03, 0.035, 0.04]

valuation_matrix = np.zeros(
    (len(wacc_values), len(terminal_growth_values))
)

for i, w in enumerate(wacc_values):
    for j, tg in enumerate(terminal_growth_values):
        valuation_matrix[i, j] = calculate_dcf(
    revenue_0=revenue_0,
    growth=base_growth,
    ebit_margin=base_margin,
    tax_rate=tax_rate,
    capex_pct=capex_pct,
    da_pct=da_pct,
    nwc_pct=nwc_pct,
    wacc=w,
    terminal_growth=tg,
    years=years
)

plt.figure(figsize=(9, 6))

image = plt.imshow(
    valuation_matrix,
    aspect="auto"
)

plt.xticks(
    range(len(terminal_growth_values)),
    [f"{tg:.1%}" for tg in terminal_growth_values]
)

plt.yticks(
    range(len(wacc_values)),
    [f"{w:.1%}" for w in wacc_values]
)

plt.xlabel("Terminal Growth Rate")
plt.ylabel("WACC")
plt.title("DCF Sensitivity Heatmap: Enterprise Value (₹ Cr)")

plt.colorbar(image, label="Enterprise Value (₹ Cr)")

for i in range(len(wacc_values)):
    for j in range(len(terminal_growth_values)):
        plt.text(
            j, i,
            f"{valuation_matrix[i, j]:.0f}",
            ha="center",
            va="center"
        )

plt.tight_layout()
plt.show()

debt = 300.0
cash = 100.0
shares_outstanding = 50.0
market_price = 38.0


equity_values = values - debt + cash



share_values = equity_values / shares_outstanding

print("\n--- EQUITY VALUATION ---")
print("Mean value per share:",
      round(np.mean(share_values), 2), "₹")

print("Median value per share:",
      round(np.median(share_values), 2), "₹")

print("5th percentile:",
      round(np.percentile(share_values, 5), 2), "₹")

print("95th percentile:",
      round(np.percentile(share_values, 95), 2), "₹")


probability_undervalued = np.mean(
    share_values > market_price
)

print("Illustrative market price:", market_price, "₹")
print("Simulations above market price:",
      f"{probability_undervalued:.2%}")


margin_of_safety = (
    (share_values - market_price) / share_values
) * 100

print("\n--- MARGIN OF SAFETY ANALYSIS ---")
print("Median margin of safety:",
      round(np.median(margin_of_safety), 2), "%")

print("Mean margin of safety:",
      round(np.mean(margin_of_safety), 2), "%")

# Fraction of simulations meeting 25% MOS
target_mos = 25.0

qualifying_simulations = np.mean(
    margin_of_safety >= target_mos
)

print("Simulations with at least 25% margin of safety:",
      f"{qualifying_simulations:.2%}")


plt.figure(figsize=(10, 6))

plt.hist(
    simulated_values,
    bins=30,
    edgecolor="black"
)

plt.axvline(
    np.mean(simulated_values),
    linestyle="--",
    label="Mean valuation"
)

plt.axvline(
    np.median(simulated_values),
    linestyle=":",
    label="Median valuation"
)

plt.title("Monte Carlo DCF: Valuation Distribution")
plt.xlabel("Enterprise Value (₹ Crore)")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.show()


