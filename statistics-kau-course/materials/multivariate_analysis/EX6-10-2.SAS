TITLE 'EXAMPLE 6.10.2';
DATA dental;
  INFILE 'T6_16_DENTAL.dat';
  INPUT group Y1 Y2 Y3 Y4;run;
proc glm;
class group;
model y1-y4=group;
manova h=_all_/printh printe;
run;quit;

proc iml;
use dental;
read all var {y1 y2 y3 y4} into y;
read all var {group} into group;
print y;
n=nrow(y);
numgrps=2;
ybar =1/n *y`*J(n,1);
x=design(group);
E=y`*y-(y`*x*inv(x`*x)*x`*y);
L={1 -1,1 -1};
H=t(L*inv(x`*x)*x`*y)*ginv(L*inv(x`*x)*L`)*L*inv(x`*x)*x`*y;
print E,H;
/* or use these estimates of E and H from GLM  */
*E={135.38636364      67.920454545      97.755681818      67.755681818,
   67.920454545      104.61931818      73.178977273      82.928977273,
   97.755681818      73.178977273      161.39346591      103.26846591,
   67.755681818      82.928977273      103.26846591      124.64346591};

*H={18.687710438      17.496212121      29.003577441      37.281355219,
   17.496212121      16.380681818      27.154356061      34.904356061,
   29.003577441      27.154356061      45.013941498      57.861163721,
   37.281355219      34.904356061      57.861163721      74.375052609};

S=E/25;
c={-3 -1 1 3,
    1 -1 -1 1,
   -1  3 -3 1};
c1={-3 -1 1 3};
T2=n*(c*ybar)`*inv(c*S*c`)*(c*ybar);
TL=n*(c1*ybar)`*inv(c1*S*c1`)*(c1*ybar);
lamda=det(c*E*c`)/det(c*(E+H)*c`);
lamdl=det(c1*E*c1`)/det(c1*(E+H)*c1`);
print T2, TL, lamda, lamdl;
run;quit;
