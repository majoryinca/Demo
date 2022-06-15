import unittest
import random

import os
clear = lambda: os.system('clear')

BASE_POINTS = 1
MAX_DIE_VALUE = 6
MINI_BONUS_POINTS = 5
BONUS_POINTS = 11


class RollDice():
    def __init__(self, max_round=6):
        self.seq = []
        self.players = 2
        self.max_round = max_round

        self.current_round = 1
        self.current_player = 0

        self.total_scores = [0] * self.players
        self.bonuses = [0] * self.players
        self.temp_mini_bonus = [0] * self.players
        self.temp_bonus = [0] * self.players
        self.mini_bonuses = [0] * self.players

    def gaming(self, seq):
        self.seq = seq
        game_end = False
        if len(seq) == 0:
            self.seq = [[-1,-1,-1]] * self.players
            while not game_end:
                
                print(f"Current round: {self.current_round}, Current Player: {self.current_player}")
                
                print(f"player 0 score: {self.total_scores[0]}, player 1 score: {self.total_scores[1]}")
                # print(f"Current player bonus: {self.bonuses[0]}")
                # print(f"Current player mini_bonus: {self.mini_bonuses[0]}")
                # print(f"Current player temp bonus: {self.temp_bonus[0]}")
                # print(f"Current player temp mini_bonus: {self.temp_mini_bonus[0]}")

                print("\n")
                hit_key = input("Hit the Enter key to roll the dices:")
                clearConsole()
                self.roll_dice()
                to_next_round = self.calc_single_roll(self.current_player)
                tie_breaker_check = True if  (self.current_round > self.max_round) and to_next_round else False
                if tie_breaker_check:
                    hit_key = input(f"begin to calc winner: current player {self.current_player} current round {self.current_round}")
                    if self.calc_winner():
                        game_end = True
                        break  

        else:   
            for chunk_id in range(len(self.seq)):
                to_next_round = self.calc_single_roll(chunk_id)
                tie_breaker_check = True if  (self.current_round > self.max_round) and to_next_round else False
                if tie_breaker_check or (chunk_id == len(self.seq) - 1):
                    if self.calc_winner():
                        break
        #print(self.total_scores)
        print("Game over!")
        return self.total_scores

    def roll_dice(self):
        new_chunk = []
        while len(new_chunk) < 3:
            new_chunk.append(random.randint(1, MAX_DIE_VALUE))
        self.seq[self.current_player] = new_chunk
        str_chunk = [str(item) for item in new_chunk]
        print(f"current player: {self.current_player}" + "new dice values:" + ",".join(str_chunk))


    '''If score no points, return False and this turn ends. Otherwise return True'''

    def calc_single_roll(self, chunk_id):
        to_next_round = False
        score_flg = self.calc_chunk_score(
            self.seq[chunk_id])
        if self.get_temp_mini_bonus() > 0 and score_flg:
            self.set_mini_bonus()
            self.set_total_score(MINI_BONUS_POINTS)
        if self.get_temp_bonus() > 0 and score_flg:
            self.set_bonus()
            self.set_total_score(BONUS_POINTS)
        self.clear_temp_bonus()

        # set temporary bonus score
        self.set_temp_bonus_score(
            self.seq[chunk_id])

        if not score_flg:
            # current player turn ends and  it is another player turn
            self.current_player = (self.current_player + 1) % self.players
            print(f"next player will be {self.current_player}\n")

            # current turn ends while it is the last player. increment the current round
            if self.current_player % self.players == 0:

                # print(f'The current round {self.current_round}:')
                # for i in range(0, self.players):
                #     print(f'player index {i}: total score: {self.total_scores[i]}, mini bonus: {self.mini_bonuses[i]}, bonus: {self.bonuses[i]}')
                # print("\n")

                self.current_round += 1
                print(f"will move to next round:{self.current_round}\n")
                to_next_round = True
        return to_next_round

    def calc_winner(self):
        if self.find_single_max_exists(self.total_scores):
            return True
        elif self.find_single_max_exists(self.bonuses):
            return True
        elif self.find_single_max_exists(self.mini_bonuses):
            return True
        else:
            return False

    '''implement Turn Scoring Rules'''

    def calc_chunk_score(self, chunk):
        base_score_flg = False
        temp_bonus_flg = self.check_temp_bonus_score(
            chunk)
        if not temp_bonus_flg:
            base_points = self.calc_basepoint(chunk)
            if base_points > 0:
                self.total_scores[self.current_player] += base_points
                base_score_flg = True

        return base_score_flg or temp_bonus_flg

    '''implement the * of a kind Turn Scoring Rules'''

    def check_temp_bonus_score(self, chunk):
        temp_bonus_flg = False
        if self.calc_bonus(chunk):
            temp_bonus_flg = True
        if self.calc_mini_bonus(chunk):
            temp_bonus_flg = True
        return temp_bonus_flg

    def set_temp_bonus_score(self, chunk):
        if self.calc_bonus(chunk):
            self.temp_bonus[self.current_player] += BONUS_POINTS
        if self.calc_mini_bonus(chunk):
            self.temp_mini_bonus[self.current_player] += MINI_BONUS_POINTS

    def get_temp_mini_bonus(self):
        return self.temp_mini_bonus[self.current_player]

    def get_temp_bonus(self):
        return self.temp_bonus[self.current_player]

    def set_total_score(self, score):
        self.total_scores[self.current_player] += score

    def set_bonus(self):
        self.bonuses[self.current_player] += BONUS_POINTS

    def set_mini_bonus(self):
        self.mini_bonuses[self.current_player] += MINI_BONUS_POINTS

    def clear_temp_bonus(self):
        self.temp_mini_bonus[self.current_player] = 0
        self.temp_bonus[self.current_player] = 0

    # helper

    def find_single_max_exists(self, score_list):
        max_val = max(score_list)
        count = 0
        for s in score_list:
            if s == max_val:
                count += 1
        if count > 1:
            return False
        else:
            return True

    def calc_basepoint(self, chunk):
        '''base point rule'''
        base_points = 0
        for roll_val in chunk:
            if roll_val == self.current_round:
                base_points += BASE_POINTS
        return base_points

    def calc_bonus(self, chunk):
        for i in range(1, len(chunk)):
            if chunk[i] != chunk[0]:
                break
        else:
            '''bonus rule'''
            if chunk[0] == self.current_round:
                return True
        return False

    def calc_mini_bonus(self, chunk):
        for i in range(1, len(chunk)):
            if chunk[i] != chunk[0]:
                break
        else:
            '''mini bonus rule'''
            if chunk[0] != self.current_round:
                return True
        return False

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

