import random
import logging
import math
from pylab import arange


logging.basicConfig(level=logging.INFO)


def log(name, text):
    logging.getLogger(name).debug(text)


TASK_NEW, TASK_PROGRESS, TASK_SUSPENDED, TASK_FINISHED, TASK_KILLED = range(5)


class Task(object):
    ALL_TASKS = []
    ALL_TASKS_AP = []

    def __init__(self, env, duration, ap):
        self.env = env
        self.duration = duration
        self.creation_time = env.time
        self.state = TASK_NEW
        self.ap = ap
        self.last_work_time = self.creation_time
        self.waiting_time = 0
        if ap:
            log('tsk', "[%d] task produced %ds ABSOLUTE PRIORITY" % (env.time, self.duration))
        else:
            log('tsk', "[%d] task produced %ds" % (env.time, self.duration))
        if ap:
            Task.ALL_TASKS_AP.append(self)
        else:
            Task.ALL_TASKS.append(self)

    def suspend(self):
        if self.state != TASK_SUSPENDED:
            self.last_work_time = self.env.time
            self.state = TASK_SUSPENDED
            log('tsk', "[%d] task #%d suspended" % (self.env.time, self.id))

    def resume(self):
        if self.state != TASK_PROGRESS:
            self.waiting_time += self.env.time - self.last_work_time
            self.state = TASK_PROGRESS
            log('tsk', "[%d] task #%d resumed" % (self.env.time, self.id))

    def finished(self):
        self.state = TASK_FINISHED
        self.finish_time = self.env.time
        self.turnaround = self.finish_time - self.creation_time
        log('tsk', "[%d] task #%d finished. turnaround time: %d" %
            (self.env.time, self.id, self.turnaround))

    def kill(self):
        self.state = TASK_KILLED
        log('tsk', "[%d] task #%d killed" % (self.env.time, self.id))


def task_generator(env, task_f, task_d, ap):
    time = task_f()  # once per period
    prev_time = env.time
    diff = env.time + time
    while True:
        diff = env.time - prev_time
        while diff >= time:
            diff -= time
            task = Task(env, task_d(), ap)
            yield task
            prev_time = env.time
            time = task_f()
        yield None


def poisson(l):
    return -(1/float(l)) * math.log(random.random())


def def_task_generator(env):
    task_f = lambda: poisson(env.LAMBDA_DEF)  # random.random()*3*1000+2000  # 2000..5000
    task_d = lambda: random.random()*3*1000+1000  # 1000..4000
    return task_generator(env, task_f, task_d, False)


def ap_task_generator(env):
    task_f = lambda: poisson(env.LAMBDA_AP)  # random.random()*1.5*1000+4000  # 4000..5500
    task_d = lambda: random.random()*1*1000+500  # 500..1500
    return task_generator(env, task_f, task_d, True)


class Queue(list):
    pass


class BaseProcessor(object):
    def __init__(self, environment):
        self.new_tasks = []
        self.tid_count = 1
        self.environment = environment

    def add_task(self, task):
        task.id = self.tid_count
        self.tid_count += 1
        task.worktime = 0
        self.new_tasks.append(task)

    def tick(self):
        pass

TIME_QUANT = 400
THRESHOLDS = [3, 6, 20]
QUEUE_NUM = 3


