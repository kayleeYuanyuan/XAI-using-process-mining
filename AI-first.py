import random
import sys
import math
import copy
import time
import csv

summay_process = {}
aggregate_similar_states = {}
results = {}
fieldnames = ['Case', 'Event']
filename = 'AI-firstPlayer.csv'


def transformation(board):
    position = copy.deepcopy(board)
    # rot90
    rot90 = {}
    rot90['1'] = position['7']
    rot90['2'] = position['4']
    rot90['3'] = position['1']
    rot90['4'] = position['8']
    rot90['5'] = position['5']
    rot90['6'] = position['2']
    rot90['7'] = position['9']
    rot90['8'] = position['6']
    rot90['9'] = position['3']
    # rot180
    rot180 = {}
    rot180['1'] = position['9']
    rot180['2'] = position['8']
    rot180['3'] = position['7']
    rot180['4'] = position['6']
    rot180['5'] = position['5']
    rot180['6'] = position['4']
    rot180['7'] = position['3']
    rot180['8'] = position['2']
    rot180['9'] = position['1']
    # rot270
    rot270 = {}
    rot270['1'] = position['3']
    rot270['2'] = position['6']
    rot270['3'] = position['9']
    rot270['4'] = position['2']
    rot270['5'] = position['5']
    rot270['6'] = position['8']
    rot270['7'] = position['1']
    rot270['8'] = position['4']
    rot270['9'] = position['7']
    # updown
    updown = {}
    updown['1'] = position['7']
    updown['2'] = position['8']
    updown['3'] = position['9']
    updown['4'] = position['4']
    updown['5'] = position['5']
    updown['6'] = position['6']
    updown['7'] = position['1']
    updown['8'] = position['2']
    updown['9'] = position['3']
    # leftright
    leftright = {}
    leftright['1'] = position['3']
    leftright['2'] = position['2']
    leftright['3'] = position['1']
    leftright['4'] = position['6']
    leftright['5'] = position['5']
    leftright['6'] = position['4']
    leftright['7'] = position['9']
    leftright['8'] = position['8']
    leftright['9'] = position['7']
    # diagonal1
    diagonal1 = {}
    diagonal1['1'] = position['1']
    diagonal1['2'] = position['4']
    diagonal1['3'] = position['7']
    diagonal1['4'] = position['2']
    diagonal1['5'] = position['5']
    diagonal1['6'] = position['8']
    diagonal1['7'] = position['3']
    diagonal1['8'] = position['6']
    diagonal1['9'] = position['9']
    # diagonal2
    diagonal2 = {}
    diagonal2['1'] = position['9']
    diagonal2['2'] = position['6']
    diagonal2['3'] = position['3']
    diagonal2['4'] = position['8']
    diagonal2['5'] = position['5']
    diagonal2['6'] = position['2']
    diagonal2['7'] = position['7']
    diagonal2['8'] = position['4']
    diagonal2['9'] = position['1']
    return [position, rot90, rot180, rot270, updown, leftright, diagonal1, diagonal2]

