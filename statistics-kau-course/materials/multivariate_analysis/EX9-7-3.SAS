options ls=80;
/*EXAMPLE 9.7.3*/
data football;
infile 'T8_3_FOOTBALL.dat';
input group wdim circum fbeye eyehd earhd jaw;
proc discrim data=football outstat=ftstat 
           method=npar k=5 pool=yes crossvalidate;
class group;
var wdim circum fbeye eyehd earhd jaw;
title 'Discriminant Analysis of Football Data';
endsas; 