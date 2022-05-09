options ls=90 ps=1000 nodate nonumber;

data Speed;
infile 'T14_3_TRACK.dat';
input Country $	e1 e2 e3 e4 e5 e6 e7 e8;
;run;

proc iml;  /* DISTANCE MATRIX CODE */
   use Speed;
   read all var{e1 e2 e3 e4 e5 e6 e7 e8} into x;
   read all var{Country} into country;
   nrow=nrow(x);
   xxp=x*x`;
   vdiag=vecdiag(xxp);
   xi=j(1,nrow)@vdiag;
   dist=sqrt(xi`-2*xxp+xi);
   ave=dist*j(nrow(dist),1)/(nrow(dist)-1);
   distance=round(dist,0.1);
   print "The Distance Matrix";
   print country dist;
   print "Average distance from one element to the other.";
   print country ave;
   print "USA has the biggest difference, so make it the first element in the splinter group.";

   /*Make USA the splinter group */
   cntryMG=country[2:8];
   maingrp=dist[2:8,2:8];
   aveMG=maingrp*j(nrow(maingrp),1)/(nrow(maingrp)-1);
   avespltgrp=dist[2:8,1];
   diff=avespltgrp-aveMG;
   print cntryMG aveMG avespltgrp diff;
   print "Austrialia has a negative difference, so move it to the splinter group.";

   /*Move Aust to splinter group */
   cntryMG=country[3:8];
   maingrp=dist[3:8,3:8];
   aveMG=maingrp*j(nrow(maingrp),1)/(nrow(maingrp)-1);
   avespltgrp=(1/2)*(dist[3:8,1]+dist[3:8,2]);
   diff=avespltgrp-aveMG;
   print cntryMG aveMG avespltgrp diff;
   print "No other difference is negative, so stop the process.";
   print "Hence the final groups are CL1=(USA, Aust) and CL2=(GB, GDR, USSR, Can, Kenya, Belgium)"; 
quit;
