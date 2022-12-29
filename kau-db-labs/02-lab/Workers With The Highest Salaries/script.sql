-- medium

with max_salary_workers as (
    select worker_id from worker as w
    where w.salary in (select max(salary) from worker as w)
)
select t.worker_title
from title t
inner join max_salary_workers w on w.worker_id = t.worker_ref_id;

-- or

with max_salasy_workers as (
    select worker_id, salary, max(salary) over(partition by 1) as max_salary
    from worker as w
)
select t.worker_title
from title t
inner join max_salasy_workers w on w.salary = w.max_salary and w.worker_id = t.worker_ref_id
