# David Jantz
# Github: David2847
# Date: 8/11/24
# Description: An implementation of the 2 player strategy game Pentago.

def string_coord_to_tuple(string_coord):
    """ Converts string coordinates like 'a1' into tuple form like (0,0) """
    letter = string_coord[0]
    row = ord(letter.lower()) - ord('a')
    col = int(string_coord[1])
    return row, col


class Pentago:
    """
    This is the main / parent class for the game. It contains the board data and
    conducts all the major actions of the game except for sub-board rotation. It has the board
    as the source of ultimate truth about the state of the game, but it also has 4 sub-board
    arrays that are instances of the class SubBoard that are updated from the main board.
    """

    def __init__(self):
        """ Initializes all data members, including empty board, turn counting variable, and 4 sub-boards"""
        self._board = [[None for _ in range(6)] for _ in range(6)]
        self._num_turns_taken = 0
        self._quadrant_1 = SubBoard()
        self._quadrant_2 = SubBoard()
        self._quadrant_3 = SubBoard()
        self._quadrant_4 = SubBoard()

    def print_board(self):
        """
        Displays the current state of the board to the console. This is a function, not a method,
        because it's used by both the Pentago class and the SubBoard class.
        """
        for row in self._board:
            for slot in row:
                if slot is None:
                    print('-', end='\t')
                elif slot == 'white':
                    print('W', end='\t')
                elif slot == 'black':
                    print('B', end='\t')
                else:
                    print(slot, end='\t')
            print()
        print()

    def get_game_state(self):
        """ Returns 'UNFINISHED', 'WHITE_WON', 'BLACK_WON' or 'DRAW'. """

        # takes on a value of 'white', 'black', 'both', or None.
        winner = self.get_winner()

        if winner == 'white':
            return 'WHITE_WON'
        elif winner == 'black':
            return 'BLACK_WON'
        elif winner == 'both' or self.is_board_full():
            return 'DRAW'

        return 'UNFINISHED'

    def get_board(self):
        """ returns board array """
        return self._board

    def get_sub_board(self, sub_board):
        """ returns a SubBoard object
        :param sub_board: int describing which quadrant to grab
        """
        if sub_board == 1:
            return self._quadrant_1
        elif sub_board == 2:
            return self._quadrant_2
        elif sub_board == 3:
            return self._quadrant_3
        elif sub_board == 4:
            return self._quadrant_4

    def is_board_full(self):
        """ returns True or False to indicate whether the board is already full """
        return self._num_turns_taken > 35

    def make_move(self, color, position, sub_board, rotation):
        """
        Place the marble onto the board, rotates the sub-board (if the player hasn't won after placing the marble),
        updates the board and game state (from unfinished to indicate who wins, if necessary), updates whose turn it is.

        :param color: a string that represent the color of the marble. Is either ‘white’ or ‘black’
        :param position: a string that represent the position the marble will be put onto the board. ‘a0’, 'b1', etc.
        :param sub_board:  an integer of either 1, 2, 3 or 4 that represents the sub-board the player choose to rotate
        :param rotation: a string that represent the direction the sub-board will rotate, either ‘C’ (clockwise) or
        ‘A’ (anti-clockwise).
        :return: string: "game is finished", "Not this player's turn", "position is not empty", or True (if move was
        legal and carried out)
        """
        # this runs multiple times throughout this method... here it is preventing further
        #       play after the game is over
        if self.get_game_state() != 'UNFINISHED':
            return 'game is finished'

        if color != self.get_whose_turn():
            return "not this player's turn"

        coords = string_coord_to_tuple(position)

        # check if move is legal
        if not self.is_move_valid(coords):
            return "position is not empty"
        else:
            # update main board and sub-boards
            self.update_board(coords)
            self.update_sub_board(coords)
            self._num_turns_taken += 1

        # check for win prior to rotation
        status = self.get_game_state()
        if status == 'WHITE_WON' or status == 'BLACK_WON':
            # return true on the same move player wins, later calls to this method will return 'game is finished'
            return True

        # perform rotation on sub-board
        self.get_sub_board(sub_board).rotate(rotation)

        # copy data from sub-board back over to main board
        self.update_main_board_from_sub_board(sub_board)

        # post-rotation: check for win / loss / tie (including filled board) and return status
        if self.get_game_state() != 'UNFINISHED':
            return 'game is finished'
        else:
            return True

    def update_turn_number(self):
        """ increments the value of the turn counter by one"""
        self._num_turns_taken += 1

    def get_whose_turn(self):
        """ returns whose turn it currently is -- 'white' or 'black' """
        if self._num_turns_taken % 2 == 0:
            return 'black'
        else:
            return 'white'

    def update_board(self, position):
        """
        This should only be called if it has been determined that the desired move is legal.
        :param position: a tuple describing the (row, col) integers where the value is to be changed
        :return: nothing
        """
        row = position[0]
        col = position[1]
        self._board[row][col] = self.get_whose_turn()

    def is_move_valid(self, position):
        """
        checks to see if a move is valid -- that the desired location exists on the board
        and that the spot is unoccupied.
        :param position: a tuple describing the (row, col) integers where the value is to be changed
        :return: boolean: is it a valid move or not.
        """
        row = position[0]
        col = position[1]
        return self._board[row][col] is None

    def update_sub_board(self, main_board_coords):
        """
        decides which sub-board to update based on the coordinates of the most recent move.
        """
        if main_board_coords[0] < 3:
            if main_board_coords[1] < 3:
                self._quadrant_1.update(main_board_coords, self.get_whose_turn())
                return 'quadrant 1'
            else:
                self._quadrant_2.update(main_board_coords, self.get_whose_turn())
                return 'quadrant 2'
        else:
            if main_board_coords[1] < 3:
                self._quadrant_3.update(main_board_coords, self.get_whose_turn())
                return 'quadrant 3'
            else:
                self._quadrant_4.update(main_board_coords, self.get_whose_turn())
                return 'quadrant 4'

    def update_main_board_from_sub_board(self, sub_board):
        """
        This should be called right after a rotation. The sub-board has just been
        rotated and its values need to be reflected in the main board so there is no
        discrepancy.
        :param sub_board: an integer of 1, 2, 3, or 4 that indicates the sub-board that was
            rotated and now needs to be copied over.
        """
        row_start = 0
        col_start = 0
        if sub_board == 2 or sub_board == 4:
            col_start = 3
        if sub_board == 3 or sub_board == 4:
            row_start = 3

        sub_board = self.get_sub_board(sub_board)

        for row in range(3):
            for col in range(3):
                self._board[row + row_start][col + col_start] = sub_board.get_array()[row][col]

    def get_winner(self):
        """
        Checks for horizontal, diagonal, and vertical wins and returns who the winner
        is: 'white', 'black', 'both', or None.
        """

        horizontal_winner = self.get_horizontal_winner()
        if horizontal_winner is not None:
            return horizontal_winner

        vertical_winner = self.get_vertical_winner()
        if vertical_winner is not None:
            return vertical_winner

        # last one to check, so if it's None just return that anyway
        return self.get_diagonal_winner()

    def get_horizontal_winner(self):
        """ checks for a horizontal win, returns 'white', 'black', 'both', or None to describe if winner is
        white, black, or no one. """

        white_row_length = 0
        black_row_length = 0

        is_white_winner = False
        is_black_winner = False

        for row in self._board:
            for value in row:
                if value == 'white':
                    white_row_length += 1
                    if white_row_length == 5:
                        is_white_winner = True
                elif value == 'black':
                    black_row_length += 1
                    if black_row_length == 5:
                        is_black_winner = True
                else:
                    white_row_length = 0
                    black_row_length = 0
            # reset after each row
            white_row_length = 0
            black_row_length = 0

        if is_white_winner and is_black_winner:
            return 'both'
        elif is_white_winner:
            return 'white'
        elif is_black_winner:
            return 'black'
        else:
            return None

    def get_vertical_winner(self):
        """ checks for a vertical win, returns 'white', 'black', or None to describe if winner is
        white, black, or no one. """

        white_row_length = 0
        black_row_length = 0

        is_white_winner = False
        is_black_winner = False

        for col_num in range(len(self._board[0])):
            for row_num in range(len(self._board)):
                value = self._board[row_num][col_num]
                if value == 'white':
                    white_row_length += 1
                    if white_row_length == 5:
                        is_white_winner = True
                elif value == 'black':
                    black_row_length += 1
                    if black_row_length == 5:
                        is_black_winner = True
                else:
                    white_row_length = 0
                    black_row_length = 0
            # reset after each row
            white_row_length = 0
            black_row_length = 0

        if is_white_winner and is_black_winner:
            return 'both'
        elif is_white_winner:
            return 'white'
        elif is_black_winner:
            return 'black'
        else:
            return None

    def get_diagonal_winner(self):
        """ checks for a diagonal win, returns 'white', 'black', or None to describe if winner is
        white, black, or no one. """

        white_row_length = 0
        black_row_length = 0

        is_white_winner = False
        is_black_winner = False

        # Loop through a small grid in the upper left hand corner. The number 4 appears
        #   because that is one less than the winning row length. This section tests for
        #   diagonal wins that are sloped down to the right.
        for row_num in range(len(self._board) - 4):
            for col_num in range(len(self._board) - 4):
                for i in range(5):
                    value = self._board[row_num + i][col_num + i]
                    if value == 'white':
                        white_row_length += 1
                        if white_row_length == 5:
                            is_white_winner = True
                    elif value == 'black':
                        black_row_length += 1
                        if black_row_length == 5:
                            is_black_winner = True
                    else:
                        white_row_length = 0
                        black_row_length = 0
                # reset after each diagonal that's tested
                white_row_length = 0
                black_row_length = 0

        # Now loop through all the diagonals that are sloping up to the right.
        for row_num in range(4, len(self._board)):
            for col_num in range(len(self._board) - 4):
                for i in range(5):
                    value = self._board[row_num - i][col_num + i]
                    if value == 'white':
                        white_row_length += 1
                        if white_row_length == 5:
                            is_white_winner = True
                    elif value == 'black':
                        black_row_length += 1
                        if black_row_length == 5:
                            is_black_winner = True
                    else:
                        white_row_length = 0
                        black_row_length = 0
                # reset after each diagonal that's tested
                white_row_length = 0
                black_row_length = 0

        if is_white_winner and is_black_winner:
            return 'both'
        elif is_white_winner:
            return 'white'
        elif is_black_winner:
            return 'black'
        else:
            return None


