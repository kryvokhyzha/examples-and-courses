-- medium

with proc as (
    select type, count(*) as counts_p 
    from facebook_complaints
    where processed
    group by type
), all_ as (
    select type, count(*) as counts_all 
    from facebook_complaints
    group by type
)
select p.type, counts_p :: NUMERIC / counts_all as processed_rate
from proc p
inner join all_ a on p.type = a.type;