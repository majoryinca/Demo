import unittest

BASE_POINTS = 1
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
        for chunk_id in range(len(self.seq)):
            self.run_single_turn(chunk_id)
            if self.current_round > self.max_round:
                if self.calc_winner():
                    break
                else:
                    tie_broken, to_the_end = self.run_tiebreaker()
                    break
        print(self.total_scores)
        return self.total_scores

    '''If score no points, return False and this turn ends. Otherwise return True'''

    def run_single_turn(self, chunk_id):
        score_flg = self.calc_single_score(
            self.seq[chunk_id])
        if self.get_temp_mini_bonus() > 0 and score_flg:
            self.set_mini_bonus()
            self.set_total_score(MINI_BONUS_POINTS)
        if self.get_temp_bonus() > 0 and score_flg:
            self.set_bonus()
            self.set_total_score(BONUS_POINTS)
        self.clear_temp_bonus()

        # set temporary bonus score
        self.set_single_temp_bonus_score(
            self.seq[chunk_id])

        if not score_flg:
            # current player turn ends and  it is another player turn
            self.current_player = (self.current_player + 1) % self.players

            # current turn ends while it is the last player. increment the current round
            if self.current_player % self.players == 0:

                # print(f'The current round {self.current_round}:')
                # for i in range(0, self.players):
                #     print(f'player index {i}: total score: {self.total_scores[i]}, mini bonus: {self.mini_bonuses[i]}, bonus: {self.bonuses[i]}')
                # print("\n")

                self.current_round += 1

    def run_tiebreaker(self):
        tie_broken = False
        to_the_end = False
        addition_seq = self.seq[self.players * self.max_round:]
        start_point = 0
        while not tie_broken and not to_the_end:
            single_turn_chunks = [addition_seq[j:(
                j + self.players)] for j in range(start_point, len(addition_seq), self.players)]
            # one more round
            for chunk_id in range(len(single_turn_chunks)):
                self.run_single_turn(self.players * self.max_round + chunk_id)
            if self.calc_winner():
                tie_broken = True
            else:
                start_point += self.players
                if start_point >= len(addition_seq):
                    to_the_end = True
        return tie_broken, to_the_end

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

    def calc_single_score(self, chunk):
        base_score_flg = False
        temp_bonus_flg = self.check_single_temp_bonus_score(
            chunk)
        if not temp_bonus_flg:
            base_points = self.calc_basepoint(chunk)
            if base_points > 0:
                self.total_scores[self.current_player] += base_points
                base_score_flg = True

        return base_score_flg or temp_bonus_flg

    '''implement the * of a kind Turn Scoring Rules'''

    def check_single_temp_bonus_score(self, chunk):
        temp_bonus_flg = False
        if self.calc_bonus(chunk):
            temp_bonus_flg = True
        if self.calc_mini_bonus(chunk):
            temp_bonus_flg = True
        return temp_bonus_flg

    def set_single_temp_bonus_score(self, chunk):
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
        same_num_flg = True
        for i in range(1, len(chunk)):
            if chunk[i] != chunk[0]:
                same_num_flg = False
                break
        if same_num_flg:
            '''bonus rule'''
            if chunk[0] == self.current_round:
                return True
        return False

    def calc_mini_bonus(self, chunk):
        same_num_flg = True
        for i in range(1, len(chunk)):
            if chunk[i] != chunk[0]:
                same_num_flg = False
                break
        if same_num_flg:
            '''mini bonus rule'''
            if chunk[0] != self.current_round:
                return True
        return False

# Unit test


class TestGame(unittest.TestCase):

    def test_original_sample(self):
        game_instance = RollDice()
        sample_input = [
            [1, 1, 3], [4, 2, 1], [6, 6, 2],
            [2, 1, 6], [5, 4, 1], [3, 3, 3], [3, 4, 5],

            [4, 5, 2], [2, 2, 2], [4, 4, 4], [6, 3, 5],
            [4, 1, 3]
        ]

        output = game_instance.gaming(sample_input)
        self.assertEqual(output, [15, 2], str(output))

    def test_tiebreaker_sample(self):
        game_instance = RollDice(1)
        sample_input = [
            [2, 2, 3], [2, 2, 3], [2, 1, 1]
        ]

        output = game_instance.gaming(sample_input)
        self.assertEqual(output, [1, 0], str(output))

    def test_over_rounds_sample(self):
        game_instance = RollDice(8)
        sample_input = [
            [1, 1, 3], [4, 2, 1], [6, 6, 2],
            [2, 1, 6], [5, 4, 1], [3, 3, 3], [3, 4, 5],

            [4, 5, 2], [2, 2, 2], [4, 4, 4], [6, 3, 5],
            [4, 1, 3]
        ]

        output = game_instance.gaming(sample_input)
        self.assertEqual(output, [15, 2], str(output))

    def test_less_dice_sample(self):
        game_instance = RollDice(8)
        sample_input = [
            [1, 1], [4, 1], [6,  2],
            [2,  6], [5,  1], [3, 3], [3, 5],

            [4, 2], [2, 2], [4, 4], [6, 5],
            [4, 3]
        ]

        output = game_instance.gaming(sample_input)
        self.assertEqual(output, [13, 5], str(output))


if __name__ == '__main__':
    unittest.main()
