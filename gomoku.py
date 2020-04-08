import numpy as np
import pandas as pd
import os
import time

class Gomoku():
    def __init__(self, board_size = 19, win_condition = 5):
        self.player_info = pd.DataFrame(
        {'stone_code': (1,-1),
        'name': ('black', 'white')}
        , index=[1,2]
        )

        self.num_player = len(self.player_info)
        self.next_player_index = 0
        self.next_player = 1 # 1st player

        # Initialize board
        self.board_size = board_size
        self.board = np.zeros((self.board_size,self.board_size), dtype = int)

        # Number of consecutive stones to win
        self.win_condition = win_condition

        # row_info, column_info map "string" indices to its corresponding "integer" indices
        self.row_info = { chr( ord('A') + x ) : x for x in range(self.board_size) }
        self.column_info = {str(x+1) : x for x in range(self.board_size)}
        self.row_names = list(self.row_info)
        self.column_names = list(self.column_info)
        self.action_space = [self.row_names, self.column_names]

        # Search direction. Entries indicate slope of scan direction
        self.direction = ['-1', '0', '1', 'inf']
        self.forward = {
        '-1': np.array([1,1]),
        '0': np.array([0,1]),
        '1': np.array([-1,1]),
        'inf': np.array([-1,0]),
        }
        self.backward = {
        '-1': np.array([-1,-1]),
        '0': np.array([0,-1]),
        '1': np.array([1,-1]),
        'inf': np.array([1,0]),
        }

    def reset(self):
        self.board = np.zeros((self.board_size,self.board_size))

    def show(self, board = None):
        '''Show contents in board'''
        # 1. Current board
        if type(board) == type(None):
            # 1. Print Column names
            print('{:<3}'.format(''),end='')
            for column_name in self.column_names:
                print('{:<3}'.format(column_name), end='')
            print('\n', end='')

            for row, row_name in zip(self.board, self.row_names):
                print('{:<3}'.format(row_name), end='')
                for column in row:
                    if column == 0:
                        print('{:<3}'.format('+'), end='')
                    elif column == 1:
                        print('{:<3}'.format('○'), end='')
                    elif column == -1:
                        print('{:<3}'.format('●'), end='')
                    else:
                        assert False, 'wrong data in board'
                print('\n', end='')

        # 2. New board
        else:
            # 1. Print Column names
            print('{:<3}'.format(''),end='')
            for column_name in self.column_names:
                print('{:<3}'.format(column_name), end='')
            print('\n', end='')

            for row, row_name in zip(board, self.row_names):
                print('{:<3}'.format(row_name), end='')
                for column in row:
                    if column == 0:
                        print('{:<3}'.format('+'), end='')
                    elif column == 1:
                        print('{:<3}'.format('○'), end='')
                    elif column == -1:
                        print('{:<3}'.format('●'), end='')
                    else:
                        assert False, 'wrong data in board'
                print('\n', end='')

    def step(self, stone_loc, player_index):
        self.move(stone_loc, player_index)
        done, winner = self.terminal_test(stone_loc)
        return self.board, winner, done, None

    def move(self, stone_loc, player_index):
        row, column = stone_loc
        row_index = self.row_info[row]
        column_index = self.column_info[column]
        stone_loc_index = (row_index, column_index)
        stone = self.player_info.loc[player_index]['stone_code']

        if self.is_illegal(stone_loc_index, stone):
            pass
            # print('Illegal Move!! Your turn has passed...')
        else:
            self.board[stone_loc_index] = stone

        self.next_player_index = (self.next_player_index + 1) % self.num_player
        self.next_player = self.player_info.index[self.next_player_index]

    def actions(self, board = None):
        '''Return list of tuple[(x1,y1),(x2,y2),...] actions indicating locations where there are adjacent stones'''
        # 1. Board to search
        if type(board) == type(None):
            board = self.board
        # 2. If board is empty
        if (board==0).all() == True:
            return self.all_actions()

        actions = list()
        # 3. Search for all stone locations, for places which adjacent stones exist
        for row_index in range(self.board_size):
            for column_index in range(self.board_size):
                # 1] If there is no stone here
                stone_loc_index = np.asarray([row_index, column_index])
                if board[tuple(stone_loc_index)] == 0:
                    # 1) Search all adjacent 8 directions
                    for search_direction in list(self.forward.values()) + list(self.backward.values()):
                        scan_loc = stone_loc_index + search_direction
                        # If the scan location is inside the board, check if there's a stone
                        if ((0<=scan_loc).all() and (scan_loc<=self.board_size-1).all()):
                            # If there's stone on the scan location, append action
                            if board[tuple(scan_loc)] != 0:
                                actions.append( (self.row_names[row_index], self.column_names[column_index]) )
                                break

        return actions

    def all_actions(self, board = None):
        '''Return list of tuple[(x1,y1),(x2,y2),...] actions indicating all possible locations'''
        # 1. Current board
        if type(board) == type(None):
            board = self.board

        # 2. Search for all places without stone
        actions_row, actions_column = np.where(board == 0)
        actions = list()
        for row_index, column_index in zip(actions_row, actions_column):
            actions.append( (self.row_names[row_index], self.column_names[column_index]) )
        return actions

    def terminal_test(self, stone_loc):
        row, column = stone_loc
        row_index = self.row_info[row]
        column_index = self.column_info[column]
        stone_loc_index = (row_index, column_index)
        # 1. When there are "win_condition" stones
        for i, direction in enumerate(self.direction):
            counted_stones = self.count_consecutive_stones(stone_loc_index, direction, max_stones = self.win_condition + 1)

            # If counted stones meets win condition
            if counted_stones == self.win_condition:
                stone = self.board[stone_loc_index]
                # Search player index that matches stone code
                return True, self.player_info.index[self.player_info['stone_code']==stone][0]

        # 2. If the board is full but there is no winner
        if (self.board != 0).all() :
            return True, None
        # 3. Game hasn't ended yet
        return False, None

    def terminal_test_all(self):
        '''For every stone, perform terminal_test'''
        # 1. Scan search space (stone location)
        search_space_row, search_space_column = np.where(self.board != 0)
        search_space_row = np.asarray(self.row_names)[search_space_row]
        search_space_column = np.asarray(self.column_names)[search_space_column]

        # 2. For each move in the search space, check for moves [right, right-down, down]
        for row, column in zip(search_space_row, search_space_column):
            done, winner = self.terminal_test((row,column))
            if done == True:
                return True, winner

        # 3. If the board is full but there is no winner
        if (self.board != 0).all() :
            return True, None

        # 4. Game hasn't ended yet
        return False, None

    def count_consecutive_stones(self, stone_loc_index, direction, max_stones = 6):
        stone_loc_index = np.asarray(stone_loc_index)
        stone = self.board[stone_loc_index[0], stone_loc_index[1]]
        # If no stone present
        if stone == 0:
            return 0
        # 1. Backward search
        stone_count = 1
        scan_loc = stone_loc_index + self.backward[direction]

        # While scan location is inside the boundaries
        while( (0<=scan_loc).all() and (scan_loc<=self.board_size-1).all() ):
            stone_scanned = self.board[scan_loc[0], scan_loc[1]]

            # Same stone found
            if stone_scanned == stone:
                stone_count += 1
            else:
                break

            # If enough stone is found, return
            if stone_count >= max_stones:
                return stone_count

            # Move scan
            scan_loc += self.backward[direction]

        # 2. Forward search
        scan_loc = stone_loc_index + self.forward[direction]

        # While scan location is inside the boundaries
        while( (0<=scan_loc).all() and (scan_loc<=self.board_size-1).all() ):
            stone_scanned = self.board[scan_loc[0], scan_loc[1]]

            # Same stone found
            if stone_scanned == stone:
                stone_count += 1
            else:
                break

            # If enough stone is found, return
            if stone_count >= max_stones:
                return stone_count

            # Move scan
            scan_loc += self.forward[direction]

        return stone_count

    def is_illegal(self, stone_loc_index, stone):
        row_index, column_index = stone_loc_index
        # 1. Stone already exists
        if self.board[row_index, column_index] != 0:
            return True

        # 2. 3*3
        # Temporarily place stone
        self.board[stone_loc_index] = stone
        counted_stones = np.zeros_like(self.direction, dtype=int)
        for i, direction in enumerate(self.direction):
            counted_stones[i] = self.count_consecutive_stones(stone_loc_index, direction, max_stones = 4)
        # Remove stone
        self.board[stone_loc_index] = 0
        # If exactly 2 cases of 3 consecutive stones happen, it's illegal
        if sum(counted_stones==3) == 2:
            return True

        return False
