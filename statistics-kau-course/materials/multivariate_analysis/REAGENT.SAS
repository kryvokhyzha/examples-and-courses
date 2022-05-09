/* Inputs the data in table 6.19 into two formats.
Data set "reagent" has the data listed as in the data set on the disk.
Variables: REAGENT SUBJECT Y1 Y2 Y3.  80 observations with 5 variables.
All of the observations for Reagent 1 are listed followed by all observations
of Reagent 2 followed by Reagent 3 then Reagent 4.

Data set "repeat" has the data as listed in Table 6.19.
Variables: SUBJECT Y1 Y2 Y3 Y4 Y5 Y6 Y7 Y8 Y9 Y10 Y11 Y12. 20 observations with
13 variables.
Y1-Y3 are y1-y3 listed in table 6.19 for Reagent 1.  Y4-Y6 are y1-y3 listed
in table 6.19 for Reagent 2.  Y7-Y9 for Reagent 3.  Y10-Y12 for Reagent 4.*/


options ps=55 ls=78 nocenter;


data a b c d;
infile '/u1/hill/hmwrk/st611/data/reagent.dat';

input reagent subject y1-y3 @;
if reagent=1 then output a;
if reagent=2 then output b;
if reagent=3 then output c;
if reagent=4 then output d;
run;


data reagent;
 merge a b c d;
 by reagent subject;
run;


data b;
set b;
 y4=y1;
 y5=y2;
 y6=y3;
 drop y1-y3;
run;

data c;
set c;
 y7=y1;
 y8=y2;
 y9=y3;
 drop y1-y3;
run;

data d;
set d;
 y10=y1;
 y11=y2;
 y12=y3;
 drop y1-y3;
run;


data repeat;
 merge a b c d;
 by subject;
 drop reagent;
run;



