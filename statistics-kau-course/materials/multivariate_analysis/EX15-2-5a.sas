options ls=78 nodate nonumber ps=10000;

data people;
   infile 'T15_8_PERSON.dat';
   input person gender$ age$ mar_stat$ hairc$;
run;

proc corresp data=people out=plotdata(rename=(_name_=Category)) mca all;
   tables gender age mar_stat hairc;
run;quit;

/*   Plot the points using PROC GPLOT  */
goptions reset=all;
proc gplot data=plotdata;
plot dim1*dim2/vaxis=axis2 haxis=axis1;
axis1 label=(h=1.2 'Dimension 1'f=duplex);
axis2 label=(h=1.2 a=90 r=0 'Dimension 2' f=duplex);
symbol pointlabel=("#Category") v=dot;
run;quit;


/*   OR plot the points using the PLOTIT macro  */
%plotit(data=plotdata, datatype=corresp, plotvars=Dim1 Dim2);
