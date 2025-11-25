import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(page_title="Credit Card Recommendation System", layout="wide")

# ============================
# PLAY INTRO ANIMATION ONLY ONCE
# ============================

# Load CSV
df = pd.read_csv("credit_cards.csv", encoding='ISO-8859-1')

# Page Title
st.markdown("## 💳 Credit Card Recommendation System")
st.write("Use the filters below to find the best credit card for your needs.")
st.write("---")

# ================================
# LAYOUT: LEFT FILTERS + RIGHT IMAGE
# ================================
left, right = st.columns([3, 2])

# ================================
# LEFT SIDE FILTERS
# ================================
with left:

    # --------- BANK FILTER -----------
    st.markdown("### 🏦 Select Bank")
    bank = st.selectbox(
        "",
        options=["All"] + sorted(df['bank_name'].unique().tolist())
    )
    st.write("")

    # --------- MAX ANNUAL FEE (NUMBER INPUT) ----------
    st.markdown("### 💰 Maximum Annual Fee")
    max_fee = st.number_input(
        "",
        min_value=0,
        max_value=20000,
        value=20000,
        step=100
    )
    st.caption("Enter the maximum annual fee you are comfortable paying.")
    st.write("")

    # --------- BEST USE CASE (PURE DROPDOWN) ----------
    st.markdown("### 🎯 Best Use Case")
    use_case = st.selectbox(
        "",
        options=["Any"] + sorted(df['best_use_case'].unique().tolist())
    )
    st.write("")

    # --------- LIFETIME FREE FILTER ----------
    st.markdown("### 🔄 Lifetime Free?")
    lifetime_free = st.selectbox(
        "",
        options=["Any", "Yes", "No"]
    )
    st.write("")

    # --------- GO BUTTON ----------
    go = st.button("🔍 GO", use_container_width=True)

# ================================
# RIGHT SIDE IMAGE SECTION
# ================================
with right:
    st.markdown("### ")
    # Replace 'card.png' with your own uploaded image filename
    try:
        st.image("app_logo.png", use_container_width=True)
    except:
        st.info("Upload your credit card image as 'card.png' to display it here.")


# ================================
# APPLY FILTERS ONLY AFTER GO BUTTON
# ================================
if go:
    # =======================
    # VALIDATION CHECK
    # =======================
    if lifetime_free == "Yes" and max_fee > 0:
        st.warning("⚠️ You selected 'Lifetime Free' but also entered a maximum annual fee above 0. Lifetime Free cards always have an annual fee of 0.\n\n👉 Please set Maximum Annual Fee = 0 to view Lifetime Free cards.")
        st.stop()

    filtered_df = df.copy()

    # Bank filter
    if bank != "All":
        filtered_df = filtered_df[filtered_df["bank_name"] == bank]

    # Annual Fee filter
    filtered_df = filtered_df[filtered_df["annual_fee"] <= max_fee]

    # Best Use Case filter
    if use_case != "Any":
        filtered_df = filtered_df[
            filtered_df["best_use_case"].str.contains(use_case, case=False, na=False)
        ]

    # Lifetime Free filter
    if lifetime_free != "Any":
        filtered_df = filtered_df[filtered_df["is_lifetime_free"] == lifetime_free]

    st.write("---")
    st.markdown("### 📋 Recommended Cards")

    # Columns to display
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

    # ============================
    # ADD BADGE COLUMN HERE 🔥
    # ============================

    def get_badge(row):
        fee = row["Annual Fee"]

    # Lifetime free always top priority
        if row["Lifetime Free"] == "Yes":
            return "🟢 Lifetime Free"

    # Affordable
        if 1 <= fee <= 2000:
            return "🟡 Affordable"

    # Mid-Tier
        if 2001 <= fee <= 5000:
            return "🔵 Mid-Tier"

    # Premium
        if fee > 5000:
            return "✨ Premium"

        return ""


    display_df["Badge"] = display_df.apply(get_badge, axis=1)

    # Reorder columns to show badge nicely
    display_df = display_df[[
        "Bank",
        "Card Name",
        "Annual Fee",
        "Renewal Fee",
        "Use Case",
        "Lifetime Free",
        "Badge",
        "Notes"
    ]]

    st.dataframe(display_df.reset_index(drop=True), use_container_width=True)
