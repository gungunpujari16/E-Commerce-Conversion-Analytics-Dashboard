"""
utils.py — Shared data loading, preprocessing, and styling helpers
E-Commerce Conversion Analytics Dashboard
"""

import pandas as pd
import numpy as np
import streamlit as st


# ── Brand colours ────────────────────────────────────────────────────────────
BLUE    = "#2563EB"
RED     = "#E74C3C"
GREEN   = "#27AE60"
AMBER   = "#F59E0B"
PURPLE  = "#8B5CF6"
PINK    = "#EC4899"
NAVY    = "#1E3A5F"
LGRAY   = "#F1F5F9"

PALETTE = [BLUE, RED, GREEN, AMBER, PURPLE, PINK, "#06B6D4", "#84CC16"]

FUNNEL_COLORS = {
    "Product Page":    RED,
    "Cart":            AMBER,
    "Checkout":        BLUE,
    "Payment Gateway": PURPLE,
    "None":            GREEN,
}

TRAFFIC_COLORS = {
    "Email":        GREEN,
    "Organic":      BLUE,
    "Referral":     PURPLE,
    "Paid Search":  AMBER,
    "Direct":       PINK,
    "Social Media": RED,
}

DEVICE_COLORS = {
    "Desktop": BLUE,
    "Tablet":  AMBER,
    "Mobile":  RED,
}


# ── Data loading ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str = "ecommerce_cleaned.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Abandonment_Point"]   = df["Abandonment_Point"].fillna("None")
    df["Product_Category_2"]  = df["Product_Category_2"].fillna("No Second Category")
    df["Converted_bin"]       = (df["Converted"] == "Yes").astype(int)
    df["Return_bin"]          = (df["Return_Customer"] == "Yes").astype(int)
    df["Discount_bin"]        = (df["Discount_Code_Used"] == "Yes").astype(int)
    df["Cart_bin"]            = (df["Added_to_Cart"] == "Yes").astype(int)
    df["Engagement_Score"]    = df["Time_Spent_on_Site"] * df["Pages_Viewed"]
    df["Avg_Time_Per_Page"]   = df["Time_Spent_on_Site"] / (df["Pages_Viewed"] + 1)
    df["High_Engagement"]     = (
        (df["Time_Spent_on_Site"] > 15) & (df["Pages_Viewed"] > 5)
    ).astype(int)
    return df


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Apply sidebar filters to the main dataframe."""
    dff = df.copy()
    if filters.get("traffic"):
        dff = dff[dff["Traffic_Source"].isin(filters["traffic"])]
    if filters.get("device"):
        dff = dff[dff["Device_Type"].isin(filters["device"])]
    if filters.get("category"):
        dff = dff[dff["Product_Category"].isin(filters["category"])]
    if filters.get("location"):
        dff = dff[dff["Location"].isin(filters["location"])]
    if filters.get("payment"):
        dff = dff[dff["Payment_Method"].isin(filters["payment"])]
    if filters.get("return_customer") and filters["return_customer"] != "All":
        dff = dff[dff["Return_Customer"] == filters["return_customer"]]
    if filters.get("age_range"):
        lo, hi = filters["age_range"]
        dff = dff[(dff["Age"] >= lo) & (dff["Age"] <= hi)]
    return dff


# ── KPI helpers ──────────────────────────────────────────────────────────────
def kpi_metric(col, label: str, value: str, delta: str = "", delta_color: str = "normal"):
    col.metric(label=label, value=value, delta=delta if delta else None,
               delta_color=delta_color)


def pct(num, denom):
    return 0.0 if denom == 0 else round(num / denom * 100, 1)


# ── Plotly theme defaults ─────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    font_family="Inter, sans-serif",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#E2E8F0",
        borderwidth=1,
    ),
    colorway=PALETTE,
)


def style_layout(fig, title: str = "", height: int = 380):
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text=title, font=dict(size=14, color=NAVY), x=0.01),
        height=height,
        xaxis=dict(showgrid=True, gridcolor="#E2E8F0", zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", zeroline=False),
    )
    return fig
