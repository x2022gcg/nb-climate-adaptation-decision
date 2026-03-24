
from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

@st.cache_data
def load_data():
    flood_df = pd.read_csv(DATA_DIR / "Data.csv", encoding="latin1")
    wildfire_df = pd.read_csv(DATA_DIR / "Canadian_Wildfire_Evacuation_Data.csv")
    return flood_df, wildfire_df

flood_df, wildfire_df = load_data()

st.sidebar.header("Filters")

min_year = int(min(flood_df["Year"].min(), wildfire_df["Year"].min()))
max_year = int(max(flood_df["Year"].max(), wildfire_df["Year"].max()))

year_range = st.sidebar.slider(
    "Select year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

flood_filtered = flood_df[
    (flood_df["Year"] >= year_range[0]) & (flood_df["Year"] <= year_range[1])
]

wildfire_filtered = wildfire_df[
    (wildfire_df["Year"] >= year_range[0]) & (wildfire_df["Year"] <= year_range[1])
]

tab1, tab2, tab3 = st.tabs(
    ["Decision Overview", "Flood Risk", "Wildfire & Resilience"]
)

with tab1:
    st.subheader("Decision Context")
    st.write(
        "Should the New Brunswick Minister of Natural Resources and Energy Development "
        "prioritize coastal flood-protection infrastructure or invest in forest-based "
        "carbon sequestration and wildfire-resilience programs?"
    )

    st.image("img/cld-refined.png", caption="Refined Causal Loop Diagram", use_container_width=True)

    st.info(
        "Flood data highlights rising insurance-related costs, while wildfire data shows "
        "severe spike years and long-term resilience concerns."
    )

with tab2:
    st.subheader("Flood Risk and Insurance")

    metric = st.selectbox(
        "Choose a flood metric",
        ["Auto Claims", "P&C Claims", "P&C Premiums"]
    )

    fig_flood = px.line(
        flood_filtered,
        x="Year",
        y=metric,
        markers=True,
        title=f"{metric} Over Time"
    )
    st.plotly_chart(fig_flood, use_container_width=True)

    st.write(
        "This chart helps the decision-maker see how flood-related costs have changed over time "
        "and whether financial pressure is increasing."
    )

with tab3:
    st.subheader("Wildfire Damage and Forest Resilience")

    fig_fire = px.bar(
        wildfire_filtered,
        x="Year",
        y="Housing Damage",
        title="Housing Damage from Forest Fires Over Time"
    )
    st.plotly_chart(fig_fire, use_container_width=True)

    selected_year = st.selectbox(
        "Highlight a year",
        sorted(wildfire_filtered["Year"].unique(), reverse=True)
    )

    selected_row = wildfire_filtered[wildfire_filtered["Year"] == selected_year]

    if not selected_row.empty:
        st.metric(
            label=f"Housing Damage in {selected_year}",
            value=f"${selected_row['Housing Damage'].iloc[0]:,.0f}"
        )

    st.write(
        "This section shows how wildfire losses can spike sharply in severe years, supporting "
        "the case for long-term forest-based resilience investments."
    )

st.subheader("Flood Claims vs Premiums")

fig_compare = px.line(
    flood_filtered,
    x="Year",
    y=["Auto Claims", "P&C Claims", "P&C Premiums"],
    markers=True,
    title="Flood-Related Claims and Premiums"
)
st.plotly_chart(fig_compare, use_container_width=True)








