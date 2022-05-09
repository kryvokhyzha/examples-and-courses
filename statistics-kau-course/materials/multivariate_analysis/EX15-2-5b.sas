options ls=78 nodate nonumber ps=10000;

data danish;
   infile 'T15_13_DOITYOURSELF.dat';
   input Work$ Tenure$ Accomodation$ Age$ Resp$ Count;
run;

proc corresp data=danish out=plotdata(rename=(_name_=Category)) mca all;
   tables Work Tenure Accomodation Age Resp;
   weight count;
run;quit;

goptions reset=all;
proc gplot data=plotdata;
   plot dim1*dim2/vaxis=axis2 haxis=axis1;
   axis1 label=(h=1.2 'Dimension 1'f=duplex);
   axis2 label=(h=1.2 a=90 r=0 'Dimension 2' f=duplex);
   symbol pointlabel=("#Category") v=dot;
run;quit;

