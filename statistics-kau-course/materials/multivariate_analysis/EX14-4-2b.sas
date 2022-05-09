options ls=100 ps=1000 nodate nonumber;

data protein;
   infile 'T14_7_PROTEIN.dat';
   input country $ R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
run;
proc standard data=protein out=protein mean=0 std=1;
   var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
run;

/*  Find the optimum values of k and r  */
proc modeclus data=protein method=1 k=2 r=1 to 3 by .1 out=Clus_out ;
   var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
   id country;
run;
proc modeclus data=protein method=1 k=3 r=1 to 3 by .1 out=Clus_out ;
   var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
   id country;
run;
proc modeclus data=protein method=1 k=4 r=1 to 3 by .1 out=Clus_out ;
   var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
   id country;
run;

/*  Use k=2 and r=1.8  */
proc modeclus data=protein method=1 k=2 r=1.8 out=Clus_out all;
   var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
   id country;
run;
proc sort data=Clus_out;
   by cluster;
run;
proc candisc data=Clus_out noprint out=ProCan(keep=country cluster Can1 Can2 Can3);
   class cluster;
   var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
run;
goptions reset=all;
goptions csymbol=black;
symbol1 v='1';symbol2 v='2';symbol3 v='3';
symbol4 v='4';symbol5 v='5';
proc gplot data=ProCan;
plot Can2*Can1=cluster /  vaxis=axis2 haxis=axis1 nolegend;
axis1 label=("z1" justify=center);
axis2 label=("z2" justify=center r=0 a=90);
run;quit;
