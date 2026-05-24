with orders as (
    select * from {{ ref('stg_orders') }}
    where order_status = 'delivered'
),

items as (
    select * from {{ ref('stg_order_items') }}
),

payments as (
    select
        order_id,
        sum(payment_value) as total_paid
    from {{ ref('stg_order_payments') }}
    group by 1
),

products as (
    select * from {{ ref('stg_products') }}
),

joined as (
    select
        o.order_id,
        date_trunc('month', o.purchased_at)     as order_month,
        date_part('year', o.purchased_at)       as order_year,
        p.category_name,
        sum(i.price)                            as gross_revenue,
        sum(i.freight_value)                    as freight_revenue,
        sum(i.total_item_value)                 as total_item_value,
        max(pay.total_paid)                     as total_paid,
        count(distinct i.order_item_id)         as items_count
    from orders o
    join items i       on o.order_id = i.order_id
    join products p    on i.product_id = p.product_id
    left join payments pay on o.order_id = pay.order_id
    group by 1, 2, 3, 4
)

select * from joined
