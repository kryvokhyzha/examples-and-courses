-- hard

select * 
from (
    select 
        mdf.date,
        sum(case when mad.paying_customer = 'no' then mdf.downloads else 0 end) non_paying,
        sum(case when mad.paying_customer = 'yes' then mdf.downloads else 0 end) paying
    from ms_user_dimension mud
        inner join ms_acc_dimension mad on mud.acc_id = mad.acc_id
        inner join ms_download_facts mdf on mdf.user_id = mud.user_id
    group by mdf.date
) t
where non_paying > paying
order by date;