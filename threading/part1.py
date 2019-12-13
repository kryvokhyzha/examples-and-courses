import threading
import time


def sleeper(n, name):
    print(f'Process {name} would sleep.')
    time.sleep(n)
    print(f'Process {name} has just woken up.')


t = threading.Thread(target=sleeper, name='Thread1', args=(5, 'Thread1'))
t.start()
t.join()

print('Finish!')
