
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(page_title="Danube AI Insight — Demo", layout="wide",
                   initial_sidebar_state="expanded")

# ---- Sidebar ----
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/3/37/Placeholder_no_text.png", width=120)
st.sidebar.title("Danube AI Insight")
st.sidebar.markdown("**Demo** — ROI Predictor & Smart Energy Optimizer")
st.sidebar.write("Present this at events to show how simple AI-driven insights can add value to real estate projects.")
st.sidebar.caption("Built with Python + Streamlit • Offline demo (simulated data)")

# ---- Header ----
st.title("Danube AI Insight")
st.markdown("**Two concise demos:** 1) ROI Predictor for investors — quick projected returns; 2) Smart Energy Optimizer — simulated energy savings for residents.")
st.write("---")

# ---- Tabs ----
tab1, tab2 = st.tabs(["📈 ROI Predictor", "⚡ Smart Energy Optimizer"])

# ---------- TAB 1: ROI Predictor ----------
with tab1:
    st.header("ROI Predictor — quick projection")
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("### Scenario inputs")
        location_score = st.slider("Location attractiveness score (1 = low, 10 = high)", 1, 10, 6)
        purchase_price = st.number_input("Purchase price (AED)", min_value=100000.0, value=1000000.0, step=50000.0, format="%.2f")
        annual_appreciation = st.slider("Expected annual appreciation (%)", 0.0, 15.0, 5.0, step=0.5)
        annual_rental_yield = st.slider("Expected gross rental yield (%)", 0.0, 12.0, 6.0, step=0.25)
        holding_years = st.slider("Holding period (years)", 1, 10, 5)
        annual_expenses_pct = st.slider("Annual operating expenses (% of rent)", 0.0, 50.0, 20.0, step=1.0)
        st.markdown("**Notes:** This is a simplified estimator for demo purposes. Real investment decisions require full legal and financial review.")
    with col2:
        st.markdown("### Quick scenario presets")
        if st.button("Conservative (Low growth)"):
            st.session_state.annual_appreciation = 2.0
            st.session_state.annual_rental_yield = 4.0
            st.session_state.holding_years = 5
        if st.button("Balanced (Typical)"):
            st.session_state.annual_appreciation = 5.0
            st.session_state.annual_rental_yield = 6.0
            st.session_state.holding_years = 5
        if st.button("Aggressive (High growth)"):
            st.session_state.annual_appreciation = 10.0
            st.session_state.annual_rental_yield = 8.0
            st.session_state.holding_years = 7

    # Read back any preset changes (safe fallback to local variables)
    annual_appreciation = float(st.session_state.get("annual_appreciation", annual_appreciation))
    annual_rental_yield = float(st.session_state.get("annual_rental_yield", annual_rental_yield))
    holding_years = int(st.session_state.get("holding_years", holding_years))

    st.markdown("### Results")
    # Simulate year-by-year growth
    years = np.arange(0, holding_years+1)
    values = purchase_price * (1 + annual_appreciation/100) ** years
    # rental income (gross)
    yearly_rent = purchase_price * (annual_rental_yield/100)
    # net rental after expenses
    net_rent = yearly_rent * (1 - annual_expenses_pct/100)
    cumulative_rent = net_rent * np.arange(0, holding_years+1)  # simplify cumulative income

    final_value = values[-1]
    total_income = cumulative_rent[-1]
    total_return = (final_value + total_income - purchase_price) / purchase_price * 100

    st.metric(label="Projected final value (AED)", value=f"{final_value:,.0f}")
    st.metric(label="Projected total return (incl. net rent) %", value=f"{total_return:.1f}%")
    st.markdown("---")

    # Plot growth
    fig, ax = plt.subplots(figsize=(7,3.5))
    ax.plot(years, values, marker="o")
    ax.set_xlabel("Years")
    ax.set_ylabel("Estimated property value (AED)")
    ax.set_title("Property value projection")
    st.pyplot(fig)

    # Small summary table
    summary_df = pd.DataFrame({
        "Year": years,
        "Estimated Value (AED)": values.round(0),
        "Cumulative Net Rent (AED)": cumulative_rent.round(0)
    })
    st.dataframe(summary_df.style.format({"Estimated Value (AED)": "{:,.0f}", "Cumulative Net Rent (AED)": "{:,.0f}"}), height=250)

    st.markdown("**Talking points for event:**")
    st.write("- Show investors how small changes in appreciation or rental yield change ROI.")
    st.write("- Emphasize assumptions: tax, transaction fees and financing are not included in this demo.")

