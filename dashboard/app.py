import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from dashboard.db import (
    kpis, monthly_revenue, top_categories,
    delivery_by_state, delivery_status_summary,
    customer_segments, ltv_distribution,
    seller_performance, review_trends,
)

st.set_page_config(
    page_title="Olist E-Commerce Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

TEAL   = "#2a9d8f"
ORANGE = "#e76f51"
BLUE   = "#264653"
YELLOW = "#e9c46a"
GREEN  = "#52b788"

st.markdown("""
<style>
    .metric-card {
        background: #1e1e2e;
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 4px solid #2a9d8f;
    }
    .block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🛒 Olist Analytics")
    st.caption("Brazilian E-Commerce · 2016–2018")
    st.divider()
    page = st.radio(
        "Navigate",
        ["Overview", "Revenue", "Delivery", "Customers", "Sellers", "Reviews"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Stack: DuckDB · dbt · Streamlit")
    st.caption("Models: 13 · Tests: 54 ✅")

# ── Load KPIs (cached) ─────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def get_kpis():
    return kpis()

k = get_kpis()

# ══════════════════════════════════════════════════════════════════════════════
#  OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "Overview":
    st.title("📊 Overview")
    st.caption("Key metrics across all delivered orders")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Total Revenue",   f"${k['total_revenue']:,.0f}")
    c2.metric("📦 Total Orders",    f"{k['total_orders']:,}")
    c3.metric("👥 Customers",       f"{k['total_customers']:,}")
    c4.metric("⭐ Avg Review",      f"{k['avg_review_score']}/5.0")

    c5, c6, c7 = st.columns(3)
    c5.metric("🛒 Avg Order Value", f"${k['avg_order_value']:,.2f}")
    c6.metric("🚚 Avg Delivery",    f"{k['avg_delivery_days']} days")
    c7.metric("✅ On-Time Rate",    f"{k['on_time_pct']}%")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Monthly Revenue")
        df = monthly_revenue()
        fig = px.area(df, x="order_month", y="revenue",
                      color_discrete_sequence=[TEAL])
        fig.update_layout(xaxis_title="", yaxis_title="Revenue ($)",
                          plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top 10 Categories by Revenue")
        df = top_categories(10)
        fig = px.bar(df, x="revenue", y="category_name",
                     orientation="h",
                     color_discrete_sequence=[ORANGE])
        fig.update_layout(yaxis=dict(autorange="reversed"),
                          xaxis_title="Revenue ($)", yaxis_title="",
                          plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  REVENUE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Revenue":
    st.title("💰 Revenue Analysis")

    df_monthly = monthly_revenue()
    df_cat     = top_categories(15)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(df_monthly, x="order_month", y="revenue",
                      title="Monthly Gross Revenue",
                      color_discrete_sequence=[TEAL], markers=True)
        fig.update_layout(xaxis_title="", yaxis_title="Revenue ($)",
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(df_monthly, x="order_month", y="orders",
                     title="Monthly Order Volume",
                     color_discrete_sequence=[YELLOW])
        fig.update_layout(xaxis_title="", yaxis_title="Orders",
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Revenue by Category (Top 15)")
    fig = px.bar(df_cat, x="category_name", y="revenue",
                 color="orders",
                 color_continuous_scale="Teal",
                 labels={"revenue": "Revenue ($)", "orders": "Orders"})
    fig.update_layout(xaxis_tickangle=-35,
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  DELIVERY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Delivery":
    st.title("🚚 Delivery Analysis")

    col1, col2 = st.columns(2)
    with col1:
        df_status = delivery_status_summary()
        fig = px.pie(df_status, names="delivery_status", values="orders",
                     title="On-Time vs Late Deliveries",
                     color="delivery_status",
                     color_discrete_map={"on_time": GREEN, "late": ORANGE},
                     hole=0.45)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_state = delivery_by_state()
        fig = px.bar(df_state, x="avg_days", y="customer_state",
                     orientation="h",
                     title="Avg Delivery Days by State (Top 15 Slowest)",
                     color="avg_days", color_continuous_scale="RdYlGn_r",
                     labels={"avg_days": "Avg Days", "customer_state": "State"})
        fig.update_layout(yaxis=dict(autorange="reversed"),
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("On-Time Rate by State")
    df_state = delivery_by_state().sort_values("on_time_pct", ascending=False)
    fig = px.bar(df_state, x="customer_state", y="on_time_pct",
                 color="on_time_pct", color_continuous_scale="RdYlGn",
                 labels={"on_time_pct": "On-Time %", "customer_state": "State"})
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  CUSTOMERS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Customers":
    st.title("👥 Customer Analysis")

    col1, col2 = st.columns(2)
    with col1:
        df_seg = customer_segments()
        fig = px.pie(df_seg, names="customer_segment", values="customers",
                     title="Customer Segments",
                     color_discrete_sequence=[TEAL, YELLOW, ORANGE],
                     hole=0.4)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_ltv = ltv_distribution()
        fig = px.bar(df_ltv, x="ltv_quintile", y="avg_ltv",
                     title="Avg LTV by Quintile",
                     color="ltv_quintile",
                     color_continuous_scale="Teal",
                     labels={"ltv_quintile": "LTV Quintile", "avg_ltv": "Avg LTV ($)"})
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Segment Summary")
    df_seg["avg_ltv"] = df_seg["avg_ltv"].apply(lambda x: f"${x:,.2f}")
    df_seg["customers"] = df_seg["customers"].apply(lambda x: f"{x:,}")
    st.dataframe(df_seg, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SELLERS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Sellers":
    st.title("🏪 Seller Performance")

    df_sel = seller_performance()

    fig = px.scatter(df_sel,
                     x="total_revenue",
                     y="avg_review_score",
                     size="total_orders",
                     color="revenue_quartile",
                     color_continuous_scale="Teal",
                     title="Revenue vs Rating (bubble = order volume)",
                     labels={
                         "total_revenue": "Total Revenue ($)",
                         "avg_review_score": "Avg Review Score",
                         "revenue_quartile": "Quartile",
                     },
                     hover_data=["seller_state", "total_orders"])
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 10 Sellers by Revenue")
        top10 = df_sel.head(10)[["seller_id", "seller_state", "total_orders",
                                  "total_revenue", "avg_review_score"]]
        top10["seller_id"] = top10["seller_id"].str[:8] + "..."
        top10["total_revenue"] = top10["total_revenue"].apply(lambda x: f"${x:,.0f}")
        st.dataframe(top10, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("Sellers by State")
        by_state = (df_sel.groupby("seller_state")
                    .agg(sellers=("seller_id","count"),
                         avg_revenue=("total_revenue","mean"))
                    .reset_index()
                    .sort_values("sellers", ascending=False)
                    .head(10))
        fig2 = px.bar(by_state, x="seller_state", y="sellers",
                      color="avg_revenue", color_continuous_scale="Teal",
                      labels={"seller_state": "State", "sellers": "# Sellers"})
        fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  REVIEWS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Reviews":
    st.title("⭐ Review Trends")

    df_rev = review_trends()

    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(df_rev, x="review_month", y="avg_score",
                      title="Average Review Score Over Time",
                      color_discrete_sequence=[YELLOW], markers=True)
        fig.update_layout(yaxis=dict(range=[3.5, 5.0]),
                          xaxis_title="", yaxis_title="Avg Score",
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(df_rev, x="review_month", y="total_reviews",
                     title="Review Volume Over Time",
                     color_discrete_sequence=[TEAL])
        fig.update_layout(xaxis_title="", yaxis_title="Reviews",
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    fig = px.area(df_rev, x="review_month", y="positive_pct",
                  title="Positive Review Rate (%) Over Time",
                  color_discrete_sequence=[GREEN])
    fig.update_layout(yaxis=dict(range=[50, 100]),
                      xaxis_title="", yaxis_title="Positive %",
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
