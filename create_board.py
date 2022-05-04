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

    def populate_diagonals(self, row, col, board):
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

    def populate_rows(self, row, col, board):
        res = []
        for r in range(row):
            if not self.attack_same_kind(r, col, board):
                res.append((r, col))

        for c in range(col):
            if not self.attack_same_kind(row, c, board):
                res.append((row, c))

        return res


class Queen(Piece):
    def access_fields(self, row, col, board) -> list[tuple]:
        """"
        with the first for will be looked up the left part of the two diagonals while with the
        second one will be looked up the right ones
        """
        return [*self.populate_rows(row, col, board), *self.populate_diagonals(row, col, board)]


class Pawn(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.start_pos = True

    def access_fields(self, row, col, board) -> list[tuple]:
        res = []
        row_adder = row - 2 if self.is_white else row + 2
        if self.start_pos and not isinstance(board[row_adder][col], Piece):
            res.append((row_adder, col))
        move_forward_row = row - 1 if self.is_white else row + 1
        if not isinstance(board[move_forward_row][col], Piece):
            res.append((move_forward_row, col))

        if row - 1 in range(DIMENSION) and col - 1 in range(DIMENSION):
            res.append((row - 1, col - 1))

        if row + 1 in range(DIMENSION) and col + 1 in range(DIMENSION):
            res.append((row - 1, col + 1))
        return res


class Bishop(Piece):
    def access_fields(self, row, col, board) -> list[tuple]:
        return self.populate_diagonals(row, col, board)


class Rock(Piece):
    def access_fields(self, row, col, board) -> list[tuple]:
        return self.populate_rows(row, col, board)
