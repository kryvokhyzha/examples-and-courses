options ls=80;

data congress;
   infile 'T15_2_CONGRESS.dat';
   input voter $ y1-y15;
run;

/*   Generate random configuration of 
     points from a multivariate 
	 normal distribution as input
	 into the nonmetric multidimensional
	 scaling procedure       */
proc iml;
	start rnorm(mu, sigma, seed);
	z = normal(repeat(seed, 2));
	g = root(sigma);
	x = mu + t(g)*z;
	return(x);
	finish;
	m = {0,0};
	sig = {1 0,
	   	   0 1};
	sed = -1;
	do i = 1 to 15;
   		x = rnorm(m,sig,sed);
   		matx=matx//x`;
	end;
	create seeds from matx;
	append from matx;
quit;

data seeds;
	set seeds(rename=(col1=dim1 col2=dim2));

proc mds data=congress level=ordinal outfit=stress noprint dim=1 to 6 by=1;
	id voter;
run;
data stress;
	set stress;
	STRESS=criter;
	drop criter;

/*   Generate STRESS plot verses 
     number of dimensions    */
symbol i=join value=dot;
axis1 label=(angle=90 rotate=0) minor=none;
axis2 minor=none;
proc gplot data=stress;
	plot stress*_dimens_ /vaxis=axis1 haxis=axis2;
run;quit;
symbol i=none;

/*  Find MDS coordinates of congressman
    in 2 dimensions and plot them using
	PROC GPLOT        */
proc mds data=congress level=ordinal out=outplot dim=2 initial=seeds pinit;
     id voter;
	 invar dim1 dim2;
run;

symbol pointlabel=("#voter") value=dot;
axis1 label=(angle=90 rotate=0) minor=none;
axis2 minor=none;
proc gplot data=outplot;
	plot dim2*dim1/vaxis=axis1;
run;quit;
symbol pointlabel=none;

/*  Find initial configuration of points
    using a uniform distribution as input
	into PROC MDS      */
proc iml;
	matx = uniform(repeat(-1, 15,2));
	create seeds from matx;
	append from matx;
quit;

data seeds;
set seeds(rename=(col1=dim1 col2=dim2));run;

proc mds data=congress level=ordinal out=outex1 dim=2 initial=seeds
		 pinit;
     id voter;
	 invar dim1 dim2;
     run;
symbol pointlabel=("#voter") value=dot;
axis1 label=(angle=90 rotate=0) minor=none;
axis2 minor=none;

proc gplot data=outex1;
plot dim2*dim1/vaxis=axis1;run;quit;
symbol pointlabel=none;

/*  Find initial configuration of points
    using the results of metric MDS  
    as input into PROC MDS     */
proc mds data=congress level=absolute out=seeds dim=2 noprint;
     id voter;
     run;

proc mds data=congress level=ordinal out=outex1 dim=2 initial=seeds
		 pinit;
     id voter;
	 invar dim1 dim2;
     run;
goptions reset=all;
symbol pointlabel=("#voter") value=dot;
axis1 label=(angle=90 rotate=0) minor=none;
axis2 minor=none;

proc gplot data=outex1;
plot dim2*dim1/vaxis=axis1;run;quit;
symbol pointlabel=none;
