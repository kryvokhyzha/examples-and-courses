data crime;
   infile 'T14_1_CITYCRIME.dat';
   input City$ Murder Rape Robbery Assult Burglary Larceny AutoTheft;
run;

data crimesmall;
   set crime;
   if _n_>6 then delete;
run;

proc cluster data=crimesmall outtree=treecrime method=complete nonorm;
   var Murder Rape Robbery Assult Burglary Larceny AutoTheft;
   id city;
run;

proc tree data=treecrime;
id city;
run;

proc iml;  /* DISTANCE MATRIX CODE */
   use crimesmall;
   read all var{Murder Rape Robbery Assult Burglary Larceny AutoTheft} into x;
   read all var{City} into city;
   nrow=nrow(x);
   xxp=x*x`;
   vdiag=vecdiag(xxp);
   xi=j(1,nrow)@vdiag;
   dist=sqrt(xi`-2*xxp+xi);
   distance=round(dist,0.1);
   print city distance;
quit;
