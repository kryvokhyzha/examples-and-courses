/* EXAMPLE 10.6 */

TITLE 'EXAMPLE 10.6';
DATA CHEM;
  INFILE 'T10_1_CHEM.dat';
  INPUT NUM Y1-Y3 X1-X3;
PROC IML;
  USE CHEM;
  READ ALL VAR {Y1 Y2 Y3 X1 X2 X3} INTO X;
  reset print;
  n = NROW(X);
  p = NCOL(X);
  S = 1/(n-1)*X`*(I(n)-1/n*J(n))*X;
  Syy = S[1:3,1:3];
  Syx = S[1:3,4:6];
  Sxy = S[4:6,1:3];
  Sxx = S[4:6,4:6];
  R2M = DET(Syx*INV(Sxx)*Sxy)/DET(Syy);
  RV = TRACE(Sxy*Syx)/SQRT(TRACE(Sxx*Sxx)*TRACE(Syy*Syy));  
ENDSAS;
