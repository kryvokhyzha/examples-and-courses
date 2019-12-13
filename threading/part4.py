import threading
import time


class MyThread(threading.Thread):
    def __init__(self, number, func, args):
        threading.Thread.__init__(self)

        self.number = number
        self.func = func
        self.args = args

    def run(self):
        print(f'{self.number} has started!')
        self.func(*self.args)
        print(f'{self.number} has finished!')


def double(number, cycles):
    for i in range(cycles):
        number += number
    print(number)


threds_list = []

for i in range(50):
    t = MyThread(number=i+1, func=double, args=(i, 3))
    threds_list.append(t)
    t.start()

for t in threds_list:
    t.join()
