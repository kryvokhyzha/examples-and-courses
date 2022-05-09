
TITLE 'EXAMPLE 6.10.1';
DATA dental;
  INFILE 'T6_16_DENTAL.dat';
  INPUT GENDER Y1 Y2 Y3 Y4;
 
proc iml;
use dental;
read all var {y1 y2 y3 y4} into y;
reset print;
y1=y[1:11, 1:4];
y2=y[12:27, 1:4];
n1=nrow(y1);
n2=nrow(y2);
y1bar=1/n1*y1`*J(n1,1);
y2bar=1/n2*y2`*J(n2,1);
s1=1/(n1-1)*y1`*(I(n1)-1/n1*J(n1))*y1;
s2=1/(n2-1)*y2`*(I(n2)-1/n2*J(n2))*y2;
spl=1/(n1+n2-2)*((n1-1)*s1+(n2-1)*s2);
c={-3 -1 1  3,
    1 -1 -1 1,
   -1  3 -3 1};
c1=c[1:1,1:4];
c2=c[2:2,1:4];
c3=c[3:3,1:4];
T2=n2*(c*y2bar)`*inv(c*s2*c`)*(c*y2bar);
ta=c1*y2bar/sqrt(c1*s2*c1`*(1/n2));
tb=c2*y2bar/sqrt(c2*s2*c2`*(1/n2));
tc=c3*y2bar/sqrt(c3*s2*c3`*(1/n2));
a={1 -3,
   1 -1,
   1  1,
   1  3};
beta=inv(a`*inv(s2)*a)*a`*inv(s2)*y2bar;
run;