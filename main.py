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
        self.rect_list = []
        self.board = GameState().board

    @staticmethod
    def load_images():
        pieces = ["bb", "bh", "bk", "bq", "br", "bp", "wr", "wb", "wh", "wk", "wq", "wp"]
        for piece in pieces:
            if piece != empty_pos:
                IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

    def setup(self, screen):

        for row in range(DIMENSION):
            self.rect_list.append([])
            for col in range(DIMENSION):
                rect = p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                self.rect_list[row].append(rect)
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
                            self.swap(last_clicked, self.rect_list[y][x], screen)
                            white_move = not white_move
                            available_fields.clear()
                        else:
                            available_fields.clear()

                    else:
                        if piece is not empty_pos and self.check_if_players_move(y, x, white_move):
                            print(y, x)
                            available_fields = piece.access_fields(y, x, self.board)
                            last_clicked = self.rect_list[y][x]
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

    def swap(self, first_rect: p.Rect, second_rect: p.Rect, screen):
        first_x = first_rect.top
        first_y = first_rect.left
        first_rect.top = second_rect.top
        first_rect.left = second_rect.left
        second_rect.top = first_x
        second_rect.left = first_y
        self.swap_pieces(first_rect, second_rect)
        for rect in [first_rect, second_rect]:
            row, col = self.get_index(rect)
            if self.board[row][col] != empty_pos:
                screen.blit(IMAGES[self.board[row][col].take_picture_name()], rect)
            else:
                p.draw.rect(screen, self.get_cell_color(row, col), rect)

    @staticmethod
    def get_index(rect):
        return rect.y // SQ_SIZE, rect.x // SQ_SIZE

    def swap_pieces(self, first_rect, second_rect):
        (first_row, first_col) = self.get_index(first_rect)
        (second_row, second_col) = self.get_index(second_rect)
        self.board[first_row][first_col], self.board[second_row][second_col] = self.board[second_row][second_col], \
                                                                               self.board[first_row][first_col]
        self.rect_list[first_row][first_col], self.rect_list[second_row][second_col] = self.rect_list[second_row][
                                                                                           second_col], \
                                                                                       self.rect_list[first_row][
                                                                                           first_col]

    @staticmethod
    def swap_matrix(m, fr, fc, sr, sc):
        m[fr][fc], m[sr][sc] = m[sc][sr], m[fr][fc]


if __name__ == "__main__":
    game = Game()
    game.main()
