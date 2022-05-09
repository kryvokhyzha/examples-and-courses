/* EXAMPLE 7.4.1 */
options ls=72;
TITLE 'EXAMPLE 7.4.1';
DATA DIAB;
  INFILE 'T3_4_DIABETES.dat';
  INPUT subject Y1 Y2 X1 X2 X3;
PROC IML;
  USE DIAB;
  READ ALL VAR {Y1 Y2 X1 X2 X3} INTO X;
  X2=X;
  N = NROW(X2);
  M = NCOL(X2);
  Q = 2;                                 /*  Q = # Y's  */
  P = M-Q;                               /*  P = # X's  */
  S = 1/(N-1)*X2`*(I(N)-(1/N)*J(N))*X2;
  Syy = S[1:Q,1:Q];     
  Sxx = S[Q+1:M,Q+1:M];
  dets=det(s);
  detsy=det(syy);
  detsx=det(sxx);
  WILK = DET(S)/(DET(Syy)*DET(Sxx));
  DF = N-1-P;
  PRINT S,Syy,Sxx,dets,detsy,detsx,WILK,DF;
ENDSAS;