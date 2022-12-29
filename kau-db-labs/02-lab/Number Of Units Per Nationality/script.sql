-- medium

select h.nationality, count(distinct u.unit_id)
from airbnb_hosts as h
inner join airbnb_units u on h.host_id = u.host_id
where h.age < 30 and u.unit_type = 'Apartment'
group by h.nationality