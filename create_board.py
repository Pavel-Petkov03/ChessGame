DIMENSION = 8


class Piece:
    def __init__(self, is_white=None):
        self.is_white = is_white
        self.is_king = False

    def access_fields(self, row, col, board) -> list[tuple]:
        """
        This function will be overriden over every piece
        we need to get current pos in order to display allowed places
        :return: pos_list
        """

    def check_if_boundary(self, row, col, board, res):
        if isinstance(board[row][col], Piece):
            if self.attack_same_kind(row, col, board):
                return True
            res.append((row, col))
            return True
        return True

    def attack_same_kind(self, row, col, board):
        return isinstance(board[row][col], Piece) and board[row][col].is_white == self.is_white

    def populate_diagonals(self, row, col, board):
        res = []
        row_down_col_up_block = False
        row_down_col_down_block = False
        row_up_col_down_block = False
        row_up_col_up_block = False

        for left_wing in range(1, col + 1):
            if row - left_wing in range(DIMENSION) and not row_down_col_down_block:
                if self.check_if_boundary(row - left_wing, col - left_wing, board, res):
                    row_down_col_down_block = True
                    continue
                res.append((row - left_wing, col - left_wing))

            if row + left_wing in range(DIMENSION) and not row_up_col_down_block:
                if self.check_if_boundary(row + left_wing, col - left_wing, board, res):
                    row_up_col_down_block = True
                    continue
                res.append((row + left_wing, col - left_wing))

        for right_wing in range(col + 1, len(board)):
            if row - right_wing in range(DIMENSION) and not row_down_col_up_block:
                if self.check_if_boundary(row - right_wing, col + right_wing, board, res):
                    row_down_col_up_block = True
                    continue
                res.append((row - right_wing, col + right_wing))
            if row + right_wing in range(8) and not row_up_col_up_block:
                if self.check_if_boundary(row + right_wing, col + right_wing, board, res):
                    row_up_col_up_block = True
                    continue
            res.append((row + right_wing, col + right_wing))

        return res

    def populate_rows(self, row, col, board):

        return [
            *self.plain_search(0, row, row, col, False, board),
            *self.plain_search(row + 1, DIMENSION, row, col, False, board),
            *self.plain_search(0, col, row, col, True, board),
            *self.plain_search(col + 1, DIMENSION, row, col, True, board)
        ]

    def plain_search(self, start, end, row, col, is_col, board):
        res = []
        for index in range(start, end):
            tup = (index, col)if is_col else (row, index)
            if not self.check_if_boundary(tup[0], tup[1], board, res):
                res.append(tup)
            else:
                return res
        return res

    def take_picture_name(self):
        first_letter = "w" if self.is_white else "b"
        second_letter = self.__class__.__name__[0].lower()
        return f"{first_letter}{second_letter}"


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
        res += self.append_only_if_beatable(move_forward_row, col, board)
        return res

    def append_only_if_beatable(self, move_forward_row, col, board):
        res = []
        if col + 1 in range(DIMENSION) and isinstance(board[move_forward_row][col + 1], Piece) and \
                board[move_forward_row][col + 1].is_white is not self.is_white:
            res.append((move_forward_row, col + 1))
        if col - 1 in range(DIMENSION) and isinstance(board[move_forward_row][col - 1], Piece) and \
                board[move_forward_row][col - 1].is_white is not self.is_white:
            res.append((move_forward_row, col - 1))
        return res


class Bishop(Piece):
    def access_fields(self, row, col, board) -> list[tuple]:
        return self.populate_diagonals(row, col, board)


class Rock(Piece):
    def access_fields(self, row, col, board) -> list[tuple]:
        return self.populate_rows(row, col, board)


class Horse(Piece):
    def access_fields(self, row, col, board) -> list[tuple]:
        row_list = [-2, -2, -1, -1, +1, -1, 2, 2]
        col_list = [-1, +1, +2, -2, -2, +2, -1, 1]
        res = []
        for index in range(len(row_list)):
            current_row = row_list[index] + row
            current_col = col_list[index] + col

            if current_col in range(DIMENSION) and current_row in range(DIMENSION) and not self.attack_same_kind(
                    current_row, current_col, board):
                res.append((current_row, current_col))
        return res


class King(Piece):

    def castle(self):
        """
        Make castle with king if possible
        :return:
        """

    def is_checked(self, row, col, board) -> bool:
        move_forward_row = row - 1 if self.is_white else row + 1
        for (r, c) in Pawn(self.is_white).append_only_if_beatable(move_forward_row, col, board):
            if isinstance(board[r][c], Pawn):
                return True
        for (r, c) in self.populate_diagonals(row, col, board):
            if isinstance(board[r][c], Queen) or isinstance(board[r][c], Queen):
                return True

        for (r, c) in self.populate_rows(row, col, board):
            if isinstance(board[r][c], Rock) or isinstance(board[r][c], Queen):
                return True

        for (r, c) in Horse(self.is_white).access_fields(row, col, board):
            if isinstance(board[r][c], Horse):
                return True
        return False
