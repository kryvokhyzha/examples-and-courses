package com.mathpar.NAUKMA.examples;

import mpi.MPI;
import mpi.MPIException;

import java.nio.IntBuffer;
import java.util.Random;
public class TestISendAndIRecv {
    public static void main(String[] args) throws MPIException {

        MPI.Init(args);

        int myrank = MPI.COMM_WORLD.getRank();

        int np = MPI.COMM_WORLD.getSize();

        int n = 5;

        IntBuffer b = MPI.newIntBuffer(n);

        if (myrank == 0) {
            for (int i = 0; i < n; i++) {
                b.put(new Random().nextInt(10));
            }
            for (int i = 1; i < np; i++) {
                MPI.COMM_WORLD.iSend(b, b.capacity(), MPI.INT, i, 3000);
            }
            System.out.println("proc num = " + myrank + " array sent");

        } else {
            MPI.COMM_WORLD.recv(b, b.capacity(), MPI.INT, 0, 3000);
            System.out.println("proc num = " + myrank + " array received");

        }
        MPI.Finalize();
    }
}
