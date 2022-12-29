-- medium

select distinct t1.user_id
from amazon_transactions as t1
inner join amazon_transactions t2 on t1.user_id = t2.user_id
where abs(datediff('day', t1.created_at, t2.created_at)) <= 7
and t1.created_at <= t2.created_at and t1.id != t2.id;