class Processor(BaseProcessor):
    def __init__(self, env, quant=TIME_QUANT, q_num=QUEUE_NUM, thresholds=THRESHOLDS):
        super().__init__(env)
        self.qs = [Queue() for q in range(q_num)]
        self.q_ap = []
        self.current = None
        self.thresholds = thresholds
        self.quant = quant
        self.prev_time = env.time

    def get_new(self):
        self.current = None

        if len(self.q_ap):
            self.current = self.q_ap[0]
            self.current.queue = -1
            self.current.resume()
            self.q_ap.remove(self.current)
            return

        for q_id, queue in enumerate(self.qs):
            if len(queue) > 0:
                self.current = queue[0]
                self.current.queue = q_id
                self.current.resume()
                self.qs[self.current.queue].remove(self.current)
                break

    def tick(self):
        for task in self.new_tasks:
            task.loops = 0
            task.queue = 0
            if task.ap:
                self.q_ap.append(task)
            else:
                self.qs[0].append(task)
        self.new_tasks = []

        elapsed = self.environment.time - self.prev_time
        # log('cpu', "elapsed %d" % elapsed)
        self.prev_time = self.environment.time

        if not self.current:
            self.get_new()
            if self.current:
                self.current.session = 0

        if self.current:
            # elapsed = min(self.quant, self.current.duration -
                 # self.current.worktime)
            self.current.worktime += elapsed
            self.current.session += elapsed
            # log('cpu', "[%d] task #%d worktime %d AFTER" %
            #     (env.time, self.current.id, self.current.worktime))
            if self.current.worktime >= self.current.duration or \
               self.current.session >= self.quant or \
               (len(self.q_ap) and not self.current.ap):
                self.current.session = 0
                self.current.suspend()
                self.current.loops += 1
                if self.current.loops >= self.thresholds[self.current.queue] and \
                   not self.current.ap:
                    self.current.loops = 0
                    self.current.queue += 1
                    if self.current.queue >= len(self.qs):
                        self.current.kill()
                    else:
                        log('cpu', "task #%d moved to queue %d" %
                            (self.current.id, self.current.queue))
                if self.current.worktime < self.current.duration and \
                   self.current.state != TASK_KILLED:
                    if self.current.queue == -1:
                        self.q_ap.append(self.current)
                    else:
                        self.qs[self.current.queue].append(self.current)
                else:
                    self.current.finished()

                self.get_new()
                if self.current:
                    self.current.session = 0
        # return elapsed  # 0.6t period

    def is_empty(self):
        return all(len(q) == 0 for q in self.qs) and not self.current


class Environment(object):
    def __init__(self):
        self.time = 0
        self.time = 0
        self.tasks = def_task_generator(self)
        self.ap_tasks = ap_task_generator(self)
        self.processor = Processor(self)
        self.producing = True
        self.utilization_time = 0
        self.QUANT = 10
        self.LAMBDA_DEF = 0.0003
        self.LAMBDA_AP = 0.00005

    def is_empty(self):
        return self.processor.is_empty()

    def tick(self):
        if self.producing:
            task = next(self.tasks)
            while task is not None:
                self.processor.add_task(task)
                log('env', "[%d] added task #%d" % (self.time, task.id))
                task = next(self.tasks)

            task = next(self.ap_tasks)
            while task is not None:
                self.processor.add_task(task)
                log('env', "[%d] added task #%d" % (self.time, task.id))
                task = next(self.tasks)
        self.time += self.QUANT
        if self.processor.current:
            self.utilization_time += self.QUANT
        self.processor.tick()
        # log('env', "[%d] ticked" % (env.time))


