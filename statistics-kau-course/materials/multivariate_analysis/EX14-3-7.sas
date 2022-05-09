data crime;
   infile 'T14_1_CITYCRIME.dat';
   input City$ Murder Rape Robbery Assult Burglary Larceny AutoTheft;
run;

proc cluster data=crime outtree=treecrime method=ward nonorm;
   var Murder Rape Robbery Assult Burglary Larceny AutoTheft;
   id city;
run;
goptions reset=all;
axis1 label=("Increase in SSE" justify=center);
proc tree data=treecrime vaxis=axis1;
id city;
run;

