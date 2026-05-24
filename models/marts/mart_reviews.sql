with reviews as (
    select * from {{ ref('stg_order_reviews') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

joined as (
    select
        r.review_id,
        r.order_id,
        r.review_score,
        r.created_at,
        date_trunc('month', r.created_at)           as review_month,
        datediff('day', o.delivered_customer_at, r.created_at) as days_after_delivery,
        p.category_name
    from reviews r
    left join orders o  on r.order_id = o.order_id
    left join items i   on r.order_id = i.order_id
    left join products p on i.product_id = p.product_id
),

aggregated as (
    select
        review_month,
        category_name,
        count(*)                                            as total_reviews,
        round(avg(review_score), 2)                         as avg_score,
        count(case when review_score = 5 then 1 end)        as score_5,
        count(case when review_score = 4 then 1 end)        as score_4,
        count(case when review_score = 3 then 1 end)        as score_3,
        count(case when review_score <= 2 then 1 end)       as score_1_2,
        round(count(case when review_score >= 4 then 1 end) * 100.0 / count(*), 1) as positive_pct
    from joined
    group by 1, 2
)

select * from aggregated
