proc iml;
A = {17	17	12,
     11	9	13,
     11	8	19,
     14	7	28};
n = sum(a);
P = A/n;
rp = P*j(ncol(A),1,1);
cp = j(1,nrow(A),1)*P;
Dr = diag(rp);
Dc = diag(cp);
R = inv(Dr)*P;
C = P*inv(Dc);
print R,C;
quit;
