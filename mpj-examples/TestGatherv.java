package com.mathpar.NAUKMA.examples;

import mpi.MPI;
import mpi.MPIException;

import java.util.Arrays;

/*
mpirun --hostfile /home/andriy/hostfile -np 2 java -cp /home/andriy/mpi-dap/target/classes com/mathpar/NAUKMA/course4/Ivaskevich/TestGatherv 10
*/

/*
Output:
 0
 0
 1
 1
 1
 1
 1
 1
 1
 1
 1
 1
 0
 0
 0
 0
 0
 0
 0
 0
 */
public class TestGatherv {
    public static void main(String[] args) throws MPIException {
        // ініціалізація MPI
        MPI.Init(args);
        // визначення номера процесора
        int myrank = MPI.COMM_WORLD.getRank();
        // визначення числа процесорів в групі
        int np = MPI.COMM_WORLD.getSize();
        int n = 5;
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = myrank*10+i;
        }
        System.out.println("myrank = " + myrank + ": a = " + Arrays.toString(a));
        int[] q = new int[n * np];
        MPI.COMM_WORLD.gatherv(a, n, MPI.INT, q,
                new int[]{n, n}, new int[]{0, 5},
                MPI.INT, np - 1);

        if (myrank == np - 1) {
            System.out.println("myrank = " + myrank + ": q = " + Arrays.toString(q));
        }
        // завершення паралельної частини
        MPI.Finalize();
    }
}
