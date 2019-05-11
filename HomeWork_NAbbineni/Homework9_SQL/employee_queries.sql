
--1. List the following details of each employee: 
--employee number, last name, first name, gender, and salary
select e.emp_no, e.last_name, e.first_name, e.gender, s.salary 
from employees e
join salaries s on s.emp_no = e.emp_no 
order by 1;

--2. List employees who were hired in 1986.
select * from employees 
where date_part('year', hire_date) = 1986
order by 1;

--3. List the manager of each department with the following information: 
--department number, department name, the manager's employee number, last name, first name, 
--and start and end employment dates.
select d.dept_no, d.dept_name, e.emp_no, e.last_name, e.first_name, dm.from_date, dm.to_date
from dept_manager dm
join departments d on d.dept_no = dm.dept_no
join employees e on e.emp_no = dm.emp_no
order by d.dept_no, dm.from_date;

--4. List the department of each employee with the following information: 
--employee number, last name, first name, and department name.
select e.emp_no, e.last_name, e.first_name, d.dept_no, d.dept_name
from employees e
join dept_emp de on e.emp_no = de.emp_no
join departments d on d.dept_no = de.dept_no
order by e.emp_no, d.dept_no;

--select emp_no, count(*) from dept_emp group by emp_no having count(*)>1;

--5. List all employees whose first name is "Hercules" and last names begin with "B."
select * from employees e 
where first_name = 'Hercules' and last_name like 'B%'
order by 1;

--6. List all employees in the Sales department, including their 
--employee number, last name, first name, and department name.
select e.emp_no, e.last_name, e.first_name, d.dept_name
from employees e
join (select distinct emp_no, dept_no from dept_emp) de on e.emp_no = de.emp_no 
join departments d on d.dept_no = de.dept_no
where d.dept_name = 'Sales'
order by 1;

--7. List all employees in the Sales and Development departments, including their 
--employee number, last name, first name, and department name.
select e.emp_no, e.last_name, e.first_name, d.dept_name
from employees e
join (select distinct emp_no, dept_no from dept_emp) de on e.emp_no = de.emp_no 
join departments d on d.dept_no = de.dept_no
where d.dept_name in ('Sales', 'Development')
order by d.dept_name, e.emp_no;

--8. In descending order, list the frequency count of employee last names, i.e., 
--how many employees share each last name.
select e.last_name, count(e.emp_no)  as count_emp
from employees e
group by e.last_name
order by count_emp desc;


