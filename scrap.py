
if __name__ == '__main__':
    print('current:%s'%(os.getpid()))
    timer = Timer()
    print(signal.getsignal(signal.SIGALRM))
    timer.set_timer(1)
# os.kill(13032, signal.SIGFPE)
    while(True):
        try:
            pass
        except:
            timer.set_timer(1)
        # time.sleep()
        pass
signal.pause()
help(signal.getsignal)
list(signal.Handlers)
help(signal.set_wakeup_fd)

help(signal._enum_to_int)
signal._int_to_enum
signal._enum_to_int(Signals.SIGALRM)
Signals.SIGALRM
timer = Timer()
help(globals)
globals()
help('modules')
signal.signal(signal.SIGALRM, timeout)
signal.SIGALRM
timer.timer_process.start()
timer.timer_process.pid
timer.timer_process.kill()
signal._signal.__doc__
print(signal._signal.__doc__)
signal._
os.name
signal.SIGINT
os.kill(8492, signal.SIGINT)
os.kill(7920,signal.SIGFPE)
for i in signal.Signals:
    print(i)



import numpy as np
board = np.array([
[1,0,0,-1,-1,0,0,0,0],
[0,1,0,0,0,0,0,0,0],
[0,-1,-1,-1,0,0,0,0,0],
[0,0,0,0,-1,0,0,-1,0],
[1,0,0,0,0,-1,0,0,0],
[0,0,1,0,0,1,0,0,0],
[1,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,1,0,0],
[0,0,0,1,0,0,0,0,0]
])
env.board = board

from tools import my_random as mrandom

from gomoku import Gomoku
import copy
player_index = 2
env = Gomoku()
self = Iterative_Deepening_Alpha_Beta(env = copy.deepcopy(env), player_index = player_index)
env.step(('H','3'), 1)
env.step(('H','4'), 1)
env.step(('H','5'), 1)
env.step(('G','5'), 2)
env.step(('F','5'), 2)
env.step(('E','5'), 2)
env.step(('D','5'), 2)
env.show()
action_values = pd.Series(index = self.env.actions(env.board), dtype = str)
action_values = pd.Series(index = [('G','6'),('H','2'),('H','6'),('I','6')], dtype = str)
action_values
env.step(('D','8'), 2)
action_values[:] = 'unknown'
state = env.board
self.max_depth = 4
print(action_values)
alpha
beta
v
