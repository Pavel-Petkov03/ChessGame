from create_board import Rock, Horse, Bishop, Queen, King, Pawn, Piece
import pygame as p

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 15
IMAGES = {}
empty_pos = "_"


class GameState:
    def __init__(self, white_king, dark_king):
        self.board = [
            [
                Rock(is_white=False),
                Horse(is_white=False),
                Bishop(is_white=False),
                Queen(is_white=False),
                dark_king,
                Bishop(is_white=False),
                Horse(is_white=False),
                Rock(is_white=False)
            ],
            [Pawn(is_white=False) for _ in range(8)],
            *[[empty_pos for _ in range(8)] for _ in range(4)],
            [Pawn(is_white=True) for _ in range(8)],
            [
                Rock(is_white=True),
                Horse(is_white=True),
                Bishop(is_white=True),
                Queen(is_white=True),
                white_king,
                Bishop(is_white=True),
                Horse(is_white=True),
                Rock(is_white=True)
            ]
        ]


class Game:
    def __init__(self):
        self.is_white = True
        self.white_king = King(is_white=True)
        self.black_king = King(is_white=False)
        self.board = GameState(self.white_king, self.black_king).board
        self.king_pos = {
            self.white_king: [7, 4],
            self.black_king: [0, 4]
        }
        self.global_available_fields = []
        self.available_fields = []
        self.screen = p.display.set_mode((WIDTH, HEIGHT))

    @staticmethod
    def load_images():
        pieces = ["bb", "bh", "bk", "bq", "br", "bp", "wr", "wb", "wh", "wk", "wq", "wp"]
        for piece in pieces:
            if piece != empty_pos:
                IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

    def setup(self):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                rect = p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                piece = self.board[row][col]
                p.draw.rect(self.screen, self.get_cell_color(row, col), rect)
                if piece != empty_pos:
                    image = IMAGES[piece.take_picture_name()]
                    self.screen.blit(image, rect)
                    p.display.update()

    @staticmethod
    def get_cell_color(row, col):
        color_tuple = (p.Color("white"), p.Color("gray"))
        color_index = (row + col) % 2
        return color_tuple[color_index]

    def main(self):
        p.init()
        self.screen.fill(p.Color("black"))
        self.load_images()
        self.setup()
        last_clicked = None
        running = True
        while running:
            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
                elif event.type == p.MOUSEBUTTONDOWN:
                    x, y = p.mouse.get_pos()
                    x = x // SQ_SIZE
                    y = y // SQ_SIZE
                    piece = self.board[y][x]

                    if self.available_fields:
                        if self.find_location(row=y, col=x):
                            self.is_white = not self.is_white
                            self.swap(last_clicked, (y, x))
                        self.unmark()
                        self.available_fields.clear()
                    else:
                        if piece is not empty_pos and self.check_if_players_move(y, x):
                            temporary = piece.access_fields(y, x, self.board).copy()
                            self.generate_global_available_fields()
                            self.match_intersection_between_global_and_marked(temporary)
                            print(self.global_available_fields)
                            self.match_marked()
                            last_clicked = (y, x)
            p.display.flip()
            p.display.update()

    def check_if_players_move(self, y, x):
        return self.board[y][x].is_white == self.is_white

    def find_location(self, row, col):
        for location in self.available_fields:
            r, c = location
            if r == row and c == col:
                return True
        return False

    @staticmethod
    def get_index(rect):
        return rect.y // SQ_SIZE, rect.x // SQ_SIZE

    def swap(self, last_clicked: tuple, on_click: tuple):
        lx, ly = last_clicked
        ox, oy = on_click
        l_rect = p.Rect(ly * SQ_SIZE, lx * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        o_rect = p.Rect(oy * SQ_SIZE, ox * SQ_SIZE, SQ_SIZE, SQ_SIZE)

        p.draw.rect(self.screen, self.get_cell_color(lx, ly), l_rect)
        p.draw.rect(self.screen, self.get_cell_color(ox, oy), o_rect)
        self.screen.blit(IMAGES[self.board[lx][ly].take_picture_name()], o_rect)
        self.swap_matrix(self.board, lx, ly, ox, oy)

    @staticmethod
    def swap_matrix(m, fr, fc, sr, sc):
        m[sr][sc] = empty_pos
        m[fr][fc], m[sr][sc] = m[sr][sc], m[fr][fc]

    def match_marked(self):
        for (x, y) in self.available_fields:
            p.draw.rect(self.screen, p.Color("lime"), p.Rect(y * SQ_SIZE, x * SQ_SIZE, SQ_SIZE, SQ_SIZE), 1)

    def unmark(self):
        for (x, y) in self.available_fields:
            r = p.Rect(y * SQ_SIZE, x * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(self.screen, self.get_cell_color(x, y), r)
            if isinstance(self.board[x][y], Piece):
                self.screen.blit(IMAGES[self.board[x][y].take_picture_name()], r)

    def dispatch_king_attack(self):
        current_checked_king = self.get_king()
        return current_checked_king.is_checked(*self.king_pos[current_checked_king], self.board)

    def get_king(self):
        return self.white_king if self.is_white else self.black_king

    def generate_global_available_fields(self):
        global_available = set()
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                piece = self.board[r][c]
                if piece != empty_pos and piece.is_white == self.is_white:
                    piece_available_fields = piece.access_fields(r, c, self.board)
                    for (move_row, move_col) in piece_available_fields:
                        if not piece.attack_same_kind(move_row, move_col, self.board):
                            temporary_field = self.board[move_row][move_col]
                            self.board[r][c], self.board[move_row][move_col] = empty_pos, piece
                            if not self.dispatch_king_attack():
                                global_available.add((move_row, move_col))
                            self.board[r][c], self.board[move_row][move_col] = piece, temporary_field
        self.global_available_fields = list(global_available).copy()

    def match_intersection_between_global_and_marked(self, access_fields):
        res = []
        for index_tup in range(len(access_fields)):
            for global_tup in range(len(self.global_available_fields)):
                if access_fields[index_tup][0] == self.global_available_fields[global_tup][0] and \
                        access_fields[index_tup][1] == self.global_available_fields[global_tup][1]:
                    res.append((access_fields[index_tup]))
        self.available_fields = res.copy()


if __name__ == "__main__":
    game = Game()
    game.main()
