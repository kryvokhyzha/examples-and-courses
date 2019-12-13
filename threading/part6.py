import threading
import queue
import time


def putting_thread(q):
    while True:
        print('start thread')
        time.sleep(10)
        q.put(5)
        print('sup something')


q = queue.Queue()
t = threading.Thread(target=putting_thread, args=(q,), daemon=True)
t.start()

q.put(0)
print(q.get(), 'first item')
print('----')

print(q.get(), 'finish')