# Unit test


class TestGame(unittest.TestCase):

    # def test_original_sample(self):
    #     game_instance = RollDice()
    #     sample_input = [
    #         [1, 1, 3], [4, 2, 1], [6, 6, 2],
    #         [2, 1, 6], [5, 4, 1], [3, 3, 3], [3, 4, 5],
    #         [4, 5, 2], [2, 2, 2], [4, 4, 4], [6, 3, 5],
    #         [4, 1, 3]
    #     ]

    #     output = game_instance.gaming(sample_input)
    #     self.assertEqual(output, [15, 2], str(output))

    # def test_tiebreaker_sample(self):
    #     game_instance = RollDice(1)
    #     sample_input = [
    #         [2, 2, 3], [2, 2, 3], 
    #         [2, 1, 1],[1, 3, 3], [2, 1, 1], [1, 3, 3]
    #     ]

    #     output = game_instance.gaming(sample_input)
    #     self.assertEqual(output, [1, 1], str(output))

    # def test_tiebreaker_2_sample(self):
    #     game_instance = RollDice(1)
    #     sample_input = [
    #         [2, 2, 3], [2, 2, 3], 
    #         [2, 1, 1]
    #     ]

    #     output = game_instance.gaming(sample_input)
    #     self.assertEqual(output, [1, 0], str(output))
    
    # def test_over_rounds_sample(self):
    #     game_instance = RollDice(8)
    #     sample_input = [
    #         [1, 1, 3], [4, 2, 1], [6, 6, 2],
    #         [2, 1, 6], [5, 4, 1], [3, 3, 3], [3, 4, 5],
    #         [4, 5, 2], [2, 2, 2], [4, 4, 4], [6, 3, 5],
    #         [4, 1, 3]
    #     ]

    #     output = game_instance.gaming(sample_input)
    #     self.assertEqual(output, [15, 2], str(output))

    def test_play_sample(self):
        game_instance = RollDice(1)
        sample_input = [
        ]

        output = game_instance.gaming(sample_input)
        self.assertEqual(output, [13, 5], str(output))

    # def test_less_dice_sample(self):
    #     game_instance = RollDice(8)
    #     sample_input = [
    #         [1, 1], [4, 1], [6,  2],
    #         [2,  6], [5,  1], [3, 3], [3, 5],
    #         [4, 2], [2, 2], [4, 4], [6, 5],
    #         [4, 3]
    #     ]

    #     output = game_instance.gaming(sample_input)
    #     self.assertEqual(output, [13, 5], str(output))


if __name__ == '__main__':
    unittest.main()
