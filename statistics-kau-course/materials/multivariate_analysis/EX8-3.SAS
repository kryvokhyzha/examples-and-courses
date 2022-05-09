/* EXAMPLE 8.3 */

FILENAME PSYCH 'T5_1_PSYCH.dat';
DATA SCORES;
  INFILE PSYCH;
  INPUT Sex Test1 Test2 Test3 Test4;
TITLE 'EXAMPLE 8.3';
PROC IML;
  USE SCORES;
  READ ALL VAR {Test1 Test2 Test3 Test4} INTO X;
  X1 = X[1:32,];
  X2 = X[33:64,];
  N1 = NROW(X1);
  N2 = NROW(X2);
  X1BAR = 1/N1*X1`*J(N1,1);
  X2BAR = 1/N2*X2`*J(N2,1);
  S1 = 1/(N1-1)*X1`*(I(N1)-1/N1*J(N1))*X1;
  S2 = 1/(N2-1)*X2`*(I(N2)-1/N2*J(N2))*X2;
  Spl = 1/(N1+N2-2)*((N1-1)*S1+(N2-1)*S2);
  RESET PRINT;
  D2 = (X1BAR-X2BAR)`*INV(Spl)*(X1BAR-X2BAR);
  a = INV(Spl)*(X1BAR-X2BAR);
  b = (N1*N2/((N1+N2)*(N1+N2-2)+N1*N2*D2))*a;
  R2 = (X1BAR-X2BAR)`*b;
ENDSAS;