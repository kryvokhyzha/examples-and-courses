-- hard

with prep_month_data as (
    select 
        year_month, revenue,
        lag(revenue) over(order by year_month ASC) as last_month_revenue
    from (
        select 
            to_char(created_at, 'YYYY-MM') year_month,
            sum(value) as revenue
        from sf_transactions
        group by year_month
    ) t
)
select 
    year_month, round(100 * (revenue - last_month_revenue) / last_month_revenue, 2) as revenue_diff_pct
from prep_month_data;