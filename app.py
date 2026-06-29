"""
app.py — Main entry point
E-Commerce Conversion & Sales Pipeline Analytics Dashboard
Run: streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="E-Commerce Conversion Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #1E3A5F; }
    [data-testid="stSidebar"] * { color: #E2E8F0 !important; }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stSlider label { color: #CBD5E1 !important; font-size: 0.82rem; }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 14px 18px;
    }
    [data-testid="stMetricLabel"] { font-size: 0.78rem; color: #64748B; }
    [data-testid="stMetricValue"] { font-size: 1.65rem; font-weight: 700; color: #1E3A5F; }

    /* Page title */
    .dash-title {
        font-size: 1.55rem; font-weight: 700; color: #1E3A5F;
        border-left: 5px solid #2563EB;
        padding-left: 12px; margin-bottom: 4px;
    }
    .dash-sub { font-size: 0.88rem; color: #64748B; margin-bottom: 18px; }

    /* Section headers */
    .section-header {
        font-size: 1.05rem; font-weight: 600; color: #1E3A5F;
        padding: 6px 0; border-bottom: 2px solid #E2E8F0;
        margin: 20px 0 12px 0;
    }

    /* Insight box */
    .insight-box {
        background: #EFF6FF; border-left: 4px solid #2563EB;
        border-radius: 6px; padding: 10px 14px;
        font-size: 0.84rem; color: #1E3A5F; margin: 8px 0;
    }

    /* Hide Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        background: #F1F5F9; border-radius: 8px 8px 0 0;
        padding: 8px 20px; font-weight: 500; color: #475569;
    }
    .stTabs [aria-selected="true"] {
        background: #2563EB !important; color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Imports ───────────────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils import (
    load_data, apply_filters, pct, style_layout,
    PALETTE, FUNNEL_COLORS, TRAFFIC_COLORS, DEVICE_COLORS,
    BLUE, RED, GREEN, AMBER, PURPLE, PINK, NAVY, LGRAY,
)

# ── Load data ─────────────────────────────────────────────────────────────────
df_full = load_data("ecommerce_cleaned.csv")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛒 Dashboard")
    st.markdown("**E-Commerce Conversion Analytics**")
    st.markdown("---")

    st.markdown("### 🎛️ Global Filters")

    sel_traffic = st.multiselect(
        "Traffic Source",
        options=sorted(df_full["Traffic_Source"].unique()),
        default=sorted(df_full["Traffic_Source"].unique()),
    )
    sel_device = st.multiselect(
        "Device Type",
        options=sorted(df_full["Device_Type"].unique()),
        default=sorted(df_full["Device_Type"].unique()),
    )
    sel_category = st.multiselect(
        "Product Category",
        options=sorted(df_full["Product_Category"].unique()),
        default=sorted(df_full["Product_Category"].unique()),
    )
    sel_location = st.multiselect(
        "Location",
        options=sorted(df_full["Location"].unique()),
        default=sorted(df_full["Location"].unique()),
    )
    sel_payment = st.multiselect(
        "Payment Method",
        options=sorted(df_full["Payment_Method"].unique()),
        default=sorted(df_full["Payment_Method"].unique()),
    )
    sel_return = st.selectbox(
        "Customer Type",
        ["All", "Yes", "No"],
        format_func=lambda x: {"All": "All Customers", "Yes": "Return Only", "No": "New Only"}[x],
    )
    age_lo, age_hi = int(df_full["Age"].min()), int(df_full["Age"].max())
    sel_age = st.slider("Age Range", age_lo, age_hi, (age_lo, age_hi))

    st.markdown("---")
    st.caption(f"SP Jain Global | MBA Data Analytics | Term 2")

# Apply filters
filters = dict(
    traffic=sel_traffic, device=sel_device, category=sel_category,
    location=sel_location, payment=sel_payment,
    return_customer=sel_return, age_range=sel_age,
)
df = apply_filters(df_full, filters)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown('<div class="dash-title">🛒 E-Commerce Conversion & Sales Pipeline</div>', unsafe_allow_html=True)
st.markdown('<div class="dash-sub">Descriptive & Diagnostic Analytics | Real-time Filterable Dashboard</div>', unsafe_allow_html=True)

n       = len(df)
n_full  = len(df_full)
if n == 0:
    st.warning("No data matches current filters. Please adjust the sidebar.")
    st.stop()

st.caption(f"Showing **{n:,}** of **{n_full:,}** records ({n/n_full*100:.1f}%)")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview & KPIs",
    "🔽 Funnel Analysis",
    "📣 Traffic & Channels",
    "🛍️ Products & Revenue",
    "🔬 Diagnostic Deep-Dive",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW & KPIs
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    # ── KPI row ──────────────────────────────────────────────────────────────
    conv_n   = (df["Converted"] == "Yes").sum()
    cart_n   = (df["Added_to_Cart"] == "Yes").sum()
    ret_n    = (df["Return_Customer"] == "Yes").sum()
    avg_ov   = df["Order_Value"].mean()
    disc_n   = (df["Discount_Code_Used"] == "Yes").sum()
    avg_sess = df["Session_Count"].mean()

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Conversion Rate",  f"{pct(conv_n, n):.1f}%")
    k2.metric("Cart Add Rate",    f"{pct(cart_n, n):.1f}%")
    k3.metric("Return Customers", f"{pct(ret_n, n):.1f}%")
    k4.metric("Avg Order Value",  f"${avg_ov:.0f}" if not np.isnan(avg_ov) else "—")
    k5.metric("Discount Usage",   f"{pct(disc_n, n):.1f}%")
    k6.metric("Avg Sessions",     f"{avg_sess:.1f}")

    st.markdown("---")
    c1, c2 = st.columns(2)

    # Converted pie
    with c1:
        conv_counts = df["Converted"].value_counts()
        fig = px.pie(
            values=conv_counts.values,
            names=conv_counts.index,
            color=conv_counts.index,
            color_discrete_map={"Yes": GREEN, "No": RED},
            hole=0.55,
        )
        fig.update_traces(textinfo="percent+label", textfont_size=13)
        style_layout(fig, "Conversion Split", height=320)
        st.plotly_chart(fig, use_container_width=True)

    # Gender × Conversion
    with c2:
        g_conv = (
            df.groupby(["Gender", "Converted"])
            .size()
            .reset_index(name="count")
        )
        fig = px.bar(
            g_conv, x="Gender", y="count", color="Converted",
            color_discrete_map={"Yes": GREEN, "No": RED},
            barmode="group", text_auto=True,
        )
        style_layout(fig, "Gender × Conversion Volume", height=320)
        fig.update_traces(textfont_size=11)
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)

    # Age histogram
    with c3:
        fig = px.histogram(
            df, x="Age", color="Converted",
            color_discrete_map={"Yes": GREEN, "No": RED},
            nbins=25, barmode="overlay", opacity=0.75,
        )
        fig.add_vline(x=df["Age"].median(), line_dash="dash",
                      line_color=NAVY, annotation_text=f"Median={df['Age'].median():.0f}")
        style_layout(fig, "Age Distribution by Conversion", height=320)
        st.plotly_chart(fig, use_container_width=True)

    # Time of Day
    with c4:
        tod_order = ["Morning", "Afternoon", "Evening", "Night"]
        tod_conv = (
            df.groupby("Time_of_Day")["Converted_bin"]
            .mean()
            .mul(100)
            .reindex(tod_order)
            .reset_index()
        )
        tod_conv.columns = ["Time_of_Day", "Conv_Rate"]
        fig = px.bar(
            tod_conv, x="Time_of_Day", y="Conv_Rate",
            color="Conv_Rate", color_continuous_scale="Blues",
            text=tod_conv["Conv_Rate"].apply(lambda v: f"{v:.1f}%"),
        )
        fig.update_traces(textposition="outside", textfont_size=11)
        fig.update_layout(coloraxis_showscale=False)
        style_layout(fig, "Conversion Rate by Time of Day (%)", height=320)
        st.plotly_chart(fig, use_container_width=True)

    # Return vs New
    st.markdown('<div class="section-header">New vs Return Customer Comparison</div>', unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)

    ret_conv = df.groupby("Return_Customer")["Converted_bin"].mean().mul(100)
    ret_disc = df.groupby("Return_Customer")["Discount_bin"].mean().mul(100)
    ret_ov   = df.groupby("Return_Customer")["Order_Value"].mean()

    for col_st, title, series, fmt in [
        (r1, "Conversion Rate (%)", ret_conv, "{:.1f}%"),
        (r2, "Discount Usage (%)",  ret_disc, "{:.1f}%"),
        (r3, "Avg Order Value ($)", ret_ov,   "${:.0f}"),
    ]:
        fig = px.bar(
            x=series.index, y=series.values,
            color=series.index,
            color_discrete_map={"Yes": GREEN, "No": RED},
            text=[fmt.format(v) for v in series.values],
        )
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(showlegend=False)
        style_layout(fig, title, height=280)
        col_st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — FUNNEL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Checkout Funnel Drop-off Waterfall</div>', unsafe_allow_html=True)

    total         = n
    cart          = (df["Added_to_Cart"] == "Yes").sum()
    reach_checkout= df["Abandonment_Point"].isin(["Checkout", "Payment Gateway", "None"]).sum()
    reach_payment = df["Abandonment_Point"].isin(["Payment Gateway", "None"]).sum()
    converted     = (df["Converted"] == "Yes").sum()

    stages  = ["Visited Site", "Added to Cart", "Reached Checkout", "Reached Payment", "Converted"]
    counts  = [total, cart, reach_checkout, reach_payment, converted]
    drops   = [0] + [counts[i-1] - counts[i] for i in range(1, len(counts))]
    colors_funnel = [BLUE, GREEN, AMBER, PURPLE, GREEN]

    fig = go.Figure()
    for i, (stage, count, color) in enumerate(zip(stages, counts, colors_funnel)):
        fig.add_trace(go.Bar(
            x=[stage], y=[count], marker_color=color,
            text=f"{count:,}<br>({count/total*100:.1f}%)",
            textposition="outside", textfont=dict(size=12, color=NAVY),
            showlegend=False,
        ))
        if i > 0:
            drop_pct = (counts[i-1] - count) / counts[i-1] * 100
            fig.add_annotation(
                x=stage, y=count + total * 0.04,
                text=f"▼ {drop_pct:.0f}% drop",
                showarrow=False, font=dict(color=RED, size=11, family="Inter"),
            )

    style_layout(fig, "Checkout Funnel — Stage-by-Stage Drop-off", height=420)
    fig.update_layout(yaxis_title="Number of Users", bargap=0.3)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="insight-box">💡 <b>Insight:</b> The largest drop occurs at the Cart-to-Checkout transition. '
                'Optimising checkout UX and offering guest checkout can recover significant revenue.</div>',
                unsafe_allow_html=True)

    # ── Abandonment breakdown ──────────────────────────────────────────────
    st.markdown('<div class="section-header">Abandonment Point Breakdown</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        ab_order = ["Product Page", "Cart", "Checkout", "Payment Gateway"]
        ab_df = df[df["Abandonment_Point"].isin(ab_order)]["Abandonment_Point"].value_counts().reindex(ab_order).fillna(0).reset_index()
        ab_df.columns = ["Stage", "Count"]
        fig = px.funnel(ab_df, x="Count", y="Stage",
                        color_discrete_sequence=[RED, AMBER, BLUE, PURPLE])
        style_layout(fig, "Abandonment Funnel", height=320)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        ab_dev = (
            df[df["Abandonment_Point"].isin(ab_order)]
            .groupby(["Device_Type", "Abandonment_Point"])
            .size()
            .reset_index(name="count")
        )
        fig = px.bar(
            ab_dev, x="Device_Type", y="count", color="Abandonment_Point",
            color_discrete_map=FUNNEL_COLORS,
            barmode="stack", text_auto=False,
        )
        style_layout(fig, "Abandonment by Stage & Device", height=320)
        st.plotly_chart(fig, use_container_width=True)

    # ── Cross-tab: Traffic × Abandonment ──────────────────────────────────
    st.markdown('<div class="section-header">Traffic Source × Abandonment Stage (Heatmap)</div>', unsafe_allow_html=True)
    pivot = (
        df[df["Abandonment_Point"].isin(ab_order)]
        .groupby(["Traffic_Source", "Abandonment_Point"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=ab_order, fill_value=0)
    )
    fig = px.imshow(
        pivot, text_auto=True, color_continuous_scale="Reds",
        aspect="auto",
    )
    style_layout(fig, "Traffic Source × Abandonment Stage Count", height=320)
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TRAFFIC & CHANNELS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Traffic Source Performance</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        ts_conv = (
            df.groupby("Traffic_Source")
            .agg(Total=("Converted", "count"),
                 Converted=("Converted_bin", "sum"))
            .reset_index()
        )
        ts_conv["Conv_Rate"] = ts_conv["Converted"] / ts_conv["Total"] * 100
        ts_conv = ts_conv.sort_values("Conv_Rate", ascending=True)

        fig = px.bar(
            ts_conv, y="Traffic_Source", x="Conv_Rate",
            orientation="h",
            color="Conv_Rate", color_continuous_scale="RdYlGn",
            text=ts_conv["Conv_Rate"].apply(lambda v: f"{v:.1f}%"),
        )
        fig.update_traces(textposition="outside", textfont_size=11)
        fig.update_layout(coloraxis_showscale=False)
        style_layout(fig, "Conversion Rate by Traffic Source (%)", height=360)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        ts_vol = (
            df.groupby(["Traffic_Source", "Converted"])
            .size()
            .reset_index(name="count")
        )
        fig = px.bar(
            ts_vol, x="Traffic_Source", y="count", color="Converted",
            color_discrete_map={"Yes": GREEN, "No": RED},
            barmode="stack",
        )
        style_layout(fig, "Traffic Source Volume (Stacked)", height=360)
        fig.update_layout(xaxis_tickangle=-25)
        st.plotly_chart(fig, use_container_width=True)

    # ── Heatmap: Traffic × Device Conversion Rate ──────────────────────────
    st.markdown('<div class="section-header">Traffic Source × Device Type Conversion Heatmap</div>', unsafe_allow_html=True)
    pivot_td = (
        df.groupby(["Traffic_Source", "Device_Type"])["Converted_bin"]
        .mean()
        .mul(100)
        .unstack()
        .fillna(0)
    )
    fig = px.imshow(
        pivot_td, text_auto=".1f", color_continuous_scale="YlOrRd",
        aspect="auto", zmin=0, zmax=40,
    )
    fig.update_traces(textfont_size=13)
    style_layout(fig, "Conversion Rate (%) — Traffic × Device", height=320)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="insight-box">💡 <b>Insight:</b> Email traffic to Desktop converts best. '
                'Social Media on Mobile has the lowest conversion — focus on mobile-optimised landing pages for paid social.</div>',
                unsafe_allow_html=True)

    # ── Device breakdown ──────────────────────────────────────────────────
    st.markdown('<div class="section-header">Device Type Analysis</div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)

    dev_conv = df.groupby("Device_Type")["Converted_bin"].mean().mul(100).sort_values(ascending=False).reset_index()
    dev_conv.columns = ["Device_Type", "Conv_Rate"]
    fig = px.bar(dev_conv, x="Device_Type", y="Conv_Rate",
                 color="Device_Type",
                 color_discrete_map=DEVICE_COLORS,
                 text=dev_conv["Conv_Rate"].apply(lambda v: f"{v:.1f}%"))
    fig.update_traces(textposition="outside", textfont_size=12)
    fig.update_layout(showlegend=False)
    style_layout(fig, "Conversion Rate by Device (%)", height=300)
    d1.plotly_chart(fig, use_container_width=True)

    dev_time = df.groupby("Device_Type")["Time_Spent_on_Site"].mean().sort_values(ascending=False).reset_index()
    dev_time.columns = ["Device_Type", "Avg_Time"]
    fig = px.bar(dev_time, x="Device_Type", y="Avg_Time",
                 color="Device_Type", color_discrete_map=DEVICE_COLORS,
                 text=dev_time["Avg_Time"].apply(lambda v: f"{v:.1f}m"))
    fig.update_traces(textposition="outside", textfont_size=12)
    fig.update_layout(showlegend=False)
    style_layout(fig, "Avg Time Spent by Device (min)", height=300)
    d2.plotly_chart(fig, use_container_width=True)

    dev_pages = df.groupby("Device_Type")["Pages_Viewed"].mean().sort_values(ascending=False).reset_index()
    dev_pages.columns = ["Device_Type", "Avg_Pages"]
    fig = px.bar(dev_pages, x="Device_Type", y="Avg_Pages",
                 color="Device_Type", color_discrete_map=DEVICE_COLORS,
                 text=dev_pages["Avg_Pages"].apply(lambda v: f"{v:.1f}"))
    fig.update_traces(textposition="outside", textfont_size=12)
    fig.update_layout(showlegend=False)
    style_layout(fig, "Avg Pages Viewed by Device", height=300)
    d3.plotly_chart(fig, use_container_width=True)

    # ── Location map / bar ────────────────────────────────────────────────
    st.markdown('<div class="section-header">Location Performance</div>', unsafe_allow_html=True)
    loc_df = (
        df.groupby("Location")
        .agg(
            Total=("Converted", "count"),
            Conversions=("Converted_bin", "sum"),
            Avg_Order=("Order_Value", "mean"),
        )
        .reset_index()
    )
    loc_df["Conv_Rate"] = loc_df["Conversions"] / loc_df["Total"] * 100
    loc_df = loc_df.sort_values("Conv_Rate", ascending=False)

    fig = px.bar(
        loc_df, x="Location", y="Conv_Rate",
        color="Avg_Order", color_continuous_scale="Blues",
        text=loc_df["Conv_Rate"].apply(lambda v: f"{v:.1f}%"),
    )
    fig.update_traces(textposition="outside", textfont_size=10)
    style_layout(fig, "Conversion Rate by Location (colour = Avg Order Value)", height=340)
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — PRODUCTS & REVENUE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Product Category Performance</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    cat_df = (
        df.groupby("Product_Category")
        .agg(
            Count=("Converted", "count"),
            Conv_Rate=("Converted_bin", "mean"),
            AOV=("Order_Value", "mean"),
            Avg_Pages=("Pages_Viewed", "mean"),
            Avg_Time=("Time_Spent_on_Site", "mean"),
        )
        .reset_index()
    )
    cat_df["Conv_Rate"] = cat_df["Conv_Rate"] * 100
    cat_df = cat_df.sort_values("Conv_Rate", ascending=True)

    with c1:
        fig = px.bar(cat_df, y="Product_Category", x="Conv_Rate",
                     orientation="h",
                     color="Conv_Rate", color_continuous_scale="RdYlGn",
                     text=cat_df["Conv_Rate"].apply(lambda v: f"{v:.1f}%"))
        fig.update_traces(textposition="outside", textfont_size=10)
        fig.update_layout(coloraxis_showscale=False)
        style_layout(fig, "Conversion Rate by Category (%)", height=360)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        cat_aov = cat_df.sort_values("AOV", ascending=True)
        fig = px.bar(cat_aov, y="Product_Category", x="AOV",
                     orientation="h",
                     color="AOV", color_continuous_scale="Blues",
                     text=cat_aov["AOV"].apply(lambda v: f"${v:.0f}" if not np.isnan(v) else "—"))
        fig.update_traces(textposition="outside", textfont_size=10)
        fig.update_layout(coloraxis_showscale=False)
        style_layout(fig, "Average Order Value by Category ($)", height=360)
        st.plotly_chart(fig, use_container_width=True)

    # ── Bubble chart: Category Friction ───────────────────────────────────
    st.markdown('<div class="section-header">Category Friction Index (Avg Time Per Page vs Conversion)</div>', unsafe_allow_html=True)
    df["Avg_Time_Per_Page"] = df["Time_Spent_on_Site"] / (df["Pages_Viewed"] + 1)
    cat_friction = (
        df.groupby("Product_Category")
        .agg(
            Avg_Time_Per_Page=("Avg_Time_Per_Page", "mean"),
            Conv_Rate=("Converted_bin", "mean"),
            AOV=("Order_Value", "mean"),
        )
        .reset_index()
    )
    cat_friction["Conv_Rate"] *= 100

    fig = px.scatter(
        cat_friction,
        x="Avg_Time_Per_Page", y="Conv_Rate",
        size="AOV", color="Product_Category",
        color_discrete_sequence=PALETTE,
        text="Product_Category",
        size_max=50,
    )
    fig.update_traces(textposition="top center", textfont_size=10)
    style_layout(fig, "Friction Index: Avg Time Per Page vs Conversion Rate (Bubble = AOV)", height=420)
    fig.update_layout(xaxis_title="Avg Time Per Page (min) — Higher = More Friction",
                      yaxis_title="Conversion Rate (%)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="insight-box">💡 <b>Insight:</b> Categories with high time-per-page but low conversion '
                '(e.g. Electronics) indicate research-heavy shoppers who need stronger social proof and comparison tools.</div>',
                unsafe_allow_html=True)

    # ── Order value distribution & Payment ────────────────────────────────
    st.markdown('<div class="section-header">Order Value & Payment Method</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    df_conv_filt = df[df["Converted"] == "Yes"]

    with c1:
        fig = px.histogram(df_conv_filt, x="Order_Value",
                           nbins=35, color_discrete_sequence=[BLUE])
        fig.add_vline(x=df_conv_filt["Order_Value"].mean(), line_dash="dash",
                      line_color=RED,
                      annotation_text=f"Mean=${df_conv_filt['Order_Value'].mean():.0f}")
        style_layout(fig, "Order Value Distribution", height=300)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        pay_counts = df["Payment_Method"].value_counts().reset_index()
        pay_counts.columns = ["Method", "Count"]
        fig = px.pie(pay_counts, values="Count", names="Method",
                     color_discrete_sequence=PALETTE, hole=0.5)
        fig.update_traces(textinfo="percent+label", textfont_size=11)
        style_layout(fig, "Payment Method Share", height=300)
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        pay_aov = (
            df[df["Converted"] == "Yes"]
            .groupby("Payment_Method")["Order_Value"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )
        pay_aov.columns = ["Method", "AOV"]
        fig = px.bar(pay_aov, x="Method", y="AOV",
                     color="AOV", color_continuous_scale="Blues",
                     text=pay_aov["AOV"].apply(lambda v: f"${v:.0f}"))
        fig.update_traces(textposition="outside", textfont_size=11)
        fig.update_layout(coloraxis_showscale=False)
        style_layout(fig, "AOV by Payment Method ($)", height=300)
        fig.update_layout(xaxis_tickangle=-20)
        st.plotly_chart(fig, use_container_width=True)

    # ── Category × Traffic heatmap ────────────────────────────────────────
    st.markdown('<div class="section-header">Product Category × Traffic Source Conversion Heatmap</div>', unsafe_allow_html=True)
    pivot_ct = (
        df.groupby(["Product_Category", "Traffic_Source"])["Converted_bin"]
        .mean()
        .mul(100)
        .unstack()
        .fillna(0)
    )
    fig = px.imshow(
        pivot_ct, text_auto=".1f",
        color_continuous_scale="YlOrRd", aspect="auto", zmin=0,
    )
    fig.update_traces(textfont_size=11)
    style_layout(fig, "Conversion Rate (%) — Category × Traffic Source", height=380)
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — DIAGNOSTIC DEEP-DIVE
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">Engagement Metrics — Distribution & Skewness</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    for col_st, metric, title in [
        (c1, "Time_Spent_on_Site", "Time Spent on Site (min)"),
        (c2, "Pages_Viewed",        "Pages Viewed"),
        (c3, "Session_Count",       "Session Count"),
    ]:
        data = df[metric].dropna()
        skew_val = data.skew()
        fig = px.histogram(df, x=metric, color="Converted",
                           color_discrete_map={"Yes": GREEN, "No": RED},
                           nbins=30, barmode="overlay", opacity=0.72)
        fig.add_vline(x=data.mean(), line_dash="dash", line_color=NAVY,
                      annotation_text=f"μ={data.mean():.1f}")
        style_layout(fig, f"{title} | Skew={skew_val:.2f}", height=300)
        col_st.plotly_chart(fig, use_container_width=True)

    # ── Engagement vs Conversion scatter ──────────────────────────────────
    st.markdown('<div class="section-header">Engagement Score vs Order Value (Converted Only)</div>', unsafe_allow_html=True)
    df_c = df[df["Converted"] == "Yes"].copy()
    df_c["Engagement_Score"] = df_c["Time_Spent_on_Site"] * df_c["Pages_Viewed"]

    if len(df_c) > 0:
        fig = px.scatter(
            df_c, x="Engagement_Score", y="Order_Value",
            color="Product_Category",
            color_discrete_sequence=PALETTE,
            hover_data=["Traffic_Source", "Device_Type", "Payment_Method"],
            opacity=0.7, size_max=10,
        )
        style_layout(fig, "Engagement Score (Time × Pages) vs Order Value — Converted Customers", height=420)
        fig.update_layout(xaxis_title="Engagement Score", yaxis_title="Order Value ($)")
        st.plotly_chart(fig, use_container_width=True)

    # ── Correlation heatmap ────────────────────────────────────────────────
    st.markdown('<div class="section-header">Correlation Heatmap — Key Numeric Metrics</div>', unsafe_allow_html=True)
    corr_cols = ["Converted_bin", "Age", "Session_Count", "Time_Spent_on_Site",
                 "Pages_Viewed", "Engagement_Score", "Avg_Time_Per_Page",
                 "Return_bin", "Discount_bin", "Cart_bin"]
    corr_df = df[corr_cols].dropna()
    corr_mat = corr_df.corr().round(2)

    import plotly.figure_factory as ff
    fig = ff.create_annotated_heatmap(
        z=corr_mat.values,
        x=corr_mat.columns.tolist(),
        y=corr_mat.index.tolist(),
        colorscale="RdYlGn",
        showscale=True,
        annotation_text=corr_mat.values.round(2),
    )
    style_layout(fig, "Correlation Matrix — Engagement & Conversion Metrics", height=480)
    st.plotly_chart(fig, use_container_width=True)

    # ── Session Count × Conversion violin ─────────────────────────────────
    st.markdown('<div class="section-header">Session Depth vs Conversion — Violin Charts</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    for col_st, metric, title in [
        (c1, "Session_Count",       "Session Count"),
        (c2, "Time_Spent_on_Site",  "Time Spent on Site (min)"),
    ]:
        fig = px.violin(
            df, y=metric, x="Converted", color="Converted",
            color_discrete_map={"Yes": GREEN, "No": RED},
            box=True, points=False,
        )
        style_layout(fig, f"{title} by Conversion Outcome", height=340)
        col_st.plotly_chart(fig, use_container_width=True)

    # ── Discount impact ────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Discount Code Impact Analysis</div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)

    disc_conv = df.groupby("Discount_Code_Used")["Converted_bin"].mean().mul(100).reset_index()
    disc_conv.columns = ["Discount", "Conv_Rate"]
    fig = px.bar(disc_conv, x="Discount", y="Conv_Rate",
                 color="Discount", color_discrete_map={"Yes": GREEN, "No": RED},
                 text=disc_conv["Conv_Rate"].apply(lambda v: f"{v:.1f}%"))
    fig.update_traces(textposition="outside", textfont_size=12)
    fig.update_layout(showlegend=False)
    style_layout(fig, "Conversion Rate — Discount vs No Discount", height=280)
    d1.plotly_chart(fig, use_container_width=True)

    disc_aov = df[df["Converted"]=="Yes"].groupby("Discount_Code_Used")["Order_Value"].mean().reset_index()
    disc_aov.columns = ["Discount", "AOV"]
    fig = px.bar(disc_aov, x="Discount", y="AOV",
                 color="Discount", color_discrete_map={"Yes": AMBER, "No": BLUE},
                 text=disc_aov["AOV"].apply(lambda v: f"${v:.0f}"))
    fig.update_traces(textposition="outside", textfont_size=12)
    fig.update_layout(showlegend=False)
    style_layout(fig, "Avg Order Value — Discount vs No Discount", height=280)
    d2.plotly_chart(fig, use_container_width=True)

    disc_by_channel = (
        df.groupby(["Traffic_Source", "Discount_Code_Used"])["Converted_bin"]
        .mean().mul(100).unstack().fillna(0).reset_index()
    )
    disc_melt = disc_by_channel.melt(id_vars="Traffic_Source",
                                      var_name="Discount", value_name="Conv_Rate")
    fig = px.bar(disc_melt, x="Traffic_Source", y="Conv_Rate",
                 color="Discount", color_discrete_map={"Yes": GREEN, "No": RED},
                 barmode="group",
                 text=disc_melt["Conv_Rate"].apply(lambda v: f"{v:.0f}%"))
    fig.update_traces(textposition="outside", textfont_size=9)
    fig.update_layout(xaxis_tickangle=-25)
    style_layout(fig, "Discount vs No Discount Conversion by Channel", height=280)
    d3.plotly_chart(fig, use_container_width=True)

    # ── Raw data explorer ─────────────────────────────────────────────────
    st.markdown('<div class="section-header">📋 Raw Data Explorer</div>', unsafe_allow_html=True)
    st.dataframe(
        df.drop(columns=["Converted_bin", "Return_bin", "Discount_bin",
                          "Cart_bin", "Engagement_Score", "Avg_Time_Per_Page",
                          "High_Engagement"], errors="ignore")
          .reset_index(drop=True),
        use_container_width=True,
        height=400,
    )
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="filtered_ecommerce_data.csv",
        mime="text/csv",
    )
