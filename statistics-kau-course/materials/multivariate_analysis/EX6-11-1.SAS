/*EXAMPLE 6.11.1*/
options ls=72;
TITLE 'EXAMPLE 6.11.1';
DATA bioche;
  INFILE 'T6_2_ROOT.dat';
  INPUT group Y1 Y2 Y3 Y4;
 
proc glm data=bioche;
  class group;
  model Y1-Y4=group;
  manova h=group/printe printh;
  run;

proc iml;
use bioche;
read all var{Y1 Y2 Y3 Y4} into Y;
read all var{group} into group;
X=design(group);
E=y`*y-(y`*x*inv(x`*x)*x`*y);
L={1 -1 0 0 0 0,
   0 1 -1 0 0 0,
   0 0 1 -1 0 0,
   0 0 0 1 -1 0,
   0 0 0 0 1 -1};
H=t(L*inv(x`*x)*x`*y)*ginv(L*inv(x`*x)*L`)*L*inv(x`*x)*x`*y;

/*  Or use the estimates of E and H from GLM  */
*H={0.074 0.537 0.332 0.208,
   0.537 4.200 2.355 1.637,
   0.332 2.355 6.114 3.781,
   0.208 1.637 3.781 2.493};
 
HYY=H[1:2,1:2];
HYX=H[1:2,3:4];
HXY=H[3:4,1:2];
HXX=H[3:4,3:4];
*E={0.320  1.697 0.554 0.217,
   1.697 12.143 4.364 2.110,
   0.554  4.364 4.291 2.482,
   0.217  2.110 2.482 1.723};
EYY=E[1:2,1:2];
EYX=E[1:2,3:4];
EXY=E[3:4,1:2];
EXX=E[3:4,3:4];
LAMDA=(DET(E)/DET(E+H))/(DET(EYY)/DET(EYY+HYY));
print LAMDA;
RUN;QUIT;