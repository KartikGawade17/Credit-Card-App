import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("credit_cards.csv", encoding='ISO-8859-1')

st.set_page_config(page_title="Credit Card Recommendation System", layout="wide")

st.markdown("## 💳 Credit Card Recommendation System")
st.write("Use the filters below to find the best credit card for your needs.")

st.write("---")

# -------------------------
# FILTERS ON MAIN PAGE
# -------------------------

col1, col2, col3, col4, col5 = st.columns([2,2,2,2,1])

with col1:
    bank = st.selectbox(
        "Select Bank",
        options=["All"] + sorted(df['bank_name'].unique().tolist())
    )

with col2:
    max_fee = st.slider(
        "Maximum Annual Fee",
        min_value=0,
        max_value=20000,    # You asked to reduce to 20,000
        value=20000
    )

with col3:
    use_case = st.selectbox(
        "Best Use Case",
        options=["Any"] + sorted(df['best_use_case'].unique().tolist())
    )

with col4:
    lifetime_free = st.selectbox(
        "Lifetime Free?",
        options=["Any", "Yes", "No"]
    )

# GO BUTTON
with col5:
    go = st.button("🔍 GO")

# -------------------------
# PROCESS FILTERS ONLY WHEN BUTTON CLICKED
# -------------------------

filtered_df = df.copy()

if go:

    # Bank filter
    if bank != "All":
        filtered_df = filtered_df[filtered_df["bank_name"] == bank]

    # Fee filter
    filtered_df = filtered_df[filtered_df["annual_fee"] <= max_fee]

    # Use case filter
    if use_case != "Any":
        filtered_df = filtered_df[
            filtered_df["best_use_case"].str.contains(use_case, case=False, na=False)
        ]

    # Lifetime free filter
    if lifetime_free != "Any":
        filtered_df = filtered_df[filtered_df["is_lifetime_free"] == lifetime_free]

    # -------------------------
    # Display clean output table
    # -------------------------

    # show only important columns
    cols_to_show = [
        "bank_name",
        "card_name",
        "annual_fee",
        "renewal_fee",
        "best_use_case",
        "is_lifetime_free",
        "notes"
    ]
    
    display_df = filtered_df[cols_to_show].rename(columns={
    "bank_name": "Bank",
    "card_name": "Card Name",
    "annual_fee": "Annual Fee",
    "renewal_fee": "Renewal Fee",
    "best_use_case": "Use Case",
    "is_lifetime_free": "Lifetime Free",
    "notes": "Notes"
})
    
    st.write("### 📋 Recommended Cards")

    st.dataframe(display_df.reset_index(drop=True), use_container_width=True)

