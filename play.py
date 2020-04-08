import signal
import os
import sys
import platform
import time
import copy
from multiprocessing import Process
from enum import IntEnum
from gomoku import Gomoku
from agent import Iterative_Deepening_Alpha_Beta
from tools import my_random as mrandom
from tools.tools import Printer

class Timeout(Exception):
    pass

class InvalidActionspace(Exception):
    pass

def timer_function(time_count):
    print('start waiting: %s'%time_count )
    time.sleep(time_count)
    print('Time\'s up!%s'%os.getppid())
    os.kill(os.getppid(), signal.SIGINT)

class Timer():

    def __init__(self):
        if platform.system() == 'Windows':
            signal.setitimer = self.windows_setitimer
            signal.ITIMER_REAL = None
            signal.SIGALRM = signal.SIGINT

        # Timer raises "timeout" exception when time runs out
        signal.signal(signal.SIGALRM, self.timeout)

    def set_timer(self, time):
        signal.setitimer(signal.ITIMER_REAL, time)

    def windows_setitimer(self, dummy, time):
        self.timer_process = Process(target=timer_function, args=(time,))
        print('process created')
        self.timer_process.start()
        print('new process id :%s'%(self.timer_process.pid))

    def timeout(self, signum, frame):
        raise Timeout('Timeout!!')

# 0. Initialize environment
timelimit = 10.0
env = Gomoku(board_size = 19)
timer = Timer()
printer = Printer()

# 1-1. Choose  player stone
input_valid = False
while(input_valid == False):
    # Print options
    print('Choose your stone')
    for i, player_info in env.player_info.iterrows():
        print('%s: %s, '%( i, player_info['name']), end = '')
    print('\n',end='')

    # Receive input, convert to int
    i = input()
    try:
        i = int(i)
    except:
        os.system('clear')
        print('Invalid input! Choose between the options')
        continue

    # Check if player selection is valid
    if i in env.player_info.index:
        player_index = i
        input_valid = True
    else:
        print('Invalid input! Choose between the options')
        continue
print('You chose %s. Game start'%(env.player_info.loc[player_index]['name']))

# 1-2. Create Agnet
agent_index = env.player_info[env.player_info.index != player_index].index[0]
agent = Iterative_Deepening_Alpha_Beta(env = copy.deepcopy(env), player_index = agent_index)

# 2. Game start
winner = None
done = False
while(done == False):
    # 0-1] Print
    # os.system('clear')
    print('Next Player: %s'%( env.player_info.loc[env.next_player]['name'] ) )
    action = None
    env.show()

    # 0-2] Set time limit
    timer.set_timer(timelimit)

    # 1-1] Game move Search (try&except to abort code. Did not use signal handling since it cannot interrupt user input() )
    try:
        # 1) User's turn
        if env.next_player == player_index:
            # Receive valid input
            input_valid = False
            while(input_valid == False):
                print('Your next move: (Row, Column) ', end='')
                x = input()
                # Check input validity
                try:
                    row, column = x.split(',')
                    row = row.upper()
                    if (row not in env.action_space[0]) or (column not in env.action_space[1]):
                        raise InvalidActionspace('Row: [%s ~ %s], Column: [%s ~ %s]'%(env.action_space[0][0], env.action_space[0][-1], env.action_space[1][0], env.action_space[1][-1]))
                    else:
                        action = (row, column)
                        input_valid = True
                # Loop for new input only when these errors happen. (Not timeout or other types of errors)
                except ValueError as error:
                    print(error)
                except InvalidActionspace as error:
                    print(error)

        # 2) Agent's turn
        else:
            action = agent.search(env.board)

    # 1-2] Timeout
    except Timeout as timeout_message:
        print(timeout_message)
        # 1) User's turn - Random selection with Uniform probability
        if env.next_player == player_index:
            pass
        # 2) Agent's turn
        else:
            action = agent.action

    # If there is no action - Random selection with Uniform probability
    if action == None:
        print('No action! Performing random action')
        action = mrandom.choice(env.actions())

    # 2] Perform one move
    _, winner, done, _ = env.step(action, env.next_player)

# 3. Game results
env.show()
if winner != None:
    print('Winner is: %s'%(env.player_info.loc[winner]['name']))
else:
    print("It's a tie!")