def test(l_def, l_ap, time):
    env = Environment()
    env.LAMBDA_DEF = l_def
    env.LAMBDA_AP = l_ap
    while env.time < time:
        env.tick()

    prod = env.time
    env.producing = False
    while not env.is_empty():
        env.tick()
    print("SIMULATION FINISHED")

    results = {}

    results['overtime'] = env.time - prod
    print("%d overtime" % results['overtime'])

    results['utilization'] = (env.utilization_time / env.time)*100
    results['tasks processed'] = env.processor.tid_count
    results['AP tasks'] = len(Task.ALL_TASKS_AP)
    results['tasks/s'] = (env.processor.tid_count / (env.time / 1000))
    print("%4.2f%% utilization" % results['utilization'])
    print("%d tasks processed" % results['tasks processed'])
    print("%d AP tasks" % results['AP tasks'])
    print("%4.4f tasks/s" % results['tasks/s'])

    mean_turnaround_def = sum(t.turnaround for t in Task.ALL_TASKS) / len(Task.ALL_TASKS)
    results['mean turnaround def'] = mean_turnaround_def
    mean_turnaround_ap = sum(t.turnaround for t in Task.ALL_TASKS_AP) / len(Task.ALL_TASKS_AP)
    results['mean turnaround ap'] = mean_turnaround_ap
    print("%4.4f mean turnaround" % (mean_turnaround_def))
    print("%4.4f mean turnaround AP" % (mean_turnaround_ap))

    waiting_time = sum(t.waiting_time for t in Task.ALL_TASKS) / len(Task.ALL_TASKS)
    results['waiting time'] = waiting_time
    print("%4.4f waiting time" % waiting_time)
    waiting_time_AP = sum(t.waiting_time for t in Task.ALL_TASKS_AP) / len(Task.ALL_TASKS_AP)
    results['waiting time AP'] = waiting_time_AP
    print("%4.4f waiting time AP" % waiting_time_AP)

    sorted_tasks = sorted(Task.ALL_TASKS, key=lambda x: x.duration)

    waiting_times = []
    durations = []
    last_dur = sorted_tasks[0].duration
    vals = []

    waiting_times_qs = [[] for x in range(QUEUE_NUM)]
    durations_qs = [[] for x in range(QUEUE_NUM)]
    start_q_id = 0

    for i, dur in enumerate([t.duration for t in sorted_tasks]):
        if last_dur != dur:
            durations.append(last_dur)
            waiting_times.append(sum(vals)/len(vals))
            while last_dur > TIME_QUANT*(sum(THRESHOLDS[q_id] for q_id in range(0, start_q_id+1))):
                start_q_id += 1
            waiting_times_qs[start_q_id].append(sum(vals)/len(vals))
            durations_qs[start_q_id].append(last_dur)
            vals = []
        vals.append(sorted_tasks[i].waiting_time)
        last_dur = dur
    else:
        durations.append(last_dur)
        waiting_times.append(sum(vals)/len(vals))

    results['waiting times'] = waiting_times  # [t.waiting_time for t in sorted_tasks]
    results['durations'] = durations  # [t.duration for t in sorted_tasks]

    results['waiting times qs'] = waiting_times_qs
    results['durations qs'] = durations_qs
    return results


def make_plot(x, y, title_t, xlabel_t=u'интенсивность (lambda)', ylabel_t=u'время, usec', dot='b.:', clear=True):
    from pylab import plot, axis, xlabel, ylabel, grid, show, savefig, cla, rc
    rc('font', **{'family': 'serif'})
    rc('text', usetex=True)
    rc('text.latex', unicode=True)
    rc('text.latex', preamble='\\usepackage[utf8]{inputenc}')
    rc('text.latex', preamble='\\usepackage[russian]{babel}')

    plot(x, y, dot)
    # axis([0, 0.01, 0, 10000])
    ylabel(ylabel_t)
    xlabel(xlabel_t)
    grid()

    savefig('%s.png' % title_t.replace(" ", "_"))
    if clear:
        cla()


if __name__ == '__main__':
    time = 5000*600
    l_def_r = arange(0.00005, 0.0005, 0.000005)
    results = []
    for l_def in l_def_r:
        print ("Test: %f" % l_def)
        res = test(l_def, 0.00005, time)
        results.append(res)

    make_plot(l_def_r, [x['waiting time'] for x in results], 'waiting time')
    make_plot(l_def_r, [100-x['utilization'] for x in results], 'idle time')
    make_plot(l_def_r, [x['waiting time AP'] for x in results], 'waiting time AP')

    res = test(0.0002, 0.00005, time)
    make_plot(res['durations'], res['waiting times'], 'waiting by duration',
              'длительность, usec', 'время ожидание в очереди, usec', dot='b.')

    make_plot(res['durations qs'][0], res['waiting times qs'][0], 'waiting by duration with queues',
              'длительность, usec', 'время ожидание в очереди, usec', dot='b.', clear=False)
    make_plot(res['durations qs'][1], res['waiting times qs'][1], 'waiting by duration with queues',
              'длительность, usec', 'время ожидание в очереди, usec', dot='r.', clear=False)
    make_plot(res['durations qs'][2], res['waiting times qs'][2], 'waiting by duration with queues',
              'длительность, usec', 'время ожидание в очереди, usec', dot='g.', clear=True)

    make_plot([x['waiting time'] for x in results],
              [x['tasks processed'] for x in results], 'tasks count by waiting time',
              'время ожидание в очереди, usec', 'задач обработано', dot='b.:')