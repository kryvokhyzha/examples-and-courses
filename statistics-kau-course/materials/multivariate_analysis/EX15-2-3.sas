options ls=78 nodate nonumber ps=1000;

data piston2;
infile 'T15_5_PISTON.dat';
input leg$ compres$ count;
;run;

proc freq data=piston2;
   weight count;
   tables leg*compres/chisq;
run;

