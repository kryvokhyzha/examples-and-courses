import threading
import time


total = 4


def creates_item():
    global total

    for i in range(10):
        time.sleep(2)
        print(f'iteration {i}')
        total += 1

    print('iterations done')


def create_items_2():
    global total

    for i in range(7):
        time.sleep(1)
        print(f'iteration {i}')
        total += 1

    print('iterations done')


def limits_items():
    global total
    while True:
        if total > 5:
            print('Overloaded')
            total -= 3
            print('subtracted by 3')
        else:
            time.sleep(1)
            print('waiting')


creates1 = threading.Thread(target=creates_item)
creates2 = threading.Thread(target=create_items_2)
limiter = threading.Thread(target=limits_items, daemon=True)

creates1.start()
creates2.start()
limiter.start()

creates1.join()
creates2.join()
# limiter.join()

print(f'Finish. Total iterations = {total}')
