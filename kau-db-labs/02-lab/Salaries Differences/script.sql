-- easy

select abs(max(empl1.salary) - max(empl2.salary)) from db_dept
left join db_employee as empl1 on db_dept.id = empl1.department_id and db_dept.id = 1
left join db_employee as empl2 on db_dept.id = empl2.department_id and db_dept.id = 4;