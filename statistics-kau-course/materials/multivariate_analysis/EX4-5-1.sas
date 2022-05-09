/* EXAMPLE 4.5.2 */

FILENAME RAMUS 'T3_6_BONE.dat';
DATA BONES;
  INFILE RAMUS;
  INPUT OBS AGE8 AGE8_5 AGE9 AGE9_5;
TITLE 'EXAMPLE 4.5.1';
PROC IML;
  USE BONES;
  READ ALL VAR{AGE8 AGE8_5 AGE9 AGE9_5} INTO X;
  N = NROW(X);
  P = NCOL(X);
  XBAR = 1/N*X`*J(N,1);
  XBARM = REPEAT(XBAR,1,N);                  /* NxN MATRIX OF XBAR VALUES */
  S = 1/(N-1)*X`*(I(N)-1/N*J(N))*X;
  D = (X`-XBARM)`*INV(S)*(X`-XBARM);
  Di2 = VECDIAG(D);
  SIGHAT = 1/N*X`*(I(N)-1/N*J(N))*X;
  G = (X`-XBARM)`*INV(SIGHAT)*(X`-XBARM);
  b1p = SUM(G##3)/N##2;
  b2p = TRACE(G##2)/N;
  PRINT Di2, b1p, b2p;

  U = N*Di2/(N-1)##2;
  create Usort from U;
  append from U;
  close Usort;
  sort Usort by col1;
  use usort;
  read all var{col1} into U;
  alpha = (p-2)/(2*p);
  beta = (n-p-3)/(2*(n-p-1));
  a = p/2;
  b = (n-p-1)/2;
  V = J(n,1);
  do i = 1 to n;
     prob = (i-alpha)/(n-alpha-beta+1);
     V[i] = betainv(prob,a,b);
  end;
  plotpts = V||U;
  colnme = {"vi","ui"};
  create QQ from plotpts[colname=colnme];
  append from plotpts[colname=colnme];
quit;

goptions reset=all;
proc gplot data=QQ;
   plot vi*ui/vaxis=axis2 haxis=axis1;
   symbol v=dot;
   axis1 order=(0 to 1 by .2) label=(h=1.2 f=centbi);
   axis2 order=(0 to 1 by .2) label=(h=1.2 a=90 r=0 f=centbi);
run;quit;
