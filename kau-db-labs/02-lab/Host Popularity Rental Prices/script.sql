--hard

select 
    host_pop_rating,
    min(price) as min_price,
    avg(price) as avg_price,
    max(price) as max_price
from (
    select 
        distinct price || room_type || host_since || zipcode || number_of_reviews as host_id,
        price, 
        case
            when number_of_reviews <= 0 then 'New'
            when number_of_reviews between 1 and 5 then 'Rising'
            when number_of_reviews between 6 and 15 then 'Trending Up'
            when number_of_reviews between 16 and 40 then 'Popular'
            when number_of_reviews > 40 then 'Hot'
        end as host_pop_rating
    from airbnb_host_searches
) t
group by host_pop_rating;