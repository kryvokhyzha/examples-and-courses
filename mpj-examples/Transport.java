package com.mathpar.NAUKMA.examples;

import mpi.MPI;
import mpi.MPIException;
import mpi.Status;

import java.io.*;
import java.nio.ByteBuffer;
import java.util.logging.Level;
import java.util.logging.Logger;


public class Transport {

    public static void sendArrayOfObjects(Object[] a,
                                          int proc, int tag) throws MPIException,
            IOException {
        for (int i = 0; i < a.length; i++) {
            sendObject(a[i], proc, tag + i);
        }
    }


    public static Object[] recvArrayOfObjects(int proc, int tag)
            throws MPIException, IOException,
            ClassNotFoundException {

        Object[] o = new Object[4];
        for (int i = 0; i < 4; i++) {
            o[i] = recvObject(proc, tag + i);
        }
        return o;
    }

    public static void sendObject(Object a, int proc, int tag)
            throws MPIException, IOException {
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(bos);
        oos.writeObject(a);
        byte[] tmp = bos.toByteArray();
        MPI.COMM_WORLD.send(tmp, tmp.length, MPI.BYTE, proc, tag);
    }


    public static Object recvObject(int proc, int tag)
            throws MPIException, IOException,
            ClassNotFoundException {

        Status st = MPI.COMM_WORLD.probe(proc, tag);

        int size = st.getCount(MPI.BYTE);

        byte[] tmp = new byte[size];

        MPI.COMM_WORLD.recv(tmp, size, MPI.BYTE, proc, tag);
        Object res = null;
        ByteArrayInputStream bis = new ByteArrayInputStream(tmp);
        ObjectInputStream ois = new ObjectInputStream(bis);
        res = ois.readObject();

        return res;
    }


    public static void sendObjects(Object[] a, int proc, int tag)
            throws MPIException {
        ByteArrayOutputStream bos = null;
        try {
            bos = new ByteArrayOutputStream();
            ObjectOutputStream oos =
                    new ObjectOutputStream(bos);
            for (int i = 0; i < a.length; i++) {
                oos.writeObject(a[i]);
            }
            bos.toByteArray();
        } catch (Exception ex) {
            Logger.getLogger(Transport.class.getName()).
                    log(Level.SEVERE, null, ex);

        }
        byte[] temp = bos.toByteArray();
        ByteBuffer buf = MPI.newByteBuffer(temp.length);
        buf.put(temp);
        MPI.COMM_WORLD.iSend(buf, temp.length,
                MPI.BYTE, proc, tag);

    }


public static Object[] recvObjects(int m, int proc, int tag)
        throws MPIException {
    Status s = MPI.COMM_WORLD.probe(proc, tag);
    int n = s.getCount(MPI.BYTE);
    byte[] arr = new byte[n];
    MPI.COMM_WORLD.recv(arr, n, MPI.BYTE, proc, tag);
    Object[] res = new Object[m];
    try {
        ByteArrayInputStream bis =
                new ByteArrayInputStream(arr);
        ObjectInputStream ois = new ObjectInputStream(bis);
        for (int i = 0; i < m; i++) {
            res[i] = ois.readObject();
        }
    } catch (Exception ex) {
        Logger.getLogger(Transport.class.getName()).
                log(Level.SEVERE, null, ex);

    }
    return res;
}
}