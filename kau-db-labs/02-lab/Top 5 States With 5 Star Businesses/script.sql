-- hard

with results as (
    select
        state, n_businesses,
        rank() over(order by n_businesses DESC) as ranking
    from (
        select bus.state, count(bus.state) as n_businesses
        from yelp_business as bus
        where bus.stars = 5
        group by bus.state
    ) t
)
select state, n_businesses
from results
where ranking <= 5
order by n_businesses DESC, state;