options ls=100 ps=1000 nodate nonumber;

/*  The following are two ways of doing the MDS
    example:  one using IML and the other using
    PROC MDS.                                */

/* Do MDS using IML */
proc iml;
D = {0         2.8284271 2.8284271 2.8284271 2.8284271,
     2.8284271         0         4 5.6568542         4,
     2.8284271         4         0         4 5.6568542,
     2.8284271 5.6568542         4         0         4,
     2.8284271         4 5.6568542         4         0};
A = -D#D/2;
n = nrow(A);
B = round((I(n)-J(n)/n)*A*(I(n)-J(n)/n));
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
axis1 label=(angle=90 rotate=0) minor=none;
axis2 minor=none;
symbol value=dot pointlabel=none;
proc gplot data=data1;
plot col2*col1/vaxis=axis1 haxis=axis2;
label col2='Dimension 2' col1='Dimension 1';
run;quit;


/* Do MDS using PROC MDS */
data ex1;
input x1 x2 x3 x4 x5;
datalines;
0         2.8284271 2.8284271 2.8284271 2.8284271
2.8284271         0         4 5.6568542         4
2.8284271         4         0         4 5.6568542
2.8284271 5.6568542         4         0         4
2.8284271         4 5.6568542         4         0
;

proc mds data=ex1 dim=2 level=absolute out=outex1
         pconfig pfinal pfit pineigval pineigvec pinin pinit;run;
proc gplot data=outex1;
plot dim2*dim1;run;quit;
