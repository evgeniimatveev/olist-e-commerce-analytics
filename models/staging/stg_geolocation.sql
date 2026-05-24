with source as (
    select * from {{ source('raw', 'raw_geolocation') }}
),

-- keep one lat/lng per zip code (avg to remove duplicates)
deduped as (
    select
        geolocation_zip_code_prefix as zip_code,
        round(avg(geolocation_lat), 6) as lat,
        round(avg(geolocation_lng), 6) as lng,
        lower(min(geolocation_city))   as city,
        upper(min(geolocation_state))  as state
    from source
    group by 1
)

select * from deduped
