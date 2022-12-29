-- hard

with prepare_data as (
    select 
        distinct on (user_id::varchar || product_id::varchar)
        user_id, product_id, created_at
    from marketing_campaign
    order by (user_id::varchar || product_id::varchar), created_at
)
select count(distinct t1.user_id)
from prepare_data t1
    inner join prepare_data t2 on t1.user_id = t2.user_id
where 1=1
    and t1.created_at < t2.created_at
    and t1.product_id != t2.product_id
;