options ls=80;
/*EXAMPLE 12.2(a)*/
data sons;
infile 'T3_7_SONS.dat';
input x1 x2 y1 y2;

proc princomp cov;
  var x1 x2;
run;
proc plot;
  plot x2 * x1/ vpos=60;
run;