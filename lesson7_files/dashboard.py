import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import data_loader as dl
import business_metrics as bm

# ── Page setup ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    h2 { margin-bottom: 0 !important; }
</style>
""", unsafe_allow_html=True)

CHART_CFG = {"displayModeBar": False}
COLOR_PRIMARY = "#1f4e79"
COLOR_SECONDARY = "#9dc3e6"

MONTH_NAMES = {
    0: "Full Year", 1: "January", 2: "February", 3: "March",
    4: "April", 5: "May", 6: "June", 7: "July",
    8: "August", 9: "September", 10: "October", 11: "November", 12: "December",
}

# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    datasets = dl.load_all("ecommerce_data")
    all_sales = dl.build_sales_data(datasets["orders"], datasets["order_items"])
    delivered = dl.filter_delivered(all_sales)
    delivered = dl.compute_delivery_speed(delivered)
    return datasets["orders"], datasets["products"], datasets["customers"], datasets["reviews"], delivered

orders, products, customers, reviews, delivered = load_data()

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_currency(val: float) -> str:
    if abs(val) >= 1_000_000:
        return f"${val / 1_000_000:.2f}M"
    if abs(val) >= 1_000:
        return f"${val / 1_000:.0f}K"
    return f"${val:.0f}"

def trend_parts(current: float, prior: float, lower_is_better: bool = False):
    """Return (label, hex-color) for a trend vs prior period."""
    if prior == 0 or np.isnan(prior):
        return "no prior data", "#6c757d"
    pct = (current - prior) / prior * 100
    improving = (pct > 0) if not lower_is_better else (pct < 0)
    color = "#28a745" if improving else "#dc3545"
    sign = "+" if pct > 0 else ""
    return f"{sign}{pct:.2f}% vs prior year", color

def stars(score: float, max_score: int = 5) -> str:
    full = min(int(round(score)), max_score)
    return "★" * full + "☆" * (max_score - full)

def kpi_card(col, title: str, value: str, trend_label: str = "", trend_color: str = "#6c757d"):
    with col:
        st.markdown(f"""
        <div style="background:#ffffff; border-radius:10px; padding:18px 22px;
                    border:1px solid #e8e8e8; height:130px; box-sizing:border-box;
                    box-shadow:0 1px 4px rgba(0,0,0,.06);">
            <div style="font-size:11px; color:#888; font-weight:600;
                        text-transform:uppercase; letter-spacing:.7px;">{title}</div>
            <div style="font-size:26px; font-weight:700; color:{COLOR_PRIMARY};
                        margin-top:8px; line-height:1.1;">{value}</div>
            <div style="font-size:13px; color:{trend_color}; margin-top:6px;">{trend_label}</div>
        </div>""", unsafe_allow_html=True)

def bottom_card(col, title: str, value: str, subtitle: str = "", trend_label: str = "", trend_color: str = "#6c757d"):
    with col:
        trend_html = f'<div style="font-size:13px;color:{trend_color};margin-top:5px;">{trend_label}</div>' if trend_label else ""
        sub_html = f'<div style="font-size:13px;color:#888;margin-top:5px;">{subtitle}</div>' if subtitle else ""
        st.markdown(f"""
        <div style="background:#ffffff; border-radius:10px; padding:20px 28px;
                    border:1px solid #e8e8e8; height:140px; box-sizing:border-box;
                    box-shadow:0 1px 4px rgba(0,0,0,.06);">
            <div style="font-size:11px; color:#888; font-weight:600;
                        text-transform:uppercase; letter-spacing:.7px;">{title}</div>
            <div style="font-size:30px; font-weight:700; color:{COLOR_PRIMARY};
                        margin-top:8px; line-height:1.1;">{value}</div>
            {trend_html}{sub_html}
        </div>""", unsafe_allow_html=True)

# ── Header & filters ──────────────────────────────────────────────────────────
hdr_left, hdr_right = st.columns([3, 2])

with hdr_left:
    st.markdown("## E-Commerce Sales Dashboard")

with hdr_right:
    f1, f2 = st.columns(2)
    years = sorted(delivered["year"].dropna().unique().astype(int), reverse=True)
    selected_year = f1.selectbox("Year", years, index=0)
    selected_month_key = f2.selectbox(
        "Month", list(MONTH_NAMES.keys()),
        format_func=lambda k: MONTH_NAMES[k],
    )
    analysis_month = None if selected_month_key == 0 else selected_month_key
    comparison_year = selected_year - 1

# ── Filter data ───────────────────────────────────────────────────────────────
sales_current = dl.filter_by_period(delivered, year=selected_year, month=analysis_month)
sales_prior   = dl.filter_by_period(delivered, year=comparison_year, month=analysis_month)

if len(sales_current) == 0:
    st.warning("No delivered orders found for the selected period.")
    st.stop()

# ── Pre-compute metrics ───────────────────────────────────────────────────────
rev_c   = bm.total_revenue(sales_current)
rev_p   = bm.total_revenue(sales_prior) if len(sales_prior) > 0 else 0
ord_c   = bm.total_orders(sales_current)
ord_p   = bm.total_orders(sales_prior) if len(sales_prior) > 0 else 0
aov_c   = bm.average_order_value(sales_current)
aov_p   = bm.average_order_value(sales_prior) if len(sales_prior) > 0 else 0
dlv_c   = bm.delivery_stats(sales_current)["mean_days"]
dlv_p   = bm.delivery_stats(sales_prior)["mean_days"] if len(sales_prior) > 0 else 0
rev_sc  = bm.average_review_score(sales_current, reviews)

mom_series = bm.monthly_growth_rate(sales_current)["mom_growth"].dropna()
mom_avg = mom_series.mean() if len(mom_series) > 0 else float("nan")

st.markdown("<div style='margin:6px 0 2px'></div>", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

rev_label, rev_color = trend_parts(rev_c, rev_p)
kpi_card(k1, "Total Revenue", fmt_currency(rev_c), rev_label, rev_color)

if np.isnan(mom_avg):
    mom_val, mom_sub = "N/A", "select full year for monthly trend"
else:
    mom_val, mom_sub = f"{mom_avg * 100:+.2f}%", "avg month-over-month"
kpi_card(k2, "Monthly Growth", mom_val, mom_sub)

aov_label, aov_color = trend_parts(aov_c, aov_p)
kpi_card(k3, "Average Order Value", fmt_currency(aov_c), aov_label, aov_color)

ord_label, ord_color = trend_parts(ord_c, ord_p)
kpi_card(k4, "Total Orders", f"{ord_c:,}", ord_label, ord_color)

st.markdown("<div style='margin:14px 0 2px'></div>", unsafe_allow_html=True)

# ── Charts: Row 1 ─────────────────────────────────────────────────────────────
row1_l, row1_r = st.columns(2)

# Revenue trend line chart
with row1_l:
    mr_c = bm.monthly_revenue(sales_current)
    mr_p = bm.monthly_revenue(sales_prior) if len(sales_prior) > 0 else None

    max_rev = mr_c["revenue"].max()
    if mr_p is not None and len(mr_p) > 0:
        max_rev = max(max_rev, mr_p["revenue"].max())
    tick_vals = np.linspace(0, max_rev * 1.15, 6)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=mr_c["month"], y=mr_c["revenue"],
        name=str(selected_year),
        mode="lines+markers",
        line=dict(color=COLOR_PRIMARY, width=2.5),
        marker=dict(size=6),
    ))
    if mr_p is not None and len(mr_p) > 0:
        fig.add_trace(go.Scatter(
            x=mr_p["month"], y=mr_p["revenue"],
            name=str(comparison_year),
            mode="lines+markers",
            line=dict(color=COLOR_SECONDARY, width=2, dash="dash"),
            marker=dict(size=5),
        ))
    fig.update_layout(
        title=f"Monthly Revenue: {selected_year} vs {comparison_year}",
        xaxis_title="Month",
        yaxis_title="Revenue",
        height=340,
        margin=dict(t=44, b=40, l=10, r=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(orientation="h", y=1.12, x=1, xanchor="right"),
        xaxis=dict(showgrid=True, gridcolor="#f0f0f0", dtick=1),
        yaxis=dict(
            showgrid=True, gridcolor="#f0f0f0",
            tickvals=tick_vals,
            ticktext=[fmt_currency(v) for v in tick_vals],
        ),
    )
    st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)

# Top 10 categories bar chart
with row1_r:
    cat_rev = bm.revenue_by_category(sales_current, products).head(10)
    cat_rev = cat_rev.sort_values("revenue", ascending=True)  # ascending so highest is at top of horizontal bar

    n = len(cat_rev)
    blue_gradient = px.colors.sample_colorscale(
        "Blues", [0.25 + 0.75 * i / max(n - 1, 1) for i in range(n)]
    )
    max_cat = cat_rev["revenue"].max()
    tick_vals_cat = np.linspace(0, max_cat * 1.2, 5)

    fig2 = go.Figure(go.Bar(
        x=cat_rev["revenue"],
        y=cat_rev["product_category_name"],
        orientation="h",
        marker_color=blue_gradient,
        text=[fmt_currency(v) for v in cat_rev["revenue"]],
        textposition="outside",
        cliponaxis=False,
    ))
    fig2.update_layout(
        title=f"Top 10 Product Categories ({selected_year})",
        xaxis_title="Revenue",
        yaxis_title="",
        height=340,
        margin=dict(t=44, b=40, l=10, r=80),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(
            showgrid=True, gridcolor="#f0f0f0",
            tickvals=tick_vals_cat,
            ticktext=[fmt_currency(v) for v in tick_vals_cat],
            range=[0, max_cat * 1.3],
        ),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig2, use_container_width=True, config=CHART_CFG)

# ── Charts: Row 2 ─────────────────────────────────────────────────────────────
row2_l, row2_r = st.columns(2)

# Revenue by state choropleth
with row2_l:
    state_rev = bm.revenue_by_state(sales_current, orders, customers)
    fig3 = px.choropleth(
        state_rev,
        locations="customer_state",
        color="revenue",
        locationmode="USA-states",
        scope="usa",
        color_continuous_scale="Blues",
        title=f"Revenue by State ({selected_year})",
        labels={"revenue": "Revenue", "customer_state": "State"},
    )
    fig3.update_coloraxes(
        colorbar=dict(
            tickvals=[state_rev["revenue"].min(), state_rev["revenue"].max()],
            ticktext=[
                fmt_currency(state_rev["revenue"].min()),
                fmt_currency(state_rev["revenue"].max()),
            ],
        )
    )
    fig3.update_layout(
        height=340,
        margin=dict(t=44, b=0, l=0, r=0),
    )
    st.plotly_chart(fig3, use_container_width=True, config=CHART_CFG)

# Satisfaction by delivery time
with row2_r:
    del_review = bm.review_score_by_delivery_bucket(sales_current, reviews)
    fig4 = go.Figure(go.Bar(
        x=del_review["delivery_time"],
        y=del_review["review_score"],
        marker_color=COLOR_PRIMARY,
        text=[f"{v:.2f}" for v in del_review["review_score"]],
        textposition="outside",
    ))
    fig4.update_layout(
        title=f"Customer Satisfaction by Delivery Speed ({selected_year})",
        xaxis_title="Delivery Time",
        yaxis_title="Average Review Score",
        height=340,
        margin=dict(t=44, b=40, l=10, r=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis=dict(
            range=[0, 5.5],
            showgrid=True,
            gridcolor="#f0f0f0",
        ),
        xaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig4, use_container_width=True, config=CHART_CFG)

st.markdown("<div style='margin:4px 0'></div>", unsafe_allow_html=True)

# ── Bottom Row ────────────────────────────────────────────────────────────────
b1, b2 = st.columns(2)

dlv_label, dlv_color = trend_parts(dlv_c, dlv_p, lower_is_better=True)
bottom_card(b1, "Average Delivery Time", f"{dlv_c:.1f} days",
            trend_label=dlv_label, trend_color=dlv_color)

bottom_card(b2, "Review Score",
            f"{rev_sc:.2f}  {stars(rev_sc)}",
            subtitle="Average Review Score")
