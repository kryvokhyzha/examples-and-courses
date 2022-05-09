/* EXAMPLE 7.4.3 */

TITLE 'EXAMPLE 7.4.3';
DATA PROBE;
  INFILE 'T3_5_PROBE.dat';
  INPUT Subject Pos1 Pos2 Pos3 Pos4 Pos5;
PROC IML;
  USE PROBE;
  READ ALL VAR{Pos1 Pos2 Pos3 Pos4 Pos5} INTO X;
  n = NROW(X);
  p = NCOL(X);
  S = 1/(n-1)*X`*(I(n)-1/n*J(n))*X;
  D = DIAG(S)##.5;
  R = INV(D)*S*INV(D);
  u = DET(R);
  uprime = -(n-1-((2*p+5)/6))*LOG(u);
  f = p*(p-1)/2;
  PRINT n,p,R,u,uprime,f;
ENDSAS;