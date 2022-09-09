create table week1 (name varchar primary key, test int default 0, assignment int default 0, behaviour int default 0, communication int default 0, participation int default 0);  

-------------------------------------------------------------------------------------------------

create view assignments as
select coalesce ( w1.name,w2.name,w3.name,w4.name,w5.name,w6.name,w7.name,w8.name ) as name, coalesce( w1.assignment,0 ) as assignment1, coalesce( w2.assignment,0 ) as assignment2, coalesce( w3.assignment,0 ) as assignment3, coalesce( w4.assignment,0 ) as assignment4, coalesce( w5.assignment,0 )as assignment5, coalesce( w6.assignment,0 ) as assignment6, coalesce( w7.assignment,0 ) as assignment7, coalesce( w8.assignment,0 ) as assignment8     
from week1 w1 
full outer join week2 w2 on w2.name = w1.name 
full outer join week3 w3 on w3.name = w1.name
full outer join week4 w4 on w4.name = w1.name 
full outer join week5 w5 on w5.name = w1.name 
full outer join week6 w6 on w6.name = w1.name 
full outer join week7 w7 on w7.name = w1.name
full outer join week8 w8 on w8.name = w1.name

create view communications as
select coalesce ( w1.name,w2.name,w3.name,w4.name,w5.name,w6.name,w7.name,w8.name ) as name, coalesce( w1.communication,0 ) as communication1, coalesce( w2.communication,0 ) as communication2, coalesce( w3.communication,0 ) as communication3, coalesce( w4.communication,0 ) as communication4, coalesce( w5.communication,0 )as communication5, coalesce( w6.communication,0 ) as communication6, coalesce( w7.communication,0 ) as communication7, coalesce( w8.communication,0 ) as communication8     
from week1 w1 
full outer join week2 w2 on w2.name = w1.name 
full outer join week3 w3 on w3.name = w1.name
full outer join week4 w4 on w4.name = w1.name 
full outer join week5 w5 on w5.name = w1.name 
full outer join week6 w6 on w6.name = w1.name 
full outer join week7 w7 on w7.name = w1.name
full outer join week8 w8 on w8.name = w1.name

create view participations as
select coalesce ( w1.name,w2.name,w3.name,w4.name,w5.name,w6.name,w7.name,w8.name ) as name, coalesce( w1.participation,0 ) as participation1, coalesce( w2.participation,0 ) as participation2, coalesce( w3.participation,0 ) as participation3, coalesce( w4.participation,0 ) as participation4, coalesce( w5.participation,0 )as participation5, coalesce( w6.participation,0 ) as participation6, coalesce( w7.participation,0 ) as participation7, coalesce( w8.participation,0 ) as participation8     
from week1 w1 
full outer join week2 w2 on w2.name = w1.name 
full outer join week3 w3 on w3.name = w1.name
full outer join week4 w4 on w4.name = w1.name 
full outer join week5 w5 on w5.name = w1.name 
full outer join week6 w6 on w6.name = w1.name 
full outer join week7 w7 on w7.name = w1.name
full outer join week8 w8 on w8.name = w1.name

create view tests as
select coalesce ( w1.name,w2.name,w3.name,w4.name,w5.name,w6.name,w7.name,w8.name ) as name, coalesce( w1.test,0 ) as test1, coalesce( w2.test,0 ) as test2, coalesce( w3.test,0 ) as test3, coalesce( w4.test,0 ) as test4, coalesce( w5.test,0 )as test5, coalesce( w6.test,0 ) as test6, coalesce( w7.test,0 ) as test7, coalesce( w8.test,0 ) as test8     
from week1 w1 
full outer join week2 w2 on w2.name = w1.name 
full outer join week3 w3 on w3.name = w1.name
full outer join week4 w4 on w4.name = w1.name 
full outer join week5 w5 on w5.name = w1.name 
full outer join week6 w6 on w6.name = w1.name 
full outer join week7 w7 on w7.name = w1.name
full outer join week8 w8 on w8.name = w1.name

create view behaviours as
select coalesce ( w1.name,w2.name,w3.name,w4.name,w5.name,w6.name,w7.name,w8.name ) as name, coalesce( w1.behaviour,0 ) as behaviour1, coalesce( w2.behaviour,0 ) as behaviour2, coalesce( w3.behaviour,0 ) as behaviour3, coalesce( w4.behaviour,0 ) as behaviour4, coalesce( w5.behaviour,0 )as behaviour5, coalesce( w6.behaviour,0 ) as behaviour6, coalesce( w7.behaviour,0 ) as behaviour7, coalesce( w8.behaviour,0 ) as behaviour8     
from week1 w1 
full outer join week2 w2 on w2.name = w1.name 
full outer join week3 w3 on w3.name = w1.name
full outer join week4 w4 on w4.name = w1.name 
full outer join week5 w5 on w5.name = w1.name 
full outer join week6 w6 on w6.name = w1.name 
full outer join week7 w7 on w7.name = w1.name
full outer join week8 w8 on w8.name = w1.name

-----------------------------------------------------------------------------------------------

create view parameters as

with cte1 as (
select coalesce ( t.name,a.name,b.name,c.name,p.name ) as name,
test1+test2+test3+test4+test5+test6+test7+test8 as test_total,
assignment1+assignment2+assignment3+assignment4+assignment5+assignment6+assignment7+assignment8 as assignment_total,
behaviour1+behaviour2+behaviour3+behaviour4+behaviour5+behaviour6+behaviour7+behaviour8 as behaviour_total,
communication1+communication2+communication3+communication4+communication5+communication6+communication7+communication8 as communication_total,
participation1+participation2+participation3+participation4+participation5+participation6+participation7+participation8 as participation_total
from tests t
full outer join assignments a on a.name = t.name 
full outer join behaviours b on b.name = t.name
full outer join communications c on c.name = t.name 
full outer join participations p on p.name = t.name 
),

cte2 as (
select * ,
test_total+assignment_total+behaviour_total+communication_total+participation_total as parameters_total
from cte1
)

select * from cte2


----------------------------------------------------------------------------------------------

