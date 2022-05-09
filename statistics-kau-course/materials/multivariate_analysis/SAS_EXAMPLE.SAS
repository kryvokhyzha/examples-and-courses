*  This file is an example of the use of Proc IML in SAS. 
* Any line that starts with a '*' is regarded as a comment 
* by SAS and is ignored when running. Also anything enclosed
* in /* */ is seen as a comment.
/* These are useful for making comments like this
   or for making SAS skip a portion of the command file
   that you do not want to delete but also don't want to run a 
   particular time.
*/
;
options ls=72; /* this makes the output fit on an 80 column output screen */
data head;
infile 'head.dat';
      input group y1-y6;
* These 3 lines set up a SAS Data set named 'head' and then read the data
* from the file 'head.dat'.  The first column in the file becomes the
* variable 'group' and the next 6 columns become the variables y1
* through y6.  Note: look at the data file first to see what format
* the data needs to be read in. Some files contain a subject column
* that is not used in the analysis, but if it is not accounted for then
* you will read the data into the wrong columns.  See a SAS manual
* for further information on reading in data.
run;

proc iml; 
 
use head;  /* We will be getting the data from SAS Data set 'head' */
read all var {group} into group;
read all var {y1, y2, y3, y4, y5, y6} into y;
/*
      Read the variable group into a column vector called 'group'.
and the variables y1-y6 into an nx6 matrix called 'y'.
*/
 
start t2(y,mu);
      n=nrow(y);
      p=ncol(y);
      ybar=1/n*y`*J(n,1);   /* Equation 3.17 */
      s=1/(n-1)*y`*(I(n)-1/n*J(n))*y;   /* Equation 3.27 */
      t2=n*(ybar-mu)`*inv(s)*(ybar-mu);  /* Equation 5.4 */
     print n p, ybar mu, s, "T squared =" t2;
finish;

* The previous 8 lines define a module (subroutine) named t2.
* This module expects 2 pieces of input, a matrix y and a 
* vector mu.  This module computes Hotelling's T squared
* test of H0: mean vector = mu.  Note: in the print statement, 
* variables separated by a space will be printed next to each other,
* and variables separated by comma's will be above and below each other.

;
reset print; /* this ensures that everything we do will be output. */

      n=nrow(y);
      p=ncol(y); 
* set the variables 'n' and 'p' from the matrix.;

y1=y[1:30,];
y2=y[31:60,];
y3=y[61:90,];
* these 3 lines break up the matrix into the 3 groups. 
* the first subscript indicates the rows to use. and the second gives
* the columns ('1:30' means 1 through 30).;
temp1=y1||y2;  /* This horizontally concatenates the 2 matrices into
                  a 30x12 matrix.   */
temp2=y1//y2;  /* This vertically concatenates the 2 matrices into
                  a 60x6 matrix     */
reset noprint; /* turn automatic printing off. */

run t2(y1,{0,0,0,0,0,0});
m2={1,2,3,4,5,6};
run t2(y2,m2);
run t2(y3,1/n*y`*J(n,1));
* These run our module 't2' on the three matrices, testing against
* different mu's.

quit;  /* Quit IML.  You are now back in regular SAS. */

* IML has some built in matrices, e.g.,
* I(n) is an nxn Identity matrix.
* J(n) is an nxn matrix of 1's.
* J(n,p) is an nxp matrix of 1's.
* J(n,p,r) is an nxp matrix of r's.


endsas;  /* Quit SAS. */
