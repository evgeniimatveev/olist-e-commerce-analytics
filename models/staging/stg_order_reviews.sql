with source as (
    select * from {{ source('raw', 'raw_order_reviews') }}
),

renamed as (
    select
        review_id,
        order_id,
        cast(review_score as integer)                  as review_score,
        review_comment_title                           as comment_title,
        review_comment_message                         as comment_message,
        cast(review_creation_date as timestamp)        as created_at,
        cast(review_answer_timestamp as timestamp)     as answered_at
    from source
)

select * from renamed
