from main import GameState

DIMENSION = 8


class Piece:
    def __init__(self, is_white=None):
        self.is_white = is_white

    def access_fields(self, row, col, board) -> list[tuple]:
        """
        This function will be overriden over every piece
        we need to get current pos in order to display allowed places
        :return: pos_list
        """

    def attack_same_kind(self, row, col, board):
        return isinstance(board[row][col], Piece) and board[row][col].is_white == self.is_white


class Queen(Piece):
    def access_fields(self, row, col, board) -> list[tuple]:
        """"
        with the first for will be looked up the left part of the two diagonals while with the
        second one will be looked up the right ones
        """
        res = []
        for left_wing in range(1, col + 1):
            if row - left_wing in range(DIMENSION) and not self.attack_same_kind(row - left_wing, col - left_wing,
                                                                                 board):
                res.append((row - left_wing, col - left_wing))
            if row + left_wing in range(DIMENSION) and not self.attack_same_kind(row + left_wing, col - left_wing,
                                                                                 board):
                res.append((row + left_wing, col - left_wing))

        for right_wing in range(col + 1, len(board)):
            if row - right_wing in range(DIMENSION) and not self.attack_same_kind(row - right_wing, col + right_wing,
                                                                                  board):
                res.append((row - right_wing, col + right_wing))
            if row + right_wing in range(8) and not self.attack_same_kind(row + right_wing, col + right_wing, board):
                res.append((row + right_wing, col + right_wing))

        return res


class Pawn(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.start_pos = True

    def access_fields(self, row, col, board) -> list[tuple]:
        res = []
        if self.is_white:
            if self.start_pos and not isinstance(board[row][col - 2], Piece):
                res.append((row, col - 2))
                self.start_pos = False
            if not isinstance(board[row][col-1], Piece):
                pass
        else:
            pass
