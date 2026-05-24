with orders as (
    select * from {{ ref('stg_orders') }}
    where order_status = 'delivered'
      and delivered_customer_at is not null
      and estimated_delivery_at is not null
),

customers as (
    select * from {{ ref('stg_customers') }}
),

delivery as (
    select
        o.order_id,
        o.purchased_at,
        date_trunc('month', o.purchased_at)                             as order_month,
        c.state                                                         as customer_state,
        c.city                                                          as customer_city,
        datediff('day', o.purchased_at, o.approved_at)                 as days_to_approve,
        datediff('day', o.approved_at, o.delivered_carrier_at)         as days_to_carrier,
        datediff('day', o.delivered_carrier_at, o.delivered_customer_at) as days_to_deliver,
        datediff('day', o.purchased_at, o.delivered_customer_at)       as total_delivery_days,
        datediff('day', o.purchased_at, o.estimated_delivery_at)       as estimated_days,
        datediff('day', o.estimated_delivery_at, o.delivered_customer_at) as delivery_delay_days,
        case
            when o.delivered_customer_at <= o.estimated_delivery_at then 'on_time'
            else 'late'
        end as delivery_status
    from orders o
    join customers c on o.customer_id = c.customer_id
)

select * from delivery
