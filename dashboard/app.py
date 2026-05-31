import streamlit as st
import plotly.express  as px
import plotly.graph_objects as go
impor t sys
import os

sys.path.insert(0, os.path.d irname(os.path.dirname(__file__)))
from dashb oard.db import (
    kpis, monthly_revenue, t op_categories,
    delivery_by_state, deliver y_status_summary,
    customer_segments, ltv_ distribution,
    seller_performance, review_ trends,
)

st.set_page_config(
    page_title ="Olist E-Commerce Analytics",
    page_icon= "🛒",
    layout="wide",
    initial_sideba r_state="expanded",
)

TEAL   = "#2a9d8f"
ORA NGE = "#e76f51"
BLUE   = "#264653"
YELLOW = " #e9c46a"
GREEN  = "#52b788"

st.markdown("""
 <style>
    .metric-card {
        background : #1e1e2e;
        border-radius: 12px;
         padding: 16px 20px;
        border-left: 4 px solid #2a9d8f;
    }
    .block-container  { padding-top: 1.5rem; }
</style>
""", unsafe _allow_html=True)

# ── Sidebar ─── ─────────────── ─────────────── ─────────────── ─────────────── ─────
with st.sidebar:
    st.title ("🛒 Olist Analytics")
    st.caption("Braz ilian E-Commerce · 2016–2018")
    st.divi der()
    page = st.radio(
        "Navigate" ,
        ["Overview", "Revenue", "Delivery",  "Customers", "Sellers", "Reviews"],
         label_visibility="collapsed",
    )
    st.di vider()
    st.caption("Stack: DuckDB · dbt  · Streamlit")
    st.caption("Models: 13 ·  Tests: 54 ✅")

# ── Load KPIs (cached)  ─────────────── ─────────────── ─────────────── ────────────
@st.cach e_data(ttl=300)
def get_kpis():
    return kp is()

try:
    k = get_kpis()
except Exception as e:
    st.error(f"Database error: {type(e).__name__}: {e}")
    st.stop()

# ═══════ ═══════════════ ═══════════════ ═══════════════ ═══════════════ ═══════════
#  OVERVIEW 
# ══════════════ ═══════════════ ═══════════════ ═══════════════ ═══════════════ ════
if page == "Overview":
    st.ti tle("📊 Overview")
    st.caption("Key metr ics across all delivered orders")

    c1, c2 , c3, c4 = st.columns(4)
    c1.metric("💰  Total Revenue",   f"${k['total_revenue']:,.0f }")
    c2.metric("📦 Total Orders",    f"{ k['total_orders']:,}")
    c3.metric("👥 Cu stomers",       f"{k['total_customers']:,}")
     c4.metric("⭐ Avg Review",      f"{k['av g_review_score']}/5.0")

    c5, c6, c7 = st. columns(3)
    c5.metric("🛒 Avg Order Valu e", f"${k['avg_order_value']:,.2f}")
    c6.m etric("🚚 Avg Delivery",    f"{k['avg_deliv ery_days']} days")
    c7.metric("✅ On-Time  Rate",    f"{k['on_time_pct']}%")

    st.di vider()
    col1, col2 = st.columns(2)

    w ith col1:
        st.subheader("Monthly Reven ue")
        df = monthly_revenue()
        f ig = px.area(df, x="order_month", y="revenue" ,
                      color_discrete_sequen ce=[TEAL])
        fig.update_layout(xaxis_ti tle="", yaxis_title="Revenue ($)",
                           plot_bgcolor="rgba(0,0,0,0)", 
                          paper_bgcolor="rgb a(0,0,0,0)")
        st.plotly_chart(fig, use _container_width=True)

    with col2:
         st.subheader("Top 10 Categories by Revenue" )
        df = top_categories(10)
        fig  = px.bar(df, x="revenue", y="category_name", 
                     orientation="h",
                      color_discrete_sequence=[ORANG E])
        fig.update_layout(yaxis=dict(auto range="reversed"),
                           xaxis_title="Revenue ($)", yaxis_title="",
                           plot_bgcolor="rgba(0, 0,0,0)",
                          paper_bgco lor="rgba(0,0,0,0)")
        st.plotly_chart( fig, use_container_width=True)

