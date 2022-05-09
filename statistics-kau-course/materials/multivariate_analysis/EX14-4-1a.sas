options ls=100 ps=1000 nodate nonumber;

data protein;
infile 'T14_7_PROTEIN.dat';
input country $ R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
run;
proc standard data=protein out=protein mean=0 std=1;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
run;
goptions reset=all;
goptions csymbol=black;
symbol1 v='1';symbol2 v='2';symbol3 v='3';
symbol4 v='4';symbol5 v='5';

/*  Use principal components to guess the number
    of initial clusters to use   */
proc princomp data=protein out=ProPC noprint;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
run;
goptions reset=all;
symbol pointlabel=("#country") font=, value=dot;
proc gplot data=ProPC;
plot prin2*prin1/ vaxis=axis2 haxis=axis1 nolegend;
axis1 label=("z1" justify=center);
axis2 label=("z2" justify=center r=0 a=90);
run;quit;
symbol pointlabel=none;

/*  Method #1 for getting seeds:  Random 5 observations   */
proc fastclus data=protein maxc=5 replace=random maxiter=10 out=Clus_out radius=1;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
id country;
run;
proc sort data=Clus_out;
by cluster distance;
run;
proc candisc data=Clus_out noprint out=ProCan(keep=country cluster Can1 Can2);
class cluster;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
run;
proc gplot data=ProCan;
plot Can2*Can1=cluster /  vaxis=axis2 haxis=axis1 nolegend;
axis1 label=("z1" justify=center);
axis2 label=("z2" justify=center r=0 a=90);
run;quit;
proc print data=Clus_out;
var country cluster distance;
run;

/*  Method #2 for getting seeds:  First 5 observations   */
proc fastclus data=protein radius=0 maxc=5 replace=none maxiter=10 out=Clus_out ;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
id country;
run;
proc sort data=Clus_out;
by cluster distance;
run;
proc candisc data=Clus_out noprint out=ProCan(keep=country cluster Can1 Can2);
class cluster;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
run;
proc gplot data=ProCan;
plot Can2*Can1=cluster /  vaxis=axis2 haxis=axis1 nolegend;
axis1 label=("z1" justify=center);
axis2 label=("z2" justify=center r=0 a=90);
run;quit;
proc print data=Clus_out;
var country cluster distance;
run;

/*  Method #3 for getting seeds:  Select 5 obs that are mutually farthest apart */
proc fastclus data=protein radius=5 maxc=5 replace=full maxiter=10 out=Clus_out;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
id country;
run;
proc fastclus data=protein radius=4 maxc=5 replace=full maxiter=10 out=Clus_out;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
id country;
run;
proc fastclus data=protein radius=4.1142 maxc=5 replace=full maxiter=10 out=Clus_out;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
id country;
run;
proc sort data=Clus_out;
by cluster distance;
run;
proc candisc data=Clus_out noprint out=ProCan(keep=country cluster Can1 Can2);
class cluster;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
run;
proc gplot data=ProCan;
plot Can2*Can1=cluster /  vaxis=axis2 haxis=axis1 nolegend;
axis1 label=("z1" justify=center);
axis2 label=("z2" justify=center r=0 a=90);
run;quit;
proc print data=Clus_out;
var country cluster distance;
run;

/*  Method #4 for getting seeds:Use Average Linkage to get cluster centriods   */
proc cluster data=protein method=average outtree=ProTree noprint;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
id country;
run;
proc tree data=ProTree nclusters=5 out=newdata noprint;
id country;
copy R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
run;
proc sort data=newdata;
by cluster;
run;
proc means data=newdata noprint;
by cluster;
output out=Seeds mean=R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
run;
proc fastclus data=protein maxc=5 maxiter=50 seed=Seeds out=Clus_out noprint;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
id country;
run;
proc sort data=Clus_out;
by cluster distance;
run;
proc candisc data=Clus_out noprint out=ProCan(keep=country cluster Can1 Can2);
class cluster;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
run;
proc gplot data=ProCan;
plot Can2*Can1=cluster /  vaxis=axis2 haxis=axis1 nolegend;
axis1 label=("z1" justify=center);
axis2 label=("z2" justify=center r=0 a=90);
run;quit;
proc print data=Clus_out;
var country cluster distance;
run;

/*  Method #5 for getting seeds:  SAS default   */
proc fastclus data=protein maxc=5 maxiter=10 out=Clus_out;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
id country;
run;
proc sort data=Clus_out;
by cluster distance;
run;
proc candisc data=Clus_out noprint out=ProCan(keep=country cluster Can1 Can2);
class cluster;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
run;
proc gplot data=ProCan;
plot Can2*Can1=cluster /  vaxis=axis2 haxis=axis1 nolegend;
axis1 label=("z1" justify=center);
axis2 label=("z2" justify=center r=0 a=90);
run;quit;
proc print data=Clus_out;
var country cluster distance;
run;





proc cluster data=protein method=ward outtree=ProTree noprint;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
id country;
run;
proc tree data=ProTree;run;
proc cluster data=protein method=centroid outtree=ProTree noprint;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
id country;
run;
proc tree data=ProTree;run;
proc cluster data=protein method=median outtree=ProTree noprint;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
id country;
run;
proc tree data=ProTree;run;
proc cluster data=protein method=flexible outtree=ProTree noprint;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
id country;
run;
proc tree data=ProTree;run;

proc princomp data=protein out=ProPC noprint;
var R_meat W_meat Eggs Milk Fish Cereals Starchy Nuts Frut_Veg;
run;
goptions reset=all;
symbol pointlabel=("#country") font=, value=dot;
proc gplot data=ProPC;
plot prin2*prin1/ vaxis=axis2 haxis=axis1 nolegend;
axis1 label=("z1" justify=center);
axis2 label=("z2" justify=center r=0 a=90);
run;quit;
symbol pointlabel=none;