# ---------- TAB 2: Smart Energy Optimizer ----------
with tab2:
    st.header("Smart Energy Optimizer — simulated savings")
    left, right = st.columns([2,1])
    with left:
        st.markdown("### Scenario inputs")
        building_type = st.selectbox("Building type", ["Apartment", "Villa", "Office"])
        baseline_profile = st.selectbox("Baseline consumption profile", ["Low", "Medium", "High"])
        occupants = st.slider("Average occupants (per unit)", 1, 10, 3)
        ac_setpoint = st.slider("AC setpoint during occupied hours (°C)", 20, 26, 23)
        lighting_behavior = st.selectbox("Lighting behavior", ["Conservative", "Normal", "Generous"])
        duration_days = st.slider("Simulate days", 1, 14, 7)
        st.markdown("**Note:** This is a rule-based simulated optimizer for demo only.")
    with right:
        st.markdown("### Quick presets")
        if st.button("Residential, typical"):
            st.session_state.building_type = "Apartment"
            st.session_state.baseline_profile = "Medium"
            st.session_state.occupants = 3
        if st.button("Office, high use"):
            st.session_state.building_type = "Office"
            st.session_state.baseline_profile = "High"
            st.session_state.occupants = 6

    # Pull any preset changes
    building_type = st.session_state.get("building_type", building_type)
    baseline_profile = st.session_state.get("baseline_profile", baseline_profile)
    occupants = int(st.session_state.get("occupants", occupants))
    ac_setpoint = int(st.session_state.get("ac_setpoint", ac_setpoint))
    lighting_behavior = st.session_state.get("lighting_behavior", lighting_behavior)
    duration_days = int(st.session_state.get("duration_days", duration_days))

    # Simulate baseline hourly consumption (kWh) for given days
    hours = duration_days * 24
    rng = np.random.default_rng(seed=42)
    base_level = {"Low": 1.0, "Medium": 1.6, "High": 2.4}[baseline_profile]  # kWh per hour baseline multiplier
    occupant_influence = 0.1 * occupants
    hourly_baseline = base_level + occupant_influence * rng.normal(1.0, 0.05, size=hours)

    # Create a simple optimizer: reduce HVAC energy when unoccupied and shift temperatures
    # Occupied hours assumption: 7am-9am, 6pm-11pm for residential; 8am-6pm for office
    def occupied_mask(days, btype):
        mask = np.zeros(days*24, dtype=bool)
        for d in range(days):
            base = d*24
            if btype == "Apartment" or btype == "Villa":
                mask[base+7:base+9] = True
                mask[base+18:base+23] = True
            else:
                mask[base+8:base+18] = True
        return mask

    occ = occupied_mask(duration_days, building_type)
    # Lighting factor
    lighting_factor = {"Conservative": 0.8, "Normal": 1.0, "Generous": 1.2}[lighting_behavior]

    # Baseline includes lighting + HVAC influence
    lighting_hourly = 0.2 * lighting_factor * rng.normal(1.0, 0.02, size=hours)
    hvac_hourly = hourly_baseline * 0.6  # HVAC portion
    other_hourly = hourly_baseline * 0.4 * rng.normal(1.0,0.05,size=hours)

    baseline_total = lighting_hourly + hvac_hourly + other_hourly

    # Optimizer: when unoccupied, set HVAC to setback (reduce by 25%); when occupied, smart setpoint reduces HVAC by a small percent
    optimized_hvac = hvac_hourly.copy()
    optimized_hvac[~occ] *= 0.7  # setback when unoccupied
    # smart setpoint effect: slightly better when occupants follow good behaviors and setpoint chosen
    setpoint_effect = max(0, (26 - ac_setpoint) / 6)  # higher setpoint => more saving
    optimized_hvac[occ] *= (1 - 0.05 * setpoint_effect)

    optimized_lighting = lighting_hourly * (0.85 if lighting_behavior=="Conservative" else (1.0 if lighting_behavior=="Normal" else 1.1))

    optimized_total = optimized_lighting + optimized_hvac + other_hourly

    baseline_sum = baseline_total.sum()
    optimized_sum = optimized_total.sum()
    pct_saving = (baseline_sum - optimized_sum) / baseline_sum * 100

    st.metric("Estimated baseline energy (kWh)", f"{baseline_sum:,.1f}")
    st.metric("Estimated optimized energy (kWh)", f"{optimized_sum:,.1f}")
    st.metric("Estimated savings", f"{pct_saving:.1f}%")
    st.markdown("---")

    # Prepare time index for plotting
    start = datetime.now()
    time_index = [start + timedelta(hours=int(i)) for i in range(hours)]

    df = pd.DataFrame({
        "timestamp": time_index,
        "baseline_kwh": baseline_total,
        "optimized_kwh": optimized_total,
        "occupied": occ.astype(int)
    })
    df = df.set_index("timestamp")

    st.markdown("### Consumption profile (simulated)")
    fig2, ax2 = plt.subplots(figsize=(9,3.5))
    ax2.plot(df.index, df.baseline_kwh, label="Baseline")
    ax2.plot(df.index, df.optimized_kwh, label="Optimized", linestyle="--")
    ax2.set_ylabel("kWh per hour")
    ax2.set_xlabel("Time")
    ax2.set_title("Baseline vs Optimized hourly consumption (simulated)")
    ax2.legend()
    st.pyplot(fig2)

    st.markdown("### Quick actionable recommendations")
    st.write("- Implement occupancy-aware setback on HVAC to reduce energy when apartments are empty.")
    st.write("- Use adaptive lighting control and smart scheduling to lower lighting during unoccupied periods.")
    st.write("- Combine energy optimization with tenant engagement (alerts, simple app nudges) for higher adoption.")
    st.write("- This demo is rule-based; production systems use sensors + ML models to improve savings over time.")

# ---- Footer ----
st.write("---")
st.markdown("**Demo created for showcasing AI value in Real Estate — Danube AI Insight**")
st.markdown("If you want, I can: (1) package this into a single downloadable app, (2) add more realistic ML models, (3) create a short demo video for your event.")
