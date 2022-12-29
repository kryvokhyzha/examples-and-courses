-- hard

with all_pairs as (
    select user1, count(distinct user2) as user2_cnt
    from (
        select user1, user2 from facebook_friends
        union
        select user2, user1 from facebook_friends
    ) t
    group by user1
)
select user1, 100.0 * user2_cnt / count(user1) over(partition by 1)
from all_pairs;