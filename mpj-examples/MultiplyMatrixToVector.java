package com.mathpar.NAUKMA.examples;

import com.mathpar.matrix.MatrixS;
import com.mathpar.number.*;
import mpi.MPI;
import mpi.MPIException;

import java.io.IOException;
import java.util.Random;

public class MultiplyMatrixToVector {
    public static void main(String[] args) throws MPIException,
            IOException, ClassNotFoundException {

        Ring ring = new Ring("Z[]");
        MPI.Init(args);
        int rank = MPI.COMM_WORLD.getRank();
        int size = MPI.COMM_WORLD.getSize();
        int ord = 16; // matrix size (ord х ord)
        int k = ord / size; // the number of rows for each processor
        int n = ord - k * (size - 1); // the last portion will be n (less than k) elements )
        if (rank == 0) {
            int den = 10000; // for density=100%
            Random rnd = new Random();
            MatrixS A = new MatrixS(ord, ord, den, new int[]{5},rnd, NumberZ.ONE, ring);
            System.out.println("Matrix A = " + A.toString());
            VectorS B = new VectorS(ord, den, new int[]{5},rnd, ring);
            System.out.println("Vector B = " + B.toString());
            Element[] result = new Element[ord]; // For resulting vector
            for (int j = 1; j < size; j++) {
                Element[][] Mj=new Element[k][];
                int[][] colj=new int[k][];
                for (int s = 0; s < k; s++) {
                    Mj[s]=A.M[s+j*k]; colj[s]=A.col[s+j*k];
                }
                MatrixS Aj=new MatrixS(Mj,colj);
                Transport.sendObject(Aj, j, 1);
                Transport.sendObject(B, j, 2);
            }
            Element[][] M0=new Element[n][];  int[][] col0=new int[n][];
            for (int s = 0; s < n; s++) {
                M0[s]=A.M[s+(size-1)*k]; col0[s]=A.col[s+(size-1)*k];
            }
            MatrixS A0=new MatrixS(M0,col0);
            VectorS V0=A0.multiplyByColumn(B.transpose(ring), ring);
            System.arraycopy(V0.V, 0, result, (size-1)*k, n);
            for (int t = 1; t < size; t++) {
                VectorS Vt = (VectorS)Transport.recvObject(t, t);
                System.arraycopy(Vt.V, 0, result,(t - 1) * k, k);
            }
            System.out.println("RESULT: A*B=" + new VectorS(result).toString(ring));
        } else {
            MatrixS AA = (MatrixS)Transport.recvObject(0, 1 );
            System.out.println(  " AA("+rank+") = " + AA.toString(ring));
            VectorS BB = (VectorS)Transport.recvObject(0, 2 );
            System.out.println(  " BB("+rank+") = " + BB.toString(ring));
            VectorS VV=AA.multiplyByColumn(BB.transpose(ring), ring);
            System.out.println(  " VV("+rank+") = " + VV.toString(ring));
            Transport.sendObject(VV, 0,  rank);
            System.out.println("send result from("+rank+")");
        }
        MPI.Finalize();
    }
}