# ═══� �══════════════� �══════════════� �══════════════� �══════════════� �══════════════
#   REVENUE
# ═══════════ ═══════════════ ═══════════════ ═══════════════ ═══════════════ ═══════
elif page == "Revenue": 
    st.title("💰 Revenue Analysis")

    d f_monthly = monthly_revenue()
    df_cat      = top_categories(15)

    col1, col2 = st.col umns(2)
    with col1:
        fig = px.line( df_monthly, x="order_month", y="revenue",
                       title="Monthly Gross Reven ue",
                      color_discrete_seq uence=[TEAL], markers=True)
        fig.updat e_layout(xaxis_title="", yaxis_title="Revenue  ($)",
                          plot_bgcolor ="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0 )")
        st.plotly_chart(fig, use_containe r_width=True)

    with col2:
        fig = p x.bar(df_monthly, x="order_month", y="orders" ,
                     title="Monthly Order V olume",
                     color_discrete_s equence=[YELLOW])
        fig.update_layout(x axis_title="", yaxis_title="Orders",
                           plot_bgcolor="rgba(0,0,0,0) ", paper_bgcolor="rgba(0,0,0,0)")
        st. plotly_chart(fig, use_container_width=True)

     st.divider()
    st.subheader("Revenue by  Category (Top 15)")
    fig = px.bar(df_cat,  x="category_name", y="revenue",
                  color="orders",
                 color_c ontinuous_scale="Teal",
                 labe ls={"revenue": "Revenue ($)", "orders": "Orde rs"})
    fig.update_layout(xaxis_tickangle=- 35,
                      plot_bgcolor="rgba( 0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
     st.plotly_chart(fig, use_container_width=Tru e)

# ═════════════ ═══════════════ ═══════════════ ═══════════════ ═══════════════ ═════
#  DELIVERY
# ═════ ═══════════════ ═══════════════ ═══════════════ ═══════════════ ═════════════
elif  page == "Delivery":
    st.title("🚚 Delive ry Analysis")

    col1, col2 = st.columns(2) 
    with col1:
        df_status = delivery_ status_summary()
        fig = px.pie(df_stat us, names="delivery_status", values="orders", 
                     title="On-Time vs Late  Deliveries",
                     color="deli very_status",
                     color_disc rete_map={"on_time": GREEN, "late": ORANGE},
                      hole=0.45)
        fig.u pdate_layout(paper_bgcolor="rgba(0,0,0,0)")
         st.plotly_chart(fig, use_container_wid th=True)

    with col2:
        df_state = d elivery_by_state()
        fig = px.bar(df_st ate, x="avg_days", y="customer_state",
                      orientation="h",
                      title="Avg Delivery Days by State (To p 15 Slowest)",
                     color="a vg_days", color_continuous_scale="RdYlGn_r",
                      labels={"avg_days": "Avg  Days", "customer_state": "State"})
        f ig.update_layout(yaxis=dict(autorange="revers ed"),
                          plot_bgcolor= "rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0) ")
        st.plotly_chart(fig, use_container _width=True)

    st.divider()
    st.subhead er("On-Time Rate by State")
    df_state = de livery_by_state().sort_values("on_time_pct",  ascending=False)
    fig = px.bar(df_state, x ="customer_state", y="on_time_pct",
                  color="on_time_pct", color_continuous _scale="RdYlGn",
                 labels={"on _time_pct": "On-Time %", "customer_state": "S tate"})
    fig.update_layout(plot_bgcolor="r gba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)") 
    st.plotly_chart(fig, use_container_width =True)

# ═══════════� �══════════════� �══════════════� �══════════════� �══════════════� �══════
#  CUSTOMERS
# ═══� ��══════════════� ��══════════════� ��══════════════� ��══════════════� ��══════════════
 elif page == "Customers":
    st.title("👥  Customer Analysis")

    col1, col2 = st.colu mns(2)
    with col1:
        df_seg = custom er_segments()
        fig = px.pie(df_seg, na mes="customer_segment", values="customers",
                      title="Customer Segments" ,
                     color_discrete_sequenc e=[TEAL, YELLOW, ORANGE],
                      hole=0.4)
        fig.update_layout(paper_b gcolor="rgba(0,0,0,0)")
        st.plotly_cha rt(fig, use_container_width=True)

    with c ol2:
        df_ltv = ltv_distribution()
         fig = px.bar(df_ltv, x="ltv_quintile", y= "avg_ltv",
                     title="Avg LT V by Quintile",
                     color="l tv_quintile",
                     color_cont inuous_scale="Teal",
                     lab els={"ltv_quintile": "LTV Quintile", "avg_ltv ": "Avg LTV ($)"})
        fig.update_layout( plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor=" rgba(0,0,0,0)")
        st.plotly_chart(fig,  use_container_width=True)

    st.divider()
     st.subheader("Segment Summary")
    df_seg ["avg_ltv"] = df_seg["avg_ltv"].apply(lambda  x: f"${x:,.2f}")
    df_seg["customers"] = df _seg["customers"].apply(lambda x: f"{x:,}")
     st.dataframe(df_seg, use_container_width=T rue, hide_index=True)

# ══════� �══════════════� �══════════════� �══════════════� �══════════════� �═══════════
#  SELLERS 
# ══════════════ ═══════════════ ═══════════════ ═══════════════ ═══════════════ ════
elif page == "Sellers":
    st.t itle("🏪 Seller Performance")

    df_sel =  seller_performance()

    fig = px.scatter(d f_sel,
                     x="total_revenue" ,
                     y="avg_review_score",
                      size="total_orders",
                      color="revenue_quartile",
                      color_continuous_scale="T eal",
                     title="Revenue vs  Rating (bubble = order volume)",
                      labels={
                         "t otal_revenue": "Total Revenue ($)",
                          "avg_review_score": "Avg Revi ew Score",
                         "revenue_ quartile": "Quartile",
                     } ,
                     hover_data=["seller_st ate", "total_orders"])
    fig.update_layout( plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor=" rgba(0,0,0,0)")
    st.plotly_chart(fig, use_ container_width=True)

    st.divider()
    c ol1, col2 = st.columns(2)
    with col1:
         st.subheader("Top 10 Sellers by Revenue") 
        top10 = df_sel.head(10)[["seller_id" , "seller_state", "total_orders",
                                   "total_revenue", "avg_ review_score"]]
        top10["seller_id"] =  top10["seller_id"].str[:8] + "..."
        to p10["total_revenue"] = top10["total_revenue"] .apply(lambda x: f"${x:,.0f}")
        st.dat aframe(top10, use_container_width=True, hide_ index=True)

    with col2:
        st.subhea der("Sellers by State")
        by_state = (d f_sel.groupby("seller_state")
                     .agg(sellers=("seller_id","count"),
                          avg_revenue=("total_reve nue","mean"))
                    .reset_inde x()
                    .sort_values("sellers ", ascending=False)
                    .head (10))
        fig2 = px.bar(by_state, x="sell er_state", y="sellers",
                       color="avg_revenue", color_continuous_scale= "Teal",
                      labels={"seller _state": "State", "sellers": "# Sellers"})
         fig2.update_layout(plot_bgcolor="rgba(0 ,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
         st.plotly_chart(fig2, use_container_width =True)

# ═══════════� �══════════════� �══════════════� �══════════════� �══════════════� �══════
#  REVIEWS
# ════ ═══════════════ ═══════════════ ═══════════════ ═══════════════ ══════════════
el if page == "Reviews":
    st.title("⭐ Revie w Trends")

    df_rev = review_trends()

     col1, col2 = st.columns(2)
    with col1:
         fig = px.line(df_rev, x="review_month",  y="avg_score",
                      title=" Average Review Score Over Time",
                       color_discrete_sequence=[YELLOW], m arkers=True)
        fig.update_layout(yaxis= dict(range=[3.5, 5.0]),
                           xaxis_title="", yaxis_title="Avg Score", 
                          plot_bgcolor="rgba (0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
         st.plotly_chart(fig, use_container_widt h=True)

    with col2:
        fig = px.bar( df_rev, x="review_month", y="total_reviews",
                      title="Review Volume Ove r Time",
                     color_discrete_ sequence=[TEAL])
        fig.update_layout(xa xis_title="", yaxis_title="Reviews",
                           plot_bgcolor="rgba(0,0,0,0) ", paper_bgcolor="rgba(0,0,0,0)")
        st. plotly_chart(fig, use_container_width=True)

     st.divider()
    fig = px.area(df_rev, x= "review_month", y="positive_pct",
                   title="Positive Review Rate (%) Over T ime",
                  color_discrete_sequen ce=[GREEN])
    fig.update_layout(yaxis=dict( range=[50, 100]),
                      xaxis _title="", yaxis_title="Positive %",
                       plot_bgcolor="rgba(0,0,0,0)", p aper_bgcolor="rgba(0,0,0,0)")
    st.plotly_c hart(fig, use_container_width=True)
 