with source as (
    select * from {{ source('raw', 'raw_order_items') }}
),

renamed as (
    select
        order_id,
        order_item_id,
        product_id,
        seller_id,
        cast(shipping_limit_date as timestamp) as shipping_limit_at,
        cast(price as decimal(10,2))           as price,
        cast(freight_value as decimal(10,2))   as freight_value,
        cast(price + freight_value as decimal(10,2)) as total_item_value
    from source
)

select * from renamed
