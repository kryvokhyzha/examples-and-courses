/* EXAMPLE 3.9.1 (a) */

FILENAME PROBE 'T3_5_PROBE.dat';
DATA WORD;
  INFILE PROBE;
  INPUT Subject Pos1 Pos2 Pos3 Pos4 Pos5;
PROC IML;
TITLE 'EXAMPLE 3.9.1 (a)';
  USE WORD;
  READ ALL VAR{Pos1 Pos2 Pos3 Pos4 Pos5} INTO X;
  N = NROW(X);
  XBAR = 1/N*X`*J(N,1);
  S = 1/(N-1)*X`*(I(N)-1/N*J(N))*X;
  A = {3, -2, 4, -1, 1};
  Z = (A`*X`)`;
  ZBAR = 1/N*Z`*J(N,1);                 /*  ZBAR = A`*XBAR; */
  Sz = 1/(N-1)*Z`*(I(N)-1/N*J(N))*Z;    /*  Sz = A`*S*A;    */
  PRINT XBAR, S, ZBAR, Sz;

  B = {1, 3, -1, 1, -2};
  UBAR = B`*XBAR;
  Su = B`*S*B;
  Szu = A`*S*B;
  Rzu = Szu/(Sz#Su)##.5;
  PRINT UBAR, Su, Szu, Rzu;

  A = {1 1 1 1 1, 2 -3 1 -2 -1, -1 -2 1 -2 3};
  ZBAR = A*XBAR;
  SZ = A*S*A`;
  D = DIAG(Sz)##.5;
  R = INV(D)*Sz*INV(D);
  B = {1 -1 -3 1 -2, -2 3 -1 2 -1};
  Szw = A*S*B`;
  PRINT ZBAR, Sz, R, D, Szw;
ENDSAS;