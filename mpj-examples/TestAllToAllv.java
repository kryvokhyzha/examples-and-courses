package com.mathpar.NAUKMA.examples;

import mpi.MPI;
import mpi.MPIException;

import java.util.Arrays;

/*
mpirun --hostfile /home/andriy/hostfile -np 1 java -cp /home/andriy/mpi-dap/target/classes com/mathpar/NAUKMA/course4/Ivaskevich/TestAllToAllv 2
 */

/*
Output:
myrank = 0; 0
myrank = 0; 1
 */
public class TestAllToAllv {
    public static void main(String[] args) throws MPIException {
        // ініціалізація MPI
        MPI.Init(args);
        // визначення номера процесора
        int myrank = MPI.COMM_WORLD.getRank();
        int n = 4;
        Integer[] a = new Integer[n];
        for (int i = 0; i < n; i++) {
            a[i] = myrank*10+i;
        }
        System.out.println("myrank = " + myrank + ": a = " + Arrays.toString(a));
        Integer[] q = new Integer[n];
        MPI.COMM_WORLD.allToAllv(a, new int[]{1, 1, 1, 1},
                new int[]{0, 1, 2, 3}, MPI.INT, q, new int[]{1, 1, 1, 1},
                new int[]{3, 2, 1, 0}, MPI.INT);

        System.out.println("myrank = " + myrank + ": q = " + Arrays.toString(q));

        // завершення паралельної частини
        MPI.Finalize();
    }
}
