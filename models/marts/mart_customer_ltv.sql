with orders as (
    select * from {{ ref('stg_orders') }}
    where order_status = 'delivered'
),

payments as (
    select
        order_id,
        sum(payment_value) as total_paid
    from {{ ref('stg_order_payments') }}
    group by 1
),

customers as (
    select * from {{ ref('stg_customers') }}
),

customer_orders as (
    select
        c.customer_unique_id,
        min(c.state)                                                    as state,
        min(c.city)                                                     as city,
        count(distinct o.order_id)                                      as total_orders,
        round(sum(p.total_paid), 2)                                     as lifetime_value,
        round(avg(p.total_paid), 2)                                     as avg_order_value,
        min(o.purchased_at)                                             as first_order_at,
        max(o.purchased_at)                                             as last_order_at,
        datediff('day', min(o.purchased_at), max(o.purchased_at))      as customer_lifespan_days
    from customers c
    join orders o   on c.customer_id = o.customer_id
    join payments p on o.order_id = p.order_id
    group by 1
)

select
    *,
    case
        when total_orders = 1 then 'one_time'
        when total_orders between 2 and 3 then 'returning'
        else 'loyal'
    end as customer_segment,
    ntile(5) over (order by lifetime_value) as ltv_quintile
from customer_orders
