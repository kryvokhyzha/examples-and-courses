package com.mathpar.NAUKMA.examples;

import mpi.MPI;
import mpi.MPIException;

import java.util.Arrays;

public class TestScatter {
    public static void main(String[] args) throws MPIException{
        // ініціалізація MPI
        MPI.Init(args);
        // визначення номера процесора
        int myrank = MPI.COMM_WORLD.getRank();
        // визначенння числа процесорів в групі
        int np = MPI.COMM_WORLD.getSize();
        int n = 6;
        // оголошуємо масив об'єктів
        int[] a = new int[n];
        // заповнюємо цей масив на нульовому процесорі
        if (myrank == 0){
            for (int i = 0; i < n; i++){
                a[i] = i ;
            }
            System.out.println("myrank = " + myrank + ": a = " + Arrays.toString(a));
        }
        // оголошуємо масив, в який будуть записуватись
        // прийняті процесором елементи
        int[] q = new int[n/2];
        MPI.COMM_WORLD.scatter(a, 3, MPI.INT, q, n/2, MPI.INT, 0);
        // роздруковуємо отримані масиви і номера процесорів
        System.out.println("myrank = " + myrank + ": q = " + Arrays.toString(q));

        // завершення паралельної частини
        MPI.Finalize();
    }
}
