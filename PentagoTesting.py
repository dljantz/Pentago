import unittest
from Pentago import *


# Completed tests:
# 5 in a row vertically -- done
# 5 in a row horizontally -- done
# 5 in a row diagonally -- done
# print_board() -- done
# string_coord_to_tuple()
# is_move_valid()
# update_board()
# update_sub_board()
# SubBoard class update() method
# SubBoard class rotate() method
# update_main_board_from_sub_board()
# make_move()


class MyTestCase(unittest.TestCase):
    def test_string_coord_to_tuple(self):
        self.assertTupleEqual(string_coord_to_tuple('b3'), (1, 3))  # add assertion here

    def test_is_move_valid(self):
        game = Pentago()
        self.assertTrue(game.is_move_valid((0, 0)))

    def test_update_board(self):
        game = Pentago()
        game.update_board((3, 3))
        game.print_board()

        comparison_board = [[None for _ in range(6)] for _ in range(6)]
        comparison_board[3][3] = 'black'

        self.assertListEqual(comparison_board, game.get_board())

    def test_update_sub_board(self):
        game = Pentago()
        self.assertEqual(game.update_sub_board((1, 1)), 'quadrant 1')
        self.assertEqual(game.update_sub_board((1, 4)), 'quadrant 2')
        self.assertEqual(game.update_sub_board((4, 1)), 'quadrant 3')
        self.assertEqual(game.update_sub_board((4, 4)), 'quadrant 4')

    def test_update(self):
        """ tests the update method for the SubBoard class"""
        game = Pentago()
        sub_board = game.get_sub_board(1)
        sub_board.update((4, 5), 'black')
        self.assertEqual(sub_board.get_array()[1][2], 'black')
        sub_board.update((0, 5), 'black')
        self.assertEqual(sub_board.get_array()[0][2], 'black')
        sub_board.update((4, 2), 'black')
        self.assertEqual(sub_board.get_array()[1][2], 'black')
        sub_board.update((1, 1), 'black')
        self.assertEqual(sub_board.get_array()[1][1], 'black')
        # print_board(sub_board.get_array())

    def test_rotate(self):
        game = Pentago()
        sub_board = game.get_sub_board(1)
        sub_board.update((0, 0), 1)
        sub_board.update((0, 1), 2)
        sub_board.update((0, 2), 3)
        sub_board.update((1, 0), 4)
        sub_board.update((1, 1), 5)
        sub_board.update((1, 2), 6)
        sub_board.update((2, 0), 7)
        sub_board.update((2, 1), 8)
        sub_board.update((2, 2), 9)
        sub_board.print_board()
        sub_board.rotate('A')
        sub_board.print_board()

        # print_board(sub_board.get_array())
        comparison = [[3, 6, 9], [2, 5, 8], [1, 4, 7]]
        self.assertListEqual(sub_board.get_array(), comparison)

        sub_board.rotate('C')
        sub_board.print_board()
        comparison = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertListEqual(sub_board.get_array(), comparison)

    def test_update_main_board_from_sub_board(self):
        game = Pentago()

        game.update_sub_board((5, 5))
        game.update_sub_board((0, 0))
        game.update_sub_board((5, 0))
        game.update_sub_board((0, 5))

        game.update_main_board_from_sub_board(1)
        game.update_main_board_from_sub_board(2)
        game.update_main_board_from_sub_board(3)
        game.update_main_board_from_sub_board(4)

        game.print_board()
        comparison = [['black', None, None, None, None, 'black'],
                      [None, None, None, None, None, None],
                      [None, None, None, None, None, None],
                      [None, None, None, None, None, None],
                      [None, None, None, None, None, None],
                      ['black', None, None, None, None, 'black']]

        self.assertListEqual(comparison, game.get_board())

    def test_get_horizontal_winner(self):
        game = Pentago()

        game.update_board((0, 0))
        game.update_board((1, 1))

        self.assertIsNone(game.get_horizontal_winner())

        game.update_board((0, 1))
        game.update_board((0, 2))

        self.assertIsNone(game.get_horizontal_winner())

        game.update_board((0, 3))
        game.update_board((0, 4))

        self.assertEqual(game.get_horizontal_winner(), 'black')

        game.print_board()

        game.update_turn_number()
        game.update_board((4, 0))
        game.update_board((4, 1))
        game.update_board((4, 2))
        game.update_board((4, 3))
        game.update_board((4, 4))
        game.update_board((4, 5))

        game.print_board()

        self.assertEqual(game.get_horizontal_winner(), 'both')

    def test_get_vertical_winner(self):
        game = Pentago()

        game.update_board((0, 0))
        game.update_board((1, 1))

        self.assertIsNone(game.get_vertical_winner())

        game.update_board((1, 0))
        game.update_board((2, 0))

        self.assertIsNone(game.get_vertical_winner())

        game.update_board((3, 0))
        game.update_board((4, 0))

        self.assertEqual(game.get_vertical_winner(), 'black')

        game.print_board()

        game.update_turn_number()
        game.update_board((0, 4))
        game.update_board((1, 4))
        game.update_board((2, 4))
        game.update_board((3, 4))
        game.update_board((4, 4))

        game.print_board()

        self.assertEqual(game.get_vertical_winner(), 'both')

    def test_get_diagonal_winner(self):
        game = Pentago()

        game.update_board((0, 0))
        game.update_board((1, 1))

        self.assertIsNone(game.get_diagonal_winner())

        game.update_board((2, 2))
        game.update_board((3, 3))
        game.update_board((4, 4))

        self.assertEqual(game.get_diagonal_winner(), 'black')

        game.update_turn_number()

        game.update_board((1, 0))
        game.update_board((2, 1))
        game.update_board((3, 2))
        game.update_board((4, 3))

        self.assertEqual(game.get_diagonal_winner(), 'black')

        game.update_board((5, 4))

        self.assertEqual(game.get_diagonal_winner(), 'both')

        game.print_board()

        game2 = Pentago()

        game2.update_board((5, 0))
        game2.update_board((4, 1))
        game2.update_board((3, 2))
        game2.update_board((2, 3))

        self.assertIsNone(game2.get_diagonal_winner())

        game2.update_board((1, 4))

        game.print_board()

        self.assertEqual(game2.get_diagonal_winner(), 'black')

        game2.update_turn_number()

        game2.update_board((5, 0))
        game2.update_board((4, 1))
        game2.update_board((3, 2))
        game2.update_board((2, 3))
        game2.update_board((1, 4))

        self.assertEqual(game2.get_diagonal_winner(), 'white')

        game.print_board()

    def test_make_move(self):
        game = Pentago()

        # continue game when no ties or wins
        # perform piece placement
        # perform rotations, keep track of board state
        # perform alternating moves... track turn order
        print(game.make_move('black', 'a0', 2, 'A'))
        game.print_board()
        print(game.make_move('white', 'c5', 1, 'A'))
        game.print_board()
        print(game.make_move('black', 'e4', 3, 'A'))
        game.print_board()
        print(game.make_move('white', 'd2', 4, 'A'))
        game.print_board()

        comparison = [[None, None, None, None, None, None],
                      [None, None, None, None, None, None],
                      ['black', None, None, None, None, 'white'],
                      [None, None, 'white', None, None, None],
                      [None, None, None, None, 'black', None],
                      [None, None, None, None, None, None]]

        self.assertListEqual(comparison, game.get_board())

        # disallow playing pieces when wrong color chosen
        self.assertEqual("not this player's turn", game.make_move('white', 'f5', 4, 'C'))

        # disallow playing in occupied squares
        self.assertEqual("position is not empty", game.make_move('black', 'e4', 4, 'C'))

        # end game before rotation if one player wins
        print(game.make_move('black', 'a0', 4, 'A'))
        game.print_board()
        print(game.make_move('white', 'b0', 4, 'A'))
        game.print_board()
        print(game.make_move('black', 'a1', 4, 'A'))
        game.print_board()
        print(game.make_move('white', 'b1', 4, 'A'))
        game.print_board()
        print(game.make_move('black', 'a2', 4, 'A'))
        game.print_board()
        print(game.make_move('white', 'b2', 4, 'A'))
        game.print_board()
        print(game.make_move('black', 'a3', 4, 'A'))
        game.print_board()
        print(game.make_move('white', 'b3', 4, 'A'))
        game.print_board()
        state = game.make_move('black', 'a4', 1, 'A')
        game.print_board()
        print("the above board should have resulted in black winning prior to rotation")

        self.assertEqual(state, 'game is finished')
        self.assertEqual(game.get_game_state(), 'BLACK_WON')

        # prevent additional moves if game is already over
        game.make_move('white', 'b4', 4, 'A')
        game.print_board()

        # end game in tie if board is filled (after rotation)
        # pretty sure this works... I'm moving on

        # end game in tie if both players get 5 in a row
        game2 = Pentago()
        print(game2.make_move('black', 'a0', 4, 'A'))
        print(game2.make_move('white', 'b0', 4, 'A'))
        print(game2.make_move('black', 'a1', 4, 'A'))
        print(game2.make_move('white', 'b1', 4, 'A'))
        print(game2.make_move('black', 'a2', 4, 'A'))
        print(game2.make_move('white', 'b2', 4, 'A'))
        print(game2.make_move('black', 'a5', 4, 'A'))
        print(game2.make_move('white', 'a4', 4, 'A'))
        print(game2.make_move('black', 'b5', 4, 'A'))
        print(game2.make_move('white', 'b4', 4, 'A'))
        game2.print_board()
        print(game2.make_move('black', 'd5', 4, 'A'))
        state = game2.make_move('white', 'e4', 2, 'A')
        self.assertEqual('game is finished', state)

        # I win if only I have 5 in a row after rotation
        game3 = Pentago()
        print(game3.make_move('black', 'f0', 4, 'A'))
        print(game3.make_move('white', 'b0', 4, 'A'))
        print(game3.make_move('black', 'a1', 4, 'A'))
        print(game3.make_move('white', 'b1', 4, 'A'))
        print(game3.make_move('black', 'a2', 4, 'A'))
        print(game3.make_move('white', 'b2', 4, 'A'))
        print(game3.make_move('black', 'a5', 4, 'A'))
        print(game3.make_move('white', 'a4', 4, 'A'))
        print(game3.make_move('black', 'b5', 4, 'A'))
        print(game3.make_move('white', 'b4', 4, 'A'))
        print(game3.make_move('black', 'd5', 4, 'A'))
        state = game3.make_move('white', 'e4', 2, 'A')
        game3.print_board()
        self.assertEqual('game is finished', state)

        # opponent wins if I play and then rotate them into a win
        game4 = Pentago()
        print(game4.make_move('black', 'a0', 4, 'A'))
        print(game4.make_move('white', 'f0', 4, 'A'))
        print(game4.make_move('black', 'a1', 4, 'A'))
        print(game4.make_move('white', 'b1', 4, 'A'))
        print(game4.make_move('black', 'a2', 4, 'A'))
        print(game4.make_move('white', 'b2', 4, 'A'))
        print(game4.make_move('black', 'a5', 4, 'A'))
        print(game4.make_move('white', 'a4', 4, 'A'))
        print(game4.make_move('black', 'b5', 4, 'A'))
        print(game4.make_move('white', 'b4', 4, 'A'))
        print(game4.make_move('black', 'd5', 4, 'A'))
        state = game4.make_move('white', 'e4', 2, 'A')
        game4.print_board()
        self.assertEqual('game is finished', state)

    def test_vertical_win(self):
        # This test is designed to help me pass the final autograder test
        game = Pentago()
        game.make_move('black', 'a0', 3, 'C')
        game.make_move('white', 'a3', 3, 'C')
        game.make_move('black', 'b1', 3, 'C')
        game.make_move('white', 'b3', 3, 'C')
        game.make_move('black', 'c2', 3, 'C')
        game.make_move('white', 'c3', 3, 'C')
        game.make_move('black', 'd2', 3, 'C')
        game.make_move('white', 'd3', 3, 'C')
        game.make_move('black', 'e4', 3, 'C')
        game.make_move('white', 'e3', 4, 'A')
        game.print_board()
        self.assertEqual(game.get_game_state(), 'WHITE_WON')



if __name__ == '__main__':
    unittest.main()
