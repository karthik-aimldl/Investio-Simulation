import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# -----------------------------
# Asset Returns
# -----------------------------
returns = {
    "Stocks": 0.08,
    "Bonds": 0.04,
    "Gold": 0.05,
    "Deposits": 0.03,
    "Others": 0.06
}

# -----------------------------
# UI
# -----------------------------
st.title("📊 Wealth Dashboard (Deterministic Model)")

st.subheader("💰 Initial Investment per Asset")

stocks = st.number_input("Stocks (£)", value=6000)
bonds = st.number_input("Bonds (£)", value=3000)
gold = st.number_input("Gold (£)", value=1000)
deposits = st.number_input("Deposits (£)", value=2000)
others = st.number_input("Others (£)", value=1000)

initial_assets = {
    "Stocks": stocks,
    "Bonds": bonds,
    "Gold": gold,
    "Deposits": deposits,
    "Others": others
}

total = sum(initial_assets.values())
st.write(f"### 💵 Total Investment: £{total:,.2f}")

# -----------------------------
# Growth Function
# -----------------------------
def project_growth(initial_assets, years):
    asset_paths = {}

    for asset, value in initial_assets.items():
        r = returns[asset]
        path = [value]
        current = value

        for _ in range(years):
            current = current * (1 + r)
            path.append(current)

        asset_paths[asset] = path

    total_path = []

    for i in range(years + 1):
        total_path.append(sum(asset_paths[a][i] for a in asset_paths))

    return asset_paths, total_path

# -----------------------------
# Run Simulation
# -----------------------------
if st.button("Generate Projection"):

    horizons = [5, 10, 15, 20]

    all_results = {}
    horizon_values = []

    # -----------------------------
    # STORE ALL RESULTS PROPERLY
    # -----------------------------
    for h in horizons:
        assets, total_path = project_growth(initial_assets.copy(), h)

        all_results[h] = {
            "assets": assets,
            "total": total_path
        }

        horizon_values.append(total_path[-1])

    # -----------------------------
    # PIE + LINE CHARTS PER HORIZON
    # -----------------------------
    for h in horizons:
        st.markdown(f"## 📊 {h}-Year Analysis")

        assets = all_results[h]["assets"]
        total_path = all_results[h]["total"]

        col1, col2 = st.columns(2)

        # -----------------------------
        # 🥧 PIE CHART (LEFT)
        # -----------------------------
        with col1:
            st.markdown("### 🥧 Allocation")

            final_values = [assets[a][-1] for a in assets]

            fig1, ax1 = plt.subplots()
            ax1.pie(final_values, labels=assets.keys(), autopct='%1.1f%%')
            ax1.set_title(f"{h}-Year Composition")

            st.pyplot(fig1)

        # -----------------------------
        # 📈 LINE CHART (RIGHT)
        # -----------------------------
        with col2:
            st.markdown("### 📈 Growth")

            fig2, ax2 = plt.subplots()
            ax2.plot(range(h + 1), total_path, linewidth=3)

            ax2.set_title(f"{h}-Year Portfolio Growth")
            ax2.set_xlabel("Years")
            ax2.set_ylabel("Value (£)")

            st.pyplot(fig2)

            # -----------------------------
            # METRIC BELOW BOTH
            # -----------------------------
            st.metric("Final Value", f"£{total_path[-1]:,.0f}")

        st.write("---")

    # -----------------------------
    # STACKED CHART (20Y)
    # -----------------------------
    st.subheader("📊 Asset Breakdown (20 Years)")

    assets_20 = all_results[20]["assets"]

    fig3, ax3 = plt.subplots()

    x = np.arange(21)
    bottom = np.zeros(21)

    for asset, path in assets_20.items():
        ax3.bar(x, path, bottom=bottom, label=asset)
        bottom += np.array(path)

    ax3.set_xlabel("Years")
    ax3.set_ylabel("Value (£)")
    ax3.legend()

    st.pyplot(fig3)

    # -----------------------------
    # TABLE (20Y)
    # -----------------------------
    st.subheader("📋 Year-wise Projection (20 Years)")

    total_20 = all_results[20]["total"]

    df = pd.DataFrame({"Year": x})

    for asset, path in assets_20.items():
        df[asset] = path

    df["Total"] = total_20

    st.dataframe(df)

    # -----------------------------
    # HORIZON COMPARISON
    # -----------------------------
    st.subheader("📊 Horizon Comparison")

    fig4, ax4 = plt.subplots()

    ax4.bar([str(h) + "Y" for h in horizons], horizon_values)

    ax4.set_title("Final Portfolio Value by Horizon")
    ax4.set_ylabel("Value (£)")

    for i, v in enumerate(horizon_values):
        ax4.text(i, v, f"£{v:,.0f}", ha='center', va='bottom')

    st.pyplot(fig4)

    # -----------------------------
    # SUMMARY TABLE
    # -----------------------------
    st.subheader("📋 Summary Table")

    summary_df = pd.DataFrame({
        "Years": horizons,
        "Final Value (£)": horizon_values
    })

    st.dataframe(summary_df)