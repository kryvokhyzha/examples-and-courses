/* EXAMPLES 3.5, 3.6 and 3.7 */

FILENAME TURNIPS 'T3_3_CALCIUM.dat';
DATA CALCIUM;
  INFILE TURNIPS;
  INPUT Num Avail Exchange Turnip;
PROC IML;
  USE CALCIUM;
  READ ALL VAR{Avail Exchange Turnip} INTO X;
  RESET PRINT;
  N=NROW(X);
  PRINT 'EXAMPLE 3.5';
    XBAR=1/N*X`*J(N,1);
  PRINT 'EXAMPLE 3.6';
    S=1/(N-1)*X`*(I(N)-1/N*J(N))*X;
  PRINT 'EXAMPLE 3.7';
    D=DIAG(S)##.5;
    R=INV(D)*S*INV(D);
ENDSAS;