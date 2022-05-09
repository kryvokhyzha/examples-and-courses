options ls=100 ps=1000 nodate nonumber;

/*  The following are two ways of doing the MDS
    example:  one using IML and the other using
    PROC MDS.                                */

/* Do MDS using IML */
proc iml;
D={
0		587		1212	701		1936	604		748		2139	2182	543,
587		0		920		940		1745	1188	713		1858	1737	597,
1212	920		0		879		831		1726	1631	949		1021	1494,
701		940		879		0		1374	968		1420	1645	1891	1220,
1936	1745	831		1374	0		2339	2451	347		959		2300,
604		1188	1726	968		2339	0		1092	2594	2734	923,
748		713		1631	1420	2451	1092	0		2571	2408	205,
2139	1858	949		1645	347		2594	2571	0		678		2442,
2182	1737	1021	1891	959		2734	2408	678		0		2329,
543		597		1494	1220	2300	923		205		2442	2329		0
};
A = -D#D/2;
n = nrow(A);
B = (I(n)-J(n)/n)*A*(I(n)-J(n)/n);
V = eigvec(B);
L = eigval(B);
do i = 1 to n;
  if L[i]<0 then L[i] = 0;
  end;
sqrtL = diag(sqrt(L));
Z=V*sqrtL;
create data1 from z;
append from z;
print D, A, B, L, V, Z;
quit;
data names;
input city $15.;
datalines;
Atlanta
Chicago
Denver
Houston
Los Angeles
Miami
New York
San Francisco
Seattle
Washington DC
;
data data1;
merge data1 names;run;
axis1 order=(-2000 to 2000 by 1000) label=(angle=90 rotate=0) minor=none;
axis2 order=(-2000 to 2000 by 1000) minor=none;
symbol pointlabel=("#city") value=dot;
proc gplot data=data1;
plot col2*col1/vaxis=axis1 haxis=axis2;
label col2='2nd Dimension' col1='1st Dimension';
run;quit;
symbol pointlabel=none;

/* Do MDS using PROC MDS */
data citydist;
   input  (atlanta chicago denver houston losangeles
              miami newyork sanfran seattle washdc) (5.)
              @56 city $15.;
   datalines;
    0                                                  Atlanta
  587    0                                             Chicago
 1212  920    0                                        Denver
  701  940  879    0                                   Houston
 1936 1745  831 1374    0                              Los Angeles
  604 1188 1726  968 2339    0                         Miami
  748  713 1631 1420 2451 1092    0                    New York
 2139 1858  949 1645  347 2594 2571    0               San Francisco
 2182 1737 1021 1891  959 2734 2408  678    0          Seattle
  543  597 1494 1220 2300  923  205 2442 2329    0     Washington D.C.
;run;

proc mds data=citydist level=absolute out=outex2
		 pconfig pfinal pfit pineigval pineigvec pinin pinit;
     id city;
     run;
symbol pointlabel=("#city") value=dot;
proc gplot data=outex2;
plot dim2*dim1/vaxis=axis1;run;quit;
symbol pointlabel=none;