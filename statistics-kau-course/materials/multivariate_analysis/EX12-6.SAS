options ls=80;
/*EXAMPLE 12.6*/

data football;
infile 'T8_3_FOOTBALL.dat';
input group wdim circum fbeye eyehd earhd jaw;
   if group=3 then group=2;
   if group=1 then delete;
proc princomp cov; 
  var wdim circum fbeye eyehd earhd jaw;

run;
proc factor data=football scree;
  var wdim circum fbeye eyehd earhd jaw;
run;  
endsas; 





















