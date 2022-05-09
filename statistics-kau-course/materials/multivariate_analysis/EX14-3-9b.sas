data chain;  
input group $ Y1 Y2;
datalines;
A1  1.01 1.03
A2  0.80 1.74
A3  1.58 2.25
A4  1.84 0.77
A5  1.92 1.23
A6  2.06 1.87
A7  1.23 1.55
A8  0.47 1.42
A9  1.35 2.87
A10 2.26 0.68
A11 1.65 1.75
A12 2.02 2.47
A13 2.33 2.79
A14 2.61 1.72
A15 2.72 0.84
A16 3.35 1.96
A17 2.77 2.87
B1  3.34 3.24
B2  3.77 3.61
B3  4.10 4.00
B4  4.58 4.64
C1  5.64 9.02
C2  5.86 7.47
C3  5.34 5.38
C4  5.55 6.66
C5  6.07 5.63
C6  6.63 6.56
C7  6.86 6.19
C8  6.82 7.92
C9  8.06 6.34
C10 7.71 7.41
C11 5.49 8.63
C12 5.26 7.57
C13 5.58 5.80
C14 5.25 6.98
C15 6.67 5.36
C16 6.94 7.03
C17 6.06 6.56
C18 6.41 7.38
C19 7.72 6.19
C20 7.32 7.96
C21 5.76 5.23
;

symbol pointlabel=("#group") font=, value=dot;
proc gplot data=chain;
plot y2*y1;
run;quit;
symbol pointlabel=none;

proc cluster data=chain method=single outtree=outt noprint nonorm;id group;run;
proc tree data=outt;id group;run;

proc cluster data=chain method=average outtree=outt noprint nonorm;id group;run;
proc tree data=outt;id group;run;



