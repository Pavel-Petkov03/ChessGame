from create_board import Rock, Horse, Bishop, Queen, King, Pawn
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
    @staticmethod
    def load_images():
        pieces = ["bb", "bh", "bk", "bq", "br", "bp", "wr", "wb", "wh", "wk", "wq", "wp"]
        for piece in pieces:
            if piece != empty_pos:
                IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

    def setup(self, screen, gamestate: list[list]):
        color_tuple = (p.Color("white"), p.Color("gray"))
        for row in range(DIMENSION):
            self.rect_list.append([])
            for col in range(DIMENSION):
                color_index = (row + col) % 2
                color = color_tuple[color_index]
                rect = p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                self.rect_list[row].append(rect)
                piece = gamestate[row][col]
                p.draw.rect(screen, color, rect)
                if piece != empty_pos:
                    image = IMAGES[piece.take_picture_name()]
                    screen.blit(image, rect)
                    p.display.update()


    @staticmethod
    def create_rect(row, col, color, screen):
        rect = p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, rect, 1)

    def main(self):
        p.init()
        screen = p.display.set_mode((WIDTH, HEIGHT))
        screen.fill(p.Color("black"))
        game_state = GameState().board
        self.load_images()
        self.setup(screen, game_state)
        available_fields = None
        running = True
        while running:
            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
                elif event.type == p.MOUSEBUTTONDOWN:
                    x, y = p.mouse.get_pos()
                    x = x // SQ_SIZE
                    y = y // SQ_SIZE
                    piece = game_state[y][x]
                    if available_fields:
                        if self.find_location(available_fields, row=y, col=x):
                            pass
                    else:
                        if piece is not empty_pos:
                            available_fields = piece.access_fields(y, x, game_state)
                            self.fill_available_cells(available_fields, screen)

            p.display.flip()
            p.display.update()

    def fill_available_cells(self, array, screen):
        green = p.Color("green")
        for (r, c) in array:
            self.create_rect(r, c, green, screen)

    def find_location(self,  array, row, col):
        for location in array:
            r, c = location
            if r == row and c == col:
                return True
        return False

    def move_piece(self):
        pass


if __name__ == "__main__":
    game = Game()
    game.main()
