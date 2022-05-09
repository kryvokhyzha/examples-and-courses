options ls=78 nodate nonumber ps=1000;

data piston;
   input compres North Center South;
   datalines;
1	17	17	12
2	11	9	13
3	11	8	19
4	14	7	28
;run;

proc corresp data=piston out=data1(rename=(_name_=Category)) all;
   var North Center South;
   id compres;
run;

/*  Plot the points using PROC GPLOT */
goptions reset=all;
proc gplot data=data1;
plot dim2*dim1/vaxis=axis2 haxis=axis1;
axis1 order=(-0.4 to 0.4 by .1) label=(h=1.2 'Dimension 1'f=duplex);
axis2 order=(-0.2 to 0.2 by .1) label=(h=1.2 a=90 r=0 'Dimension 2' f=duplex);
symbol pointlabel=("#compres") v=dot;
run;quit;


/*  Or plot the points using the PLOTIT macro */
%plotit(data=data1, datatype=corresp, plotvars=Dim1 Dim2);
