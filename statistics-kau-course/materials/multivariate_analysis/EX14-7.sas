options ls=90 nonumber nodate ps=10000;

data crime;
   infile 'T14_1_CITYCRIME.dat';
   input city$ murder rape robbery assault burglary larceny autothef;
run;

/*   Cluster Analysis on the variables */
proc iml;
   use crime;
   read all var{murder rape robbery assault burglary larceny autothef} into Y;
   variables = {murder, rape, robbery, assault, burglary, larceny, autothef};
   n = nrow(Y);
   S = Y`*(I(n)-J(n)/n)*Y/(n-1);
   Ds = sqrt(diag(S));
   R = inv(Ds)*S*inv(Ds);
   disim = 1-R#R;
   create DisimVar from disim[rowname=variables];
   append from disim[rowname=variables];
quit;
data DisimVar(type=distance);
set DisimVar;
proc cluster data=DisimVar outtree=treecrime method=average nonorm noprint;
   id variables;
run;
proc tree data=treecrime;
   id variables;
run;quit;
goptions reset=all;
axis1 label=("Increase in SSE" justify=center);
proc cluster data=DisimVar outtree=treecrime method=Ward nonorm noprint;
   id variables;
run;
proc tree data=treecrime vaxis=axis1;
   id variables;
run;quit;


/*   Factor Analysis   */
ods output OrthRotFactPat=varmax;
proc factor data=crime method=prin priors=smc rotate=varimax;
   var murder rape robbery assault burglary larceny autothef;
run;
ods output FactorPattern=FactPat FactorStructure=orthob;
proc factor data=crime method=prin priors=smc rotate=hk;
   var murder rape robbery assault burglary larceny autothef;
run;
