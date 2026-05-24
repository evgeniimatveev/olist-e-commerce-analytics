with source as (
    select * from {{ source('raw', 'raw_sellers') }}
),

renamed as (
    select
        seller_id,
        seller_zip_code_prefix as zip_code,
        lower(seller_city)     as city,
        upper(seller_state)    as state
    from source
)

select * from renamed