def is_same(board1, board2):
    # rot90
    rot90 = board1['1'] == board2['7'] and board1['2'] == board2['4'] and board1['3'] == board2['1'] and \
            board1['4'] == board2['8'] and board1['5'] == board2['5'] and board1['6'] == board2['2'] and \
            board1['7'] == board2['9'] and board1['8'] == board2['6'] and board1['9'] == board2['3']
    # rot180
    rot180 = board1['1'] == board2['9'] and board1['2'] == board2['8'] and board1['3'] == board2['7'] and \
             board1['4'] == board2['6'] and board1['5'] == board2['5'] and board1['6'] == board2['4'] and \
             board1['7'] == board2['3'] and board1['8'] == board2['2'] and board1['9'] == board2['1']
    # rot270
    rot270 = board1['1'] == board2['3'] and board1['2'] == board2['6'] and board1['3'] == board2['9'] and \
             board1['4'] == board2['2'] and board1['5'] == board2['5'] and board1['6'] == board2['8'] and \
             board1['7'] == board2['1'] and board1['8'] == board2['4'] and board1['9'] == board2['7']
    # updown
    updown = board1['1'] == board2['7'] and board1['2'] == board2['8'] and board1['3'] == board2['9'] and \
             board1['4'] == board2['4'] and board1['5'] == board2['5'] and board1['6'] == board2['6'] and \
             board1['7'] == board2['1'] and board1['8'] == board2['2'] and board1['9'] == board2['3']
    # leftright
    leftright = board1['1'] == board2['3'] and board1['2'] == board2['2'] and board1['3'] == board2['1'] and \
                board1['4'] == board2['6'] and board1['5'] == board2['5'] and board1['6'] == board2['4'] and \
                board1['7'] == board2['9'] and board1['8'] == board2['8'] and board1['9'] == board2['7']
    # diagonal1
    diagonal1 = board1['1'] == board2['1'] and board1['2'] == board2['4'] and board1['3'] == board2['7'] and \
                board1['4'] == board2['2'] and board1['5'] == board2['5'] and board1['6'] == board2['8'] and \
                board1['7'] == board2['3'] and board1['8'] == board2['6'] and board1['9'] == board2['9']
    # diagonal2
    diagonal2 = board1['1'] == board2['9'] and board1['2'] == board2['6'] and board1['3'] == board2['3'] and \
                board1['4'] == board2['8'] and board1['5'] == board2['5'] and board1['6'] == board2['2'] and \
                board1['7'] == board2['7'] and board1['8'] == board2['4'] and board1['9'] == board2['1']
    return rot90 or rot180 or rot270 or updown or leftright or diagonal1 or diagonal2


