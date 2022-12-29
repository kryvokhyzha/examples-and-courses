-- medium

with prepare_log_data as (
   select 
      user_id, action, DATE(timestamp) as date,
      case 
         when action = 'page_load' then max(timestamp)
         when action = 'page_exit' then min(timestamp)
      end as timestamp
   from facebook_web_log
   where action in ('page_load', 'page_exit')
   group by user_id, action, date
),
calculate_session_time as (
   select 
      user_id, timestamp, action,
      lead(timestamp) over (partition by user_id order by timestamp ASC) - timestamp as diff_timestamp
   from prepare_log_data
)
select user_id, avg(diff_timestamp) as avg
from calculate_session_time
where action = 'page_load' and diff_timestamp is not null
group by user_id
;