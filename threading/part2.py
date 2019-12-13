import threading
import time


def sleeper(n, name):
    print(f'Process {name} would sleep.')
    time.sleep(n)
    print(f'Process {name} has just woken up.')


t = threading.Thread(target=sleeper, name='Thread1', args=(5, 'Thread1'))

thread_list = []

start = time.time()

for i in range(5):
    t = threading.Thread(target=sleeper,
                        name=f'thread_{i}',
                        args=(5, f'thread_{i}'))

    thread_list.append(t)
    t.start()

    print(f'{t.name} has start')

for t in thread_list:
    t.join()

print('time = {}'.format(time.time() - start))
print('All threads are done')
