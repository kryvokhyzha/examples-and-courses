options ls=74 nonumber nodate ps=10000;

/*  See commentary preceding EX15-3-4.sas 
    for explanation of biplotmacro.sas    */

data crime;
   infile 'T14_1_CITYCRIME.dat';
   input city$ murder rape robbery assault burglary larceny autothef;
run;

%biplot( data=crime, var=murder rape robbery assault burglary larceny autothef,
		 id=city, factype=GH, std=mean );run;quit;

goptions reset=all;

proc gplot data=biplot;
	plot dim2*dim1 / anno=bianno vaxis=axis2 haxis=axis1;
	axis1 label=(h=1.3 'Dimension 1');
	axis2 label=(h=1.3 a=90 r=0 'Dimension 2');
	symbol v=none;
run;quit;



%biplot( data=crime, var=murder rape robbery assault burglary larceny autothef,
		 id=city, factype=SYM, std=mean );run;quit;

goptions reset=all;

proc gplot data=biplot;
	plot dim2*dim1 / anno=bianno vaxis=axis2 haxis=axis1;
	axis1 label=(h=1.3 'Dimension 1');
	axis2 label=(h=1.3 a=90 r=0 'Dimension 2');
	symbol v=none;
run;quit;