class SubBoard:
    """
    Holds a 3 x 3 2D array of board values. The main 6 x 6 board typically drives the
    data stored here, except when a rotation is performed by SubBoard, in which case the rotated
    array is then used to update the appropriate quadrant of the main board.
    """

    def __init__(self):
        """ Initializes empty 3 x 3 2D array"""
        self._sub_board = [[None for _ in range(3)] for _ in range(3)]

    def print_board(self):
        """
        Displays the current state of the board to the console. This is a function, not a method,
        because it's used by both the Pentago class and the SubBoard class.
        """
        for row in self._sub_board:
            for slot in row:
                if slot is None:
                    print('-', end='\t')
                elif slot == 'white':
                    print('W', end='\t')
                elif slot == 'black':
                    print('B', end='\t')
                else:
                    print(slot, end='\t')
            print()
        print()

    def update(self, main_board_coords, whose_turn):
        """
        updates the sub-board
        :param main_board_coords: The coordinates of the main board
        :param whose_turn: string 'white' or 'black' to place in the sub-board array
        """
        sub_board_coords = list(main_board_coords)

        # modify main board coords to fit within sub-board
        if main_board_coords[0] > 2:
            sub_board_coords[0] -= 3
        if main_board_coords[1] > 2:
            sub_board_coords[1] -= 3

        row = sub_board_coords[0]
        col = sub_board_coords[1]
        self._sub_board[row][col] = whose_turn

    def rotate(self, direction):
        """ rotates the SubBoard. direction is a string 'A' or 'C' for clockwise or anticlockwise"""
        new_sub_board = [[None for _ in range(3)] for _ in range(3)]

        complex_multiplier = 1j
        # Normally, rotating anticlockwise would require i. But the y-axis is flipped so rotation is reversed too.
        if direction == 'A':
            complex_multiplier *= -1

        for row in range(len(self._sub_board)):
            for col in range(len(self._sub_board[0])):
                # shift coordinates over to center on origin and convert into complex number
                complex_coord = (row - 1) * 1j + (col - 1)
                # perform the rotation using complex multiplication
                complex_coord *= complex_multiplier
                # shift back so it's not centered on the origin anymore... no more negative coordinates
                complex_coord += 1 + 1j
                # extract row / col information
                new_row = int(complex_coord.imag)
                new_col = int(complex_coord.real)
                # value to transfer can be None, 'white', or 'black'
                value = self._sub_board[row][col]
                new_sub_board[new_row][new_col] = value

        self._sub_board = new_sub_board

    def get_array(self):
        """ returns the 2d array describing the sub-board"""
        return self._sub_board


def main():
    game = Pentago()
    print(game.make_move('black', 'a2', 1, 'C'))
    print(game.make_move('white', 'a2', 1, 'C'))
    print(game.is_board_full())
    game.print_board()
    print(game.get_game_state())


if __name__ == "__main__":
    main()
