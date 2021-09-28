package com.mathpar.NAUKMA.examples;

import mpi.MPI;
import mpi.MPIException;

import java.util.Arrays;

public class TestAllGatherv {
    public static void main(String[] args) throws MPIException,
            InterruptedException {

        // ініціалізація MPI
        MPI.Init(args);
        // визначення номера процесора
        int myrank = MPI.COMM_WORLD.getRank();
        int n = 5;
        int[] a = new int[n];
        int np = MPI.COMM_WORLD.getSize();
        for (int i = 0; i < n; i++) {
            a[i] = myrank*10+i;
        }
        System.out.println("myrank = " + myrank + ": a = " + Arrays.toString(a));
        int[] q = new int[n * np];
        MPI.COMM_WORLD.allGatherv(a, n, MPI.INT,
                q, new int[]{n, n}, new int[]{5, 0}, MPI.INT);

        System.out.println("myrank = " + myrank + ": q = " + Arrays.toString(q));
        // завершення паралельної частини
        MPI.Finalize();
    }
}