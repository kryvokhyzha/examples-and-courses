-- medium

select 
    DENSE_RANK() over(order by sum_n_messages desc) ranking,
    id_guest, sum_n_messages
from (
    select id_guest, sum(n_messages) sum_n_messages
    from airbnb_contacts
    group by id_guest
) t;