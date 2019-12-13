import threading
import time


class MyThread(threading.Thread):
    def __init__(self, number, style, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self.number = number
        self.style = style

    def run(self, *args, **kwargs):
        print('thread started')
        super(MyThread, self).run(*args, **kwargs)
        print('thread finished')


def sleeper(num, style):
    print(f'sleeping for {num} sec style {style}')
    time.sleep(num)


t = MyThread(number=3, style='green', target=sleeper, args=(3, 'green'))
t.start()
