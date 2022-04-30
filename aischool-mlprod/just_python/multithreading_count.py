import time
from threading import Thread

COUNT = 50000000


def countdown(n):
    while n > 0:
        n -= 1


def run_single_thread():
    start = time.time()
    countdown(COUNT)
    end = time.time()
    print('Elapsed time:', end - start)


def run_multi_thread(cores=4):
    start = time.time()
    threads = [Thread(target=countdown, args=(COUNT // cores,)) for _ in range(cores)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    end = time.time()
    print(f'Elapsed time {cores} cores:', end-start)


if __name__ == '__main__':
    run_single_thread()
    run_multi_thread()
