data crime;
   infile 'T14_1_CITYCRIME.dat';
   input City$ Murder Rape Robbery Assult Burglary Larceny AutoTheft;
run;

proc cluster data=crime outtree=treecrime method=flexible beta=-0.25 nonorm;
   var Murder Rape Robbery Assult Burglary Larceny AutoTheft;
   id city;
run;

proc tree data=treecrime;
id city;
run;

proc cluster data=crime outtree=treecrime method=flexible beta=-0.75 nonorm;
   var Murder Rape Robbery Assult Burglary Larceny AutoTheft;
   id city;
run;

proc tree data=treecrime;
id city;
run;


