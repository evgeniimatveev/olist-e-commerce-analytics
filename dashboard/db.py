import duckdb
import pandas as pd
import os

_ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.environ.get("DB_PATH", os.path.join(_ROOT, "olist.duckdb"))

def query(sql: str) -> pd.DataFrame:
    con = duckdb.connect(DB_PATH, read_only=True)
    df = con.execute(sql).df()
    con.close()
    return df

def kpis() -> dict:
    df = query("""
        select
            round(sum(gross_revenue), 0)            as total_revenue,
            count(distinct order_id)                as total_orders,
            round(avg(gross_revenue / items_count), 2) as avg_order_value
        from main_marts.mart_revenue
    """)
    customers = query("select count(*) as n from main_marts.mart_customer_ltv").iloc[0]["n"]
    delivery = query("""
        select
            round(avg(total_delivery_days), 1) as avg_days,
            round(sum(case when delivery_status='on_time' then 1 end)*100.0/count(*), 1) as on_time_pct
        from main_marts.mart_delivery_analysis
    """)
    reviews = query("select round(avg(avg_score),2) as score from main_marts.mart_reviews").iloc[0]["score"]
    return {
        "total_revenue":   df.iloc[0]["total_revenue"],
        "total_orders":    df.iloc[0]["total_orders"],
        "avg_order_value": df.iloc[0]["avg_order_value"],
        "total_customers": customers,
        "avg_delivery_days": delivery.iloc[0]["avg_days"],
        "on_time_pct":     delivery.iloc[0]["on_time_pct"],
        "avg_review_score": reviews,
    }

def monthly_revenue() -> pd.DataFrame:
    return query("""
        select
            order_month,
            round(sum(gross_revenue), 2) as revenue,
            count(distinct order_id)     as orders
        from main_marts.mart_revenue
        group by 1
        order by 1
    """)

def top_categories(n: int = 10) -> pd.DataFrame:
    return query(f"""
        select
            category_name,
            round(sum(gross_revenue), 2) as revenue,
            count(distinct order_id)     as orders
        from main_marts.mart_revenue
        group by 1
        order by 2 desc
        limit {n}
    """)

def delivery_by_state() -> pd.DataFrame:
    return query("""
        select
            customer_state,
            count(*)                                                          as total_orders,
            round(avg(total_delivery_days), 1)                               as avg_days,
            round(sum(case when delivery_status='on_time' then 1 end)*100.0/count(*), 1) as on_time_pct
        from main_marts.mart_delivery_analysis
        group by 1
        having count(*) > 100
        order by 3 desc
        limit 15
    """)

def delivery_status_summary() -> pd.DataFrame:
    return query("""
        select delivery_status, count(*) as orders
        from main_marts.mart_delivery_analysis
        group by 1
    """)

def customer_segments() -> pd.DataFrame:
    return query("""
        select customer_segment, count(*) as customers,
               round(avg(lifetime_value), 2) as avg_ltv
        from main_marts.mart_customer_ltv
        group by 1
        order by 2 desc
    """)

def ltv_distribution() -> pd.DataFrame:
    return query("""
        select ltv_quintile,
               count(*) as customers,
               round(avg(lifetime_value), 2) as avg_ltv,
               round(sum(lifetime_value), 2)  as total_ltv
        from main_marts.mart_customer_ltv
        group by 1
        order by 1
    """)

def seller_performance() -> pd.DataFrame:
    return query("""
        select seller_id, seller_state,
               total_orders, total_revenue,
               avg_review_score, revenue_quartile
        from main_marts.mart_seller_performance
        where total_orders >= 5
        order by total_revenue desc
        limit 500
    """)

def review_trends() -> pd.DataFrame:
    return query("""
        select review_month,
               round(avg(avg_score), 2)       as avg_score,
               sum(total_reviews)             as total_reviews,
               round(avg(positive_pct), 1)    as positive_pct
        from main_marts.mart_reviews
        where review_month is not null
        group by 1
        order by 1
    """)
