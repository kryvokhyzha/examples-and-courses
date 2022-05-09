/* EXAMPLES 3.2.1 and 3.2.2 */

FILENAME COLLEGE 'T3_1_heightwt.dat';
DATA MALES;
  INFILE COLLEGE;
  INPUT Num Height Weight;
PROC IML;
  USE MALES;
  READ ALL VAR{Height Weight} INTO Z;
  RESET PRINT;
  PRINT 'EXAMPLE 3.2.1';
  N = NROW(Z);
  XBAR = 1/N*Z[,1]`*J(N,1);
  YBAR = 1/N*Z[,2]`*J(N,1);
  sumXY    = Z[,1]`*Z[,2];
  Sxy = 1/(N-1)*(sumXY-N*XBAR*YBAR);

  PRINT 'EXAMPLE 3.2.2';
  sumX2 = Z[,1]`*Z[,1];
  sumY2 = Z[,2]`*Z[,2];
  Sx = (1/(N-1)*(sumX2-N*XBAR**2))##.5;
  Sy = (1/(N-1)*(sumY2-N*YBAR**2))##.5;
  Rxy = Sxy/(Sx*Sy);
ENDSAS;
