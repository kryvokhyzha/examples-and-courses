import threading


l = threading.Lock()
x = 0
COUNT = 10000


def adding_2():
    global x

    with l:
        for i in range(COUNT):
            x += 2


def adding_3():
    global x

    with l:
        for i in range(COUNT):
            x += 3


def subtracting_4():
    global x

    with l:
        for i in range(COUNT):
            x -= 4


def subtracting_1():
    global x

    with l:
        for i in range(COUNT):
            x -= 1


for i in range(COUNT):
    t1 = threading.Thread(target=adding_2)
    t2 = threading.Thread(target=adding_3)
    t3 = threading.Thread(target=subtracting_4)
    t4 = threading.Thread(target=subtracting_1)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    if x != 0:
        print(x)
        break

print(x)
