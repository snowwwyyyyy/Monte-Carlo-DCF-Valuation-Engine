def calculate_dcf(
    revenue_0,
    growth,
    ebit_margin,
    tax_rate,
    capex_pct,
    da_pct,
    nwc_pct,
    wacc,
    terminal_growth,
    years,
    starting_nwc=0
):
    """
    Calculate enterprise value using an FCFF DCF model.
    Monetary values use the same units as revenue_0.
    """

    if years < 1:
        raise ValueError("years must be at least 1")

    if wacc <= terminal_growth:
        raise ValueError(
            "WACC must be greater than terminal growth."
        )

    revenue = revenue_0
    previous_nwc = starting_nwc
    fcffs = []

    for year in range(1, years + 1):
        revenue *= (1 + growth)

        ebit = revenue * ebit_margin
        nopat = ebit * (1 - tax_rate)

        depreciation = revenue * da_pct
        capex = revenue * capex_pct

        nwc = revenue * nwc_pct
        change_nwc = nwc - previous_nwc
        previous_nwc = nwc

        fcff = (
            nopat
            + depreciation
            - capex
            - change_nwc
        )

        fcffs.append(fcff)

    pv_fcffs = sum(
        fcff / (1 + wacc) ** year
        for year, fcff in enumerate(fcffs, start=1)
    )

    fcff_next = fcffs[-1] * (1 + terminal_growth)

    terminal_value = fcff_next / (wacc - terminal_growth)

    pv_terminal = terminal_value / ((1 + wacc) ** years)

    enterprise_value = pv_fcffs + pv_terminal

    return enterprise_value