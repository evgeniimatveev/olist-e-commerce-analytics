with source as (
    select * from {{ source('raw', 'raw_products') }}
),

translation as (
    select * from {{ source('raw', 'raw_category_translation') }}
),

renamed as (
    select
        p.product_id,
        coalesce(t.product_category_name_english, p.product_category_name, 'uncategorized') as category_name,
        p.product_category_name                                             as category_name_pt,
        p.product_name_lenght                                               as name_length,
        p.product_description_lenght                                        as description_length,
        p.product_photos_qty                                                as photos_qty,
        p.product_weight_g                                                  as weight_g,
        p.product_length_cm                                                 as length_cm,
        p.product_height_cm                                                 as height_cm,
        p.product_width_cm                                                  as width_cm
    from source p
    left join translation t on p.product_category_name = t.product_category_name
)

select * from renamed
