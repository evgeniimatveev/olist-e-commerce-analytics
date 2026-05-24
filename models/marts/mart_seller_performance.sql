with items as (
    select * from {{ ref('stg_order_items') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
    where order_status = 'delivered'
),

reviews as (
    select
        order_id,
        avg(review_score) as avg_score
    from {{ ref('stg_order_reviews') }}
    group by 1
),

sellers as (
    select * from {{ ref('stg_sellers') }}
),

aggregated as (
    select
        i.seller_id,
        s.city                              as seller_city,
        s.state                             as seller_state,
        count(distinct i.order_id)          as total_orders,
        count(i.order_item_id)              as total_items_sold,
        round(sum(i.price), 2)              as total_revenue,
        round(avg(i.price), 2)              as avg_item_price,
        round(avg(r.avg_score), 2)          as avg_review_score,
        count(distinct case when r.avg_score >= 4 then i.order_id end) as positive_reviews
    from items i
    join orders o   on i.order_id = o.order_id
    join sellers s  on i.seller_id = s.seller_id
    left join reviews r on i.order_id = r.order_id
    group by 1, 2, 3
)

select
    *,
    round(positive_reviews * 100.0 / nullif(total_orders, 0), 1) as positive_review_pct,
    ntile(4) over (order by total_revenue)                        as revenue_quartile
from aggregated
