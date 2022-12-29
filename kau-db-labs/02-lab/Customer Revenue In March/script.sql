-- medium

select cust_id, sum(total_order_cost) as revenue 
from orders
where EXTRACT(MONTH FROM order_date) = 3
group by cust_id
order by revenue desc;