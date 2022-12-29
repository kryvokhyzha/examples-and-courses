-- medium

with sent_t as (
    select user_id_sender, date, action from fb_friend_requests where action = 'sent'
), accepted_t as (
    select user_id_receiver, date, action from fb_friend_requests where action = 'accepted'
)
select date, 1 - (1 + accepted_cnt + 0.0) / (accepted_cnt + sent_cnt + 0.0) as percentage_acceptance
from (
    select
        s.date,
        count(case when s.action = 'sent' then 1 end) sent_cnt,
        count(case when a.action = 'accepted' then 1 end) accepted_cnt
    from sent_t as s
    left join accepted_t as a on s.user_id_sender = a.user_id_receiver and a.date = s.date
    group by s.date
) t
