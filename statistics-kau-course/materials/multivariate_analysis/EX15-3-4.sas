options ls=74 nonumber nodate ps=10000;

data crime;
   infile 'T14_1_CITYCRIME.dat';
   input city$ murder rape robbery assault burglary larceny autothef;
run;

/*  In order to use the biplot macro, simply
	run the entire biplotmacro.sas code in
    SAS, which will load the macro for 
	later use during that SAS session.    */

/*  See biplotmacro.sas for commentary on 
	the details of the parameter options
	for this macro.						  */

%biplot( data=crime, var=murder rape robbery assault burglary larceny autothef,
		 id=city, factype=JK, std=mean );run;quit;

goptions reset=all;
proc gplot data=biplot;
	plot dim2*dim1 / anno=bianno vaxis=axis2 haxis=axis1;
	axis1 label=(h=1.3 'Dimension 1');
	axis2 label=(h=1.3 a=90 r=0 'Dimension 2');
	symbol v=none;
run;quit;


