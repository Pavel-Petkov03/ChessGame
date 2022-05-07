from create_board import Rock, Horse, Bishop, Queen, King, Pawn, Piece
import pygame as p

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 15
IMAGES = {}
empty_pos = "_"


class GameState:
    def __init__(self):
        self.board = [
            [
                Rock(is_white=False),
                Horse(is_white=False),
                Bishop(is_white=False),
                Queen(is_white=False),
                King(is_white=False),
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
                King(is_white=True),
                Bishop(is_white=True),
                Horse(is_white=True),
                Rock(is_white=True)
            ]
        ]


class Game:

    def __init__(self):
        self.board = GameState().board

    @staticmethod
    def load_images():
        pieces = ["bb", "bh", "bk", "bq", "br", "bp", "wr", "wb", "wh", "wk", "wq", "wp"]
        for piece in pieces:
            if piece != empty_pos:
                IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

    def setup(self, screen):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                rect = p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                piece = self.board[row][col]
                p.draw.rect(screen, self.get_cell_color(row, col), rect)
                if piece != empty_pos:
                    image = IMAGES[piece.take_picture_name()]
                    screen.blit(image, rect)
                    p.display.update()

    @staticmethod
    def get_cell_color(row, col):
        color_tuple = (p.Color("white"), p.Color("gray"))
        color_index = (row + col) % 2
        return color_tuple[color_index]

    def main(self):
        p.init()
        screen = p.display.set_mode((WIDTH, HEIGHT))
        screen.fill(p.Color("black"))
        white_move = True
        self.load_images()
        self.setup(screen)
        available_fields = []
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

                    if available_fields:
                        if self.find_location(available_fields, row=y, col=x):
                            white_move = not white_move
                            self.swap(last_clicked, (y, x), screen)
                        self.unmark(available_fields, screen)
                        available_fields.clear()



                    else:
                        if piece is not empty_pos and self.check_if_players_move(y, x, white_move):
                            available_fields = piece.access_fields(y, x, self.board)
                            self.match_marked(available_fields, screen)
                            print(available_fields)
                            last_clicked = (y, x)
            p.display.flip()
            p.display.update()

    def check_if_players_move(self, y, x, white_move):
        return self.board[y][x].is_white == white_move

    @staticmethod
    def find_location(array, row, col):
        for location in array:
            r, c = location
            if r == row and c == col:
                return True
        return False

    @staticmethod
    def get_index(rect):
        return rect.y // SQ_SIZE, rect.x // SQ_SIZE

    def swap(self, last_clicked: tuple, on_click: tuple, screen):
        lx, ly = last_clicked
        ox, oy = on_click
        l_rect = p.Rect(ly * SQ_SIZE, lx * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        o_rect = p.Rect(oy * SQ_SIZE, ox * SQ_SIZE, SQ_SIZE, SQ_SIZE)

        p.draw.rect(screen, self.get_cell_color(lx, ly), l_rect)
        p.draw.rect(screen, self.get_cell_color(ox, oy), o_rect)
        screen.blit(IMAGES[self.board[lx][ly].take_picture_name()], o_rect)
        self.swap_matrix(self.board, lx, ly, ox, oy)

    @staticmethod
    def swap_matrix(m, fr, fc, sr, sc):
        m[sr][sc] = empty_pos
        m[fr][fc], m[sr][sc] = m[sr][sc], m[fr][fc]

    @staticmethod
    def match_marked(ar, screen):
        for (x, y) in ar:
            p.draw.rect(screen, p.Color("lime"), p.Rect(y * SQ_SIZE, x * SQ_SIZE, SQ_SIZE, SQ_SIZE), 1)

    def unmark(self, ar, screen):
        for (x, y) in ar:
            r = p.Rect(y * SQ_SIZE, x * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, self.get_cell_color(x, y), r)
            if isinstance(self.board[x][y], Piece):
                screen.blit(IMAGES[self.board[x][y].take_picture_name()], r)


if __name__ == "__main__":
    game = Game()
    game.main()