class TicTacToe(object):

    def __init__(self):
        self.position = {}
        for i in range(1, 10):
            self.position[str(i)] = ' '
        self.board = None
        self.update()
        self.player = 'O'
        self.computer = 'X'
        self.goFirst = 'computer'
        self.process= []
        self.result = ""

    def update(self):
        """update board"""
        self.board = f"{self.position['1']}|{self.position['2']}|{self.position['3']}\n-+-+-\n{self.position['4']}|" \
                     f"{self.position['5']}|{self.position['6']}\n-+-+-\n{self.position['7']}|{self.position['8']}|" \
                     f"{self.position['9']}"

    def printf(self):
        """print board"""
        self.update()
        print(self.board)

    def player_available(self):
        possible_pos = []
        for i in self.position:
            if self.position[i] == ' ':
                possible_pos.append(i)
        return possible_pos

    def playerMove(self):
        """choose location to put player's chess"""
        self.printf()
        location = random.choice(self.player_available())
        self.position[location] = self.player
        print("Random move is: " + location)
        # self.process.append(location)
        # self.process.append(['X', location])
        position1 = copy.deepcopy(self.position)
        has = False
        for state in aggregate_similar_states:
            state_dic = eval(state)
            if position1 == state_dic:
                self.process.append(str(position1))
                has = True
                break
            elif is_same(position1, state_dic):
                self.process.append(aggregate_similar_states[state][0])
                has = True
                break
        if not has:
            aggregate_similar_states[str(position1)] = transformation(position1)
            self.process.append(str(position1))

    def computerMove(self):
        """choose location to put computer's chess"""
        position = copy.deepcopy(self.position)
        best = self.ect(position)
        #self.state[best] = position
        self.position[best] = self.computer
        # self.process.append(best)

        position1 = copy.deepcopy(self.position)
        if len(aggregate_similar_states) == 0:
            aggregate_similar_states[str(position1)] = transformation(position1)
        has = False
        for state in aggregate_similar_states:
            state_dic = eval(state)
            if position1 == state_dic:
                self.process.append(str(position1))
                has = True
                break
            elif is_same(position1, state_dic):
                self.process.append(aggregate_similar_states[state][0])
                has = True
                break
        if not has:
            aggregate_similar_states[str(position1)] = transformation(position1)
            self.process.append(str(position1))

    def check_two_positions(self, board, location, chess):
        combinations = {'1' : [['1','2','3'], ['1', '5', '9'], ['1', '4', '7']],
                        '2' : [['1', '2' ,'3'], ['2', '5', '8']],
                        '3' : [['1', '2', '3'], ['3', '5', '7'], ['3', '6', '9']],
                        '4' : [['4', '5', '6'], ['1', '4', '7']],
                        '5' : [['1', '5', '9'], ['2', '5', '8'], ['4', '5', '6'], ['3', '5', '7']],
                        '6' : [['4', '5', '6'], ['3', '6', '9']],
                        '7' : [['1', '3', '7'], ['7', '8', '9'], ['3', '5', '7']],
                        '8' : [['2', '5', '8'], ['7', '8', '9']],
                        '9' : [['7', '8', '9'], ['3', '6', '9'], ['1', '5', '9']]}
        count = 0
        for i in combinations[location]:
            item = 0
            empty = 0
            for j in i:
                if board[j] == chess:
                    item += 1
                elif board[j] == ' ':
                    empty += 1
            if item == 2 and empty == 1:
                count += 1
        return count

    @staticmethod
    def fill(position, chess):
        p = copy.deepcopy(position)
        for i in range(1, 10):
            if p[str(i)] == ' ':
                p[str(i)] = chess
        return p

    def ect(self, position):
        alpha = {}
        targe = '1'
        for i in range(1, 10):
            copyComputerPosition = copy.deepcopy(position)
            if copyComputerPosition[str(i)] == ' ':
                copyComputerPosition[str(i)] = self.computer
                beta = math.inf
                for j in range(1, 10):
                    copyPlayerPosition = copy.deepcopy(copyComputerPosition)
                    if copyPlayerPosition[str(j)] == ' ':
                        copyPlayerPosition[str(j)] = self.player
                        player_position = self.fill(copyPlayerPosition, self.player)
                        computer_position = self.fill(copyPlayerPosition, self.computer)
                        Min = 0
                        if player_position['1'] == self.player and player_position['2'] == self.player and \
                                player_position['3'] == self.player:
                            Min += 1
                        if player_position['1'] == self.player and player_position['4'] == self.player and \
                                player_position['7'] == self.player:
                            Min += 1
                        if player_position['4'] == self.player and player_position['5'] == self.player and \
                                player_position['6'] == self.player:
                            Min += 1
                        if player_position['2'] == self.player and player_position['5'] == self.player and \
                                player_position['8'] == self.player:
                            Min += 1
                        if player_position['7'] == self.player and player_position['8'] == self.player and \
                                player_position['9'] == self.player:
                            Min += 1
                        if player_position['3'] == self.player and player_position['6'] == self.player and \
                                player_position['9'] == self.player:
                            Min += 1
                        if player_position['1'] == self.player and player_position['5'] == self.player and \
                                player_position['9'] == self.player:
                            Min += 1
                        if player_position['3'] == self.player and player_position['5'] == self.player and \
                                player_position['7'] == self.player:
                            Min += 1
                        Max = 0
                        if computer_position['1'] == self.computer and computer_position['2'] == self.computer and \
                                computer_position['3'] == self.computer:
                            Max += 1
                        if computer_position['1'] == self.computer and computer_position['4'] == self.computer and \
                                computer_position['7'] == self.computer:
                            Max += 1
                        if computer_position['4'] == self.computer and computer_position['5'] == self.computer and \
                                computer_position['6'] == self.computer:
                            Max += 1
                        if computer_position['2'] == self.computer and computer_position['5'] == self.computer and \
                                computer_position['8'] == self.computer:
                            Max += 1
                        if computer_position['7'] == self.computer and computer_position['8'] == self.computer and \
                                computer_position['9'] == self.computer:
                            Max += 1
                        if computer_position['3'] == self.computer and computer_position['6'] == self.computer and \
                                computer_position['9'] == self.computer:
                            Max += 1
                        if computer_position['1'] == self.computer and computer_position['5'] == self.computer and \
                                computer_position['9'] == self.computer:
                            Max += 1
                        if computer_position['3'] == self.computer and computer_position['5'] == self.computer and \
                                computer_position['7'] == self.computer:
                            Max += 1
                        exp_beta = Max - Min
                        if exp_beta < beta:
                            beta = exp_beta
                alpha[str(i)] = beta + self.check_two_positions(copyComputerPosition, str(i), self.computer)
        max_value = -math.inf
        for key, value in alpha.items():
            if value > max_value:
                max_value = value
                targe = key
        # for i in range(1, 10):
        #     position = self.position.copy()
        #     if position[str(i)] == ' ':
        #         position[str(i)] = self.computer
        #         if self.checkWinner(position, self.computer):
        #             targe = str(i)
        #             break
        #         position[str(i)] = self.player
        #         if self.checkWinner(position, self.player):
        #             targe = str(i)
        #             break
        for i in range(1, 10):
            position = self.position.copy()
            if position[str(i)] == ' ':
                position[str(i)] = self.computer
                if self.checkWinner(position, self.computer):
                    targe = str(i)
                    return targe
        for i in range(1, 10):
            position = self.position.copy()
            if position[str(i)] == ' ':
                position[str(i)] = self.player
                if self.checkWinner(position, self.player):
                    targe = str(i)
                    break
        return targe

    @staticmethod
    def checkWinner(position, chess):
        return (position['1'] == chess and position['2'] == chess and position['3'] == chess) or \
               (position['1'] == chess and position['4'] == chess and position['7'] == chess) or \
               (position['4'] == chess and position['5'] == chess and position['6'] == chess) or \
               (position['2'] == chess and position['5'] == chess and position['8'] == chess) or \
               (position['7'] == chess and position['8'] == chess and position['9'] == chess) or \
               (position['3'] == chess and position['6'] == chess and position['9'] == chess) or \
               (position['1'] == chess and position['5'] == chess and position['9'] == chess) or \
               (position['3'] == chess and position['5'] == chess and position['7'] == chess)

    def checkDraw(self):
        end = True
        for i in range(1, 10):
            if self.position[str(i)] == ' ':
                end = False
        if not self.checkWinner(self.position, self.player) and not self.checkWinner(self.position, self.computer) and end:
            return True
        return False

    def checkBoard(self):
        if self.checkWinner(self.position, self.player):
            self.printf()
            print("Player wins! ")
            self.result = "Player wins! "
            return True
            #sys.exit()
        if self.checkWinner(self.position, self.computer):
            self.printf()
            print("AI wins! ")
            self.result = "AI wins! "
            return True
            #sys.exit()
        if self.checkDraw():
            self.printf()
            print("It's a tie!")
            self.result = "It's a tie!"
            return True
            #sys.exit()
        return False

    def run(self):
        """run the game"""
        while True:
            self.computerMove()
            if self.checkBoard():
                break
            self.playerMove()
            if self.checkBoard():
                break

if __name__ == '__main__':
    for i in range(10000):
        t = TicTacToe()
        t.run()
        summay_process[i + 1] = t.process
        results[i + 1] = t.result
    # print(aggregate_similar_states)
    # print(len(aggregate_similar_states))
    # print(summay_process)


    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for case in summay_process:
            for i in range(len(summay_process[case])):
            # for process in summay_process[case]:
                # process.append(summay_process[case].index(process) + 1)
                row = {'Case': case, 'Event': summay_process[case][i]}
                writer.writerow(row)
            row1 = {'Case': case, 'Event': results[case]}
            writer.writerow(row1)





