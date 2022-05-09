/* EXAMPLE 5.6.2 */

FILENAME PSYCH 'T5_1_PSYCH.dat';
DATA SCORES;
  INFILE PSYCH;
  INPUT Sex Test1 Test2 Test3 Test4;
  IF Sex=1 THEN Y=0.5;
  IF Sex=2 THEN Y=-0.5;
TITLE 'EXAMPLE 5.6.2';
PROC GLM;
  MODEL Y=Test1 Test2 Test3 Test4;
PROC IML;
  USE SCORES;
  READ ALL VAR {Test1 Test2 Test3 Test4} INTO X;
  X1 = X[1:32,];
  X2 = X[33:64,];
  N1 = NROW(X1);
  N2 = NROW(X2);
  R2 = .611532;
  T2 = (N1+N2-2)*R2/(1-R2);
  PRINT T2;
quit;
