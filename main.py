# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import pygame
pygame.init()

# Pygame vars
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN
)

# Set up the drawing window
# Define constants for the screen width and height
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SCREEN_RED = 0
SCREEN_GREEN = 0
SCREEN_BLUE = 0
FONT_COLOR = (255, 0, 0)

white = (255,255,255)
black = (0,0,0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Title
pygame.display.set_caption("Tic-Tac-Toe")

# Images
x_image = pygame.image.load('img/X.jpeg')
o_image = pygame.image.load('img/o_image.png')


def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, 300), (900, 300))
        pygame.draw.line(screen, (255, 255, 255), (0, 600), (900, 600))
        pygame.draw.line(screen, (255, 255, 255), (300, 0), (300, 900))
        pygame.draw.line(screen, (255, 255, 255), (600, 0), (600, 900))


class Board:

    def __init__(self):

        self.rows = 3
        self.cols = 3
        self.board = [["E" for i in range(self.cols)] for j in range(self.rows)]

    def print_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.board[j][i], end=" ")
            print("\n")

    def make_move(self, row, col, value):
        self.board[row][col] = value

    def check_rows(self, board_in):
        # Three in row
        for row in board_in:
            if len(set(row)) == 1 and row[0] != "E":
                # Return the winner
                return row[0]

    def check_diags(self):
        list_arr_right = []
        for i in range(self.rows):
            list_arr_right.append(self.board[i][i])
        if len(set(list_arr_right)) == 1 and list_arr_right[0] != "E":
            return list_arr_right[0]

        list_arr_left = []
        for j in range(self.rows):
            list_arr_left.append(np.rot90(self.board)[j][j])
        if len(set(list_arr_left)) == 1 and list_arr_left[0] != "E":
            return list_arr_left[0]

    def check_winner(self):
        if self.check_rows(self.board):
            return self.check_rows(self.board)
        if self.check_rows(np.transpose(self.board)):
            return self.check_rows(np.transpose(self.board))
        if self.check_diags():
            return self.check_diags()


class Tile:
    def __init__(self, x, y):
        self.clicked = False
        self.value = ""
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 295, 295)
        self.img = ""

    def set_value(self, value):
        self.value = value

    def get_coords(self):
        return self.x, self.y

    def draw(self, player=""):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

                # Logic to determine what the image the button should be
                if player == "X":
                    self.img = x_image
                    print("x_img")
                elif player == "O":
                    self.img = o_image
                    print("o_img")

                screen.blit(self.img, self.rect)

                print("CLICKED")

        # if pygame.mouse.get_pressed()[0] == 0:
        #     self.clicked = False

        # draw button
        # screen.blit(self.image, self.rect)
        if self.clicked == False:
            pygame.draw.rect(screen, (0, 0, 255), self.rect)
        # else:
        #     print("writing image")
        #     self.img = img
        #     # pygame.Surface.blit(x_image, screen, self.rect)
        #     screen.blit(self.img, self.rect)

        return action
class Pane(object):
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 25)
        pygame.display.set_caption('Box Test')
        self.screen = pygame.display.set_mode((600,400), 0, 32)
        self.screen.fill((white))
        pygame.display.update()


    def addRect(self):
        self.rect = pygame.draw.rect(self.screen, (black), (175, 75, 200, 100), 2)
        pygame.display.update()

    def addText(self):
        self.screen.blit(self.font.render('Hello!', True, (255,0,0)), (200, 100))
        pygame.display.update()


# All of the clickable squares for the game
top_left_tile = Tile(0, 0)
top_middle_tile = Tile(300, 0)
top_right_tile = Tile(600, 0)

mid_left_tile = Tile(0, 300)
mid_middle_tile = Tile(300, 300)
mid_right_tile = Tile(600, 300)

bottom_left_tile = Tile(0, 600)
bottom_middle_tile = Tile(300, 600)
bottom_right_tile = Tile(600, 600)

tiles = []
tiles.append(top_left_tile)
tiles.append(top_middle_tile)
tiles.append(top_right_tile)

tiles.append(mid_left_tile)
tiles.append(mid_middle_tile)
tiles.append(mid_right_tile)

tiles.append(bottom_left_tile)
tiles.append(bottom_middle_tile)
tiles.append(bottom_right_tile)


# Starting player is X.  This changes
current_player = "X"

# End screen after game is completed
game_ended = False

running = True
# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
board = Board()

while running:
    # board.print_board()
    # move = input("Make a move in form x_coord,y_coord,value: ")
    # board.make_move(int(move[0]), int(move[1]), move[2])
    # if board.check_winner():
    #     print("Player " + str(board.check_winner()) + " has won the game!")
    #     board.print_board()
    #     break

    # First element is X position
    # Second element is y position
    # Third element is width
    # Fourth element is height
    # area = pygame.draw.rect(screen,(0,0,255),(0,0,300,300))
    # area = pygame.Rect(0, 0, 300, 300)

    if game_ended:
        # screen.fill((white))
        font = pygame.font.SysFont('Arial', 25)
        screen.blit(font.render('Player ' + str(current_player) + ' has won the game', True, (255,0,0)), (300, 300))

    else:

        draw_grid()
        for tile in tiles:
            if tile.draw(current_player):

                x, y = tile.get_coords()
                board.make_move(x // 300, y // 300, current_player)
                board.print_board()
                if board.check_winner():
                    print("Player " + str(board.check_winner()) + " has won the game!")
                    # board.print_board()
                    # running = False
                    # TODO: Write a final screen
                    game_ended = True
                    break


                # Update the player
                if current_player == "O":
                    current_player = "X"
                elif current_player == "X":
                    current_player = "O"
                # Grab the coordinates
                # print(x, y)
                # print(x // 300, y // 300)




    for event in pygame.event.get():
        if event.type == QUIT:
            running = False


    pygame.display.update()

pygame.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
