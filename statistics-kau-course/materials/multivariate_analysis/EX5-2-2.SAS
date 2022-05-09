/* EXAMPLE 5.2.2 */

FILENAME COLLEGE 'T3_1_HEIGHTWT.dat';
DATA MALES;
  INFILE COLLEGE;
  INPUT Num Height Weight;
TITLE 'EXAMPLE 5.2.2';
PROC IML;
  USE MALES;
  READ ALL VAR{Height Weight} INTO X;
  N = NROW(X);
  XBAR = 1/N*X`*J(N,1);
  S = 1/(N-1)*X`*(I(N)-1/N*J(N))*X;
  MU = {70, 170};
  SIGMA = {20 100, 100 1000};
  ZSQR = N*((XBAR-MU)`*INV(SIGMA)*(XBAR-MU));
  z1 = SQRT(N)*(XBAR[1]-MU[1])/SQRT(SIGMA[1,1]);
  z2 = SQRT(N)*(XBAR[2]-MU[2])/SQRT(SIGMA[2,2]);
  PRINT ZSQR, z1, z2;
ENDSAS;