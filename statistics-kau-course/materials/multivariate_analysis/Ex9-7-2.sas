
/*EXAMPLE 9.7.2*/
data football;
infile 'T8_3_FOOTBALL.dat';
input group wdim circum fbeye eyehd earhd jaw;
proc discrim data=football outstat=ftstat
           method=npar kernel=normal r=2  pool=yes  list crosslist;
class group;
var wdim circum fbeye eyehd earhd jaw;
title 'Discriminant Analysis of Football Data';
run;
