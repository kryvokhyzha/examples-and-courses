/* EXAMPLE 5.3.2 */

FILENAME TURNIPS 'T3_3_CALCIUM.dat';
DATA CALCIUM;
  INFILE TURNIPS;
  INPUT Num Avail Exchange Turnip;
TITLE 'EXAMPLE 5.3.2';
PROC IML;
  USE CALCIUM;
  READ ALL VAR{Avail Exchange Turnip} INTO X;
  N = NROW(X);
  RESET PRINT;
  MU = {15, 6, 2.85};
  XBAR = 1/N*X`*J(N,1);
  S = 1/(N-1)*X`*(I(N)-1/N*J(N))*X;
  T2 = N*(XBAR-MU)`*INV(S)*(XBAR-MU);
ENDSAS;