-- medium

select distinct business_name, 
case
    when lower(business_name) like '%restaurant%' then 'restaurant'
    when lower(business_name) like '%cafe%' or
         lower(business_name) like '%café%' or
         lower(business_name) like '%coffee%' then 'cafe'
    when lower(business_name) like '%school%' then 'school'
    else 'other'
end as business_type
from sf_restaurant_health_violations;