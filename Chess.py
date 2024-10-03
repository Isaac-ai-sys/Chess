import pyglet # type: ignore
import time
import sys
import ctypes
import os


from PIL import Image # type: ignore
from time import sleep
from pyglet import * # type: ignore
from pyglet.gl import * # type: ignore

from pyglet.gl import GL_QUADS

class Button:
    def __init__(self, x, y, width, height, color, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.default_color = color
        self.pressed_color = (255, 255, 0)  # Yellow color for pressed state
        self.message = text
        self.text = pyglet.text.Label(text,
                                      font_name='Arial',
                                      font_size=14,
                                      x=x + width // 2,
                                      y=y + height // 2,
                                      anchor_x='center',
                                      anchor_y='center')
        self.text.color = (255, 255, 255, 255)  # Default text color (white)
        self.pressed = False
        self.enlarged = False

    def is_mouse_over(self, x, y):
        if(self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height):
            self.enlarged = True
            return True
        else:
            if(self.enlarged == True):
                self.enlarged = False
            return False
    
    def on_press(self):
        self.pressed = True
        self.text.color = (255, 255, 0, 255)  # Change text color to yellow

    def on_release(self):
        self.pressed = False
        self.text.color = (255, 255, 255, 255)  # Change text color back to white

    def draw(self):
        if(self.pressed == True and self.enlarged == False):
            square = pyglet.shapes.Rectangle(self.x, self.y, self.width, self.height, color=self.pressed_color)
        elif(self.pressed == True and self.enlarged == True):
            square = pyglet.shapes.Rectangle(self.x-30, self.y-20, self.width+60, self.height+40, color=self.pressed_color)
        elif(self.pressed == False and self.enlarged == True):
            square = pyglet.shapes.Rectangle(self.x-30, self.y-20, self.width+60, self.height+40, color=self.default_color)
        else:
            square = pyglet.shapes.Rectangle(self.x, self.y, self.width, self.height, color=self.default_color)
        square.opacity = int(0.5 * 255)
        square.draw()
        glEnable(GL_BLEND) # type: ignore
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # type: ignore
        self.text.x = self.x + self.width // 2
        self.text.y = self.y + self.height // 2
        self.text.draw()
        glEnable(GL_BLEND) # type: ignore
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # type: ignore


# View class displays all images to the screen
class View(pyglet.window.Window):
    def __init__(self, Model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = Model
        #configure display
        display = pyglet.canvas.Display()
        screen = display.get_default_screen()
        self.monitor_width = screen.width
        self.monitor_height = screen.height
        self.set_size(self.monitor_width, self.monitor_height)
        self.set_fullscreen(True)
        glEnable(GL_BLEND) # type: ignore
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # type: ignore
        self.buttons = []
        start_game_button = Button(self.monitor_width * 2 / 3, self.monitor_height * 1 / 15, self.monitor_width / 10, self.monitor_height / 15, (0, 125, 0), "Start game")
        self.buttons.append(start_game_button)
        self.menu = True
        
        # Load images
        try:
            self.dark_wood_image = pyglet.resource.image("darkWood.jpg")
            self.light_wood_image = pyglet.resource.image("lightWood.jpg")
            self.medium_wood_image = pyglet.resource.image("mediumWood.jpg")
            self.selected_medium_wood_image = pyglet.resource.image("selectedMediumWood.jpg")
            self.selected_light_wood_image = pyglet.resource.image("selectedLightWood.jpg")
            
            self.black_pawn_image = pyglet.resource.image("blackPawn.png")
            self.black_knight_image = pyglet.resource.image("blackKnight.png")
            self.black_bishop_image = pyglet.resource.image("blackBishop.png")
            self.black_rook_image = pyglet.resource.image("blackRook.png")
            self.black_queen_image = pyglet.resource.image("blackQueen.png")
            self.black_king_image = pyglet.resource.image("blackKing.png")
            self.white_pawn_image = pyglet.resource.image("whitePawn.png")
            self.white_knight_image = pyglet.resource.image("whiteKnight.png")
            self.white_bishop_image = pyglet.resource.image("whiteBishop.png")
            self.white_rook_image = pyglet.resource.image("whiteRook.png")
            self.white_queen_image = pyglet.resource.image("whiteQueen.png")
            self.white_king_image = pyglet.resource.image("whiteKing.png")
        except FileNotFoundError:
            print("Error: Image not found")

        
        #constants
        self.square_width = self.monitor_height/10
        self.spacing = 100
        
        #set widths of square images
        self.dark_wood_image.width = self.monitor_width
        self.dark_wood_image.height = self.monitor_height
        self.light_wood_image.width = self.square_width
        self.light_wood_image.height = self.square_width
        self.medium_wood_image.width = self.square_width
        self.medium_wood_image.height = self.square_width
        self.selected_light_wood_image.height = self.square_width
        self.selected_light_wood_image.width = self.square_width
        self.selected_medium_wood_image.height = self.square_width
        self.selected_medium_wood_image.width = self.square_width

        #set pieces width and height
        self.black_pawn_image.width = self.square_width - 0
        self.black_pawn_image.height = self.square_width - 0
        self.black_knight_image.width = self.square_width - 0
        self.black_knight_image.height = self.square_width - 0
        self.black_bishop_image.width = self.square_width - 0
        self.black_bishop_image.height = self.square_width - 0
        self.black_rook_image.width = self.square_width - 0
        self.black_rook_image.height = self.square_width - 0
        self.black_queen_image.width = self.square_width - 0
        self.black_queen_image.height = self.square_width - 0
        self.black_king_image.width = self.square_width - 0
        self.black_king_image.height = self.square_width - 0
        self.white_pawn_image.width = self.square_width - 0
        self.white_pawn_image.height = self.square_width - 0
        self.white_knight_image.width = self.square_width - 0
        self.white_knight_image.height = self.square_width - 0
        self.white_bishop_image.width = self.square_width - 0
        self.white_bishop_image.height = self.square_width - 0
        self.white_rook_image.width = self.square_width - 0
        self.white_rook_image.height = self.square_width - 0
        self.white_queen_image.width = self.square_width - 0
        self.white_queen_image.height = self.square_width - 0
        self.white_king_image.width = self.square_width - 0
        self.white_king_image.height = self.square_width  - 0

        #define highlights
        self.highlights = [[False for _ in range(8)] for _ in range(8)] 
        self.red_highlights = [[False for _ in range(8)] for _ in range(8)]
        self.mouse_held = False
        self.held_piece = None
        self.held_coords = None

    def on_draw(self):
        self.clear()
        #draw background
        self.dark_wood_image.blit(0, 0)
        #draw chess background
        self.chess_background()
        #draw held_highlights
        self.move_highlight()
        #draw red highlights
        self.draw_red_highlights()
        #draw piece positions
        self.draw_board()
        #draw promotions
        self.promotion_draw()
        #check mate
        self.check_mate()
        if(self.menu == True):
            self.menu_handler()
        return
    
    def draw_board(self):
        for i in range(8):
            for j in range(8):
                p = self.model.board[i][j]
                r = -1
                f = -1
                if(self.held_piece != None and self.mouse_held == True):
                    r = self.held_piece[0]
                    f = self.held_piece[1]
                if((p != 'S') and (i != r or j != f)):
                    p = p.piece_char()
                    match p:
                        case 'r':
                            self.black_rook_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                        case 'n':
                            self.black_knight_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                        case 'b':
                            self.black_bishop_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                        case 'q':
                            self.black_queen_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                        case 'k':
                            self.black_king_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                        case 'p':
                            self.black_pawn_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                        case 'R':
                            self.white_rook_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                        case 'N':
                            self.white_knight_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                        case 'B':
                            self.white_bishop_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                        case 'Q':
                            self.white_queen_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                        case 'K':
                            self.white_king_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                        case 'P':
                            self.white_pawn_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
        if(self.held_piece != None and self.mouse_held == True):
            p = self.model.board[self.held_piece[0]][self.held_piece[1]]
            if((p != 'S') and self.held_coords != None and self.mouse_held == True):
                p = p.piece_char()
                x = self.held_coords[0]
                y = self.held_coords[1]
                match p:
                    case 'r':
                        self.black_rook_image.blit(x-(self.square_width/2), y-(self.square_width/2))
                    case 'n':
                        self.black_knight_image.blit(x-(self.square_width/2), y-(self.square_width/2))
                    case 'b':
                        self.black_bishop_image.blit(x-(self.square_width/2), y-(self.square_width/2))
                    case 'q':
                        self.black_queen_image.blit(x-(self.square_width/2), y-(self.square_width/2))
                    case 'k':
                        self.black_king_image.blit(x-(self.square_width/2), y-(self.square_width/2))
                    case 'p':
                        self.black_pawn_image.blit(x-(self.square_width/2), y-(self.square_width/2))
                    case 'R':
                        self.white_rook_image.blit(x-(self.square_width/2), y-(self.square_width/2))
                    case 'N':
                        self.white_knight_image.blit(x-(self.square_width/2), y-(self.square_width/2))
                    case 'B':
                        self.white_bishop_image.blit(x-(self.square_width/2), y-(self.square_width/2))
                    case 'Q':
                        self.white_queen_image.blit(x-(self.square_width/2), y-(self.square_width/2))
                    case 'K':
                        self.white_king_image.blit(x-(self.square_width/2), y-(self.square_width/2))
                    case 'P':
                        self.white_pawn_image.blit(x-(self.square_width/2), y-(self.square_width/2))
        return
    
    def red_detection(self, x, y):
        x = (x - self.spacing) // self.square_width
        y = (y - self.spacing) // self.square_width
        self.red_highlights[int(y)][int(x)] = True
    
    def detection(self, x, y):
        for i in range(8):
            for j in range(8):
                self.red_highlights[i][j] = False
        if(x == None or y == None):
            return
        else:
            x = (x - self.spacing) // self.square_width
            y = (y - self.spacing) // self.square_width
            if(x >= 0 and y >= 0 and x < 8 and y < 8):
                self.highlights[int(y)][int(x)] = True
                for i in range(8):
                    for j in range(8):
                        if(self.highlights[i][j] == True and (i != int(y) or j != int(x))):
                            if(self.menu == False):
                                self.model.move_piece(i, j, int(y), int(x))
                            self.highlights[i][j] = False
                            self.highlights[int(y)][int(x)] = True
                            break
                piece = self.model.board[int(y)][int(x)]
                if(piece == 'S'):
                    self.highlights[int(y)][int(x)] = False
            else:
                for i in range(8):
                    for j in range(8):
                        self.highlights[i][j] = False
        return
    
    def promotion_detection(self, x, y):
        if(self.menu):
            return
        if(x == None or y == None):
            return
        else:
            x = (x - self.spacing) // self.square_width
            y = (y - self.spacing) // self.square_width
            if(x >= 0 and y >= 0 and x < 8 and y < 8):
                for i in range(8):
                    for j in range(8):
                        piece = self.model.board[i][j]
                        if(piece != 'S' and piece.piece_char() == 'P' and i == 7):
                            distance = i - int(y)
                            if(distance > 3 or distance < 0):
                                return
                            rank = 7 - i
                            match distance:
                                case 0:
                                    self.model.set_piece(rank, j, 'Q')
                                case 1:
                                    self.model.set_piece(rank, j, 'N')
                                case 2:
                                    self.model.set_piece(rank, j, 'R')
                                case 3:
                                    self.model.set_piece(rank, j, 'B')
                            self.model.promotion = False
                            self.model.to_move = 'b'
                            self.model.update_legal_moves()
                            break
                        elif(piece != 'S' and piece.piece_char() == 'p' and i == 0):
                            distance = i + int(y)
                            if(distance > 3 or distance < 0):
                                return
                            rank = 7 - i
                            match distance:
                                case 0:
                                    self.model.set_piece(rank, j, 'q')
                                case 1:
                                    self.model.set_piece(rank, j, 'n')
                                case 2:
                                    self.model.set_piece(rank, j, 'r')
                                case 3:
                                    self.model.set_piece(rank, j, 'b')
                            self.model.promotion = False
                            self.model.to_move = 'w'
                            self.model.update_legal_moves()
                            break
        return

    def piece_held(self, x, y):
        if(self.menu):
            return
        x = (x - self.spacing) // self.square_width
        y = (y - self.spacing) // self.square_width
        if(int(y) > 7 or int(x) > 7 or int(y) < 0 or int(x) < 0):
            return
        self.held_piece = (int(y), int(x))
    
    def chess_background(self):
        for i in range(0, 8):
            for j in range(0, 8):
                if(((j % 2 == 0) and (i % 2 == 0)) or ((j % 2 == 1) and (i % 2 == 1))):
                    self.light_wood_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                else:
                    self.medium_wood_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
    
    def move_highlight(self):
        if(self.held_coords != None and self.mouse_held == True and self.held_piece != None and self.menu == False):
            # Draw a filled rectangle (square)
            x = (self.held_coords[0] - self.spacing) // self.square_width
            y = (self.held_coords[1] - self.spacing) // self.square_width
            size = self.square_width  # Size of the square

            # Use pyglet.shapes.Rectangle to draw the square
            square = pyglet.shapes.Rectangle(self.square_width*x + self.spacing, self.square_width*y + self.spacing, size, size, color=(int(0.0 * 255), int(0.0 * 255), int(0.0 * 255)))
            square.opacity = int(0.2 * 255)
            square.draw()
            glEnable(GL_BLEND) # type: ignore
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # type: ignore
    
    def draw_red_highlights(self):
        for i in range(8):
            for j in range(8):
                if(self.red_highlights[i][j] == True):

                    # Draw a filled rectangle (square)
                    x, y = self.square_width*j + self.spacing, self.square_width*i + self.spacing  # Position of the bottom-left corner
                    size = self.square_width  # Size of the square

                    # Use pyglet.shapes.Rectangle to draw the square
                    square = pyglet.shapes.Rectangle(x, y, size, size, color=(int(1.0 * 255), int(0.0 * 255), int(0.0 * 255)))
                    square.opacity = int(0.5 * 255)
                    square.draw()
                    glEnable(GL_BLEND) # type: ignore
                    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # type: ignore
                if(self.highlights[i][j] == True):
                    if(((j % 2 == 0) and (i % 2 == 0)) or ((j % 2 == 1) and (i % 2 == 1))):
                        self.selected_light_wood_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                    else:
                        self.selected_medium_wood_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                    piece = self.model.board[i][j]
                    if(piece != 'S' and self.model.to_move == piece.get_color()):
                        moves = piece.get_legal_moves()
                        for rank in range(8):
                            for file in range(8):
                                if(moves[rank][file] == True):
                                    circle = pyglet.shapes.Circle(self.square_width*file + self.spacing + 0.5 * self.square_width, self.square_width*rank + self.spacing + 0.5 * self.square_width, self.square_width / 4, color=(0, 0, 0, 160))
                                    circle.draw()
                                    glEnable(GL_BLEND) # type: ignore
                                    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # type: ignore
    
    def promotion_draw(self):
        if(self.menu):
            return
        if(self.model.promotion == True):
            for i in range(8):
                for j in range(8):
                    piece = self.model.board[i][j]
                    if(piece != 'S' and piece.piece_char() == 'P' and i == 7):
                        square = pyglet.shapes.Rectangle(self.square_width*j + self.spacing, self.square_width*i + self.spacing, self.square_width, self.square_width, color=(int(1.0 * 255), int(1.0 * 255), int(1.0 * 255)))
                        square.opacity = int(1 * 255)
                        square.draw()
                        square = pyglet.shapes.Rectangle(self.square_width*j + self.spacing, self.square_width*(i-1) + self.spacing, self.square_width, self.square_width, color=(int(1.0 * 255), int(1.0 * 255), int(1.0 * 255)))
                        square.opacity = int(1 * 255)
                        square.draw()
                        square = pyglet.shapes.Rectangle(self.square_width*j + self.spacing, self.square_width*(i-2) + self.spacing, self.square_width, self.square_width, color=(int(1.0 * 255), int(1.0 * 255), int(1.0 * 255)))
                        square.opacity = int(1 * 255)
                        square.draw()
                        square = pyglet.shapes.Rectangle(self.square_width*j + self.spacing, self.square_width*(i-3) + self.spacing, self.square_width, self.square_width, color=(int(1.0 * 255), int(1.0 * 255), int(1.0 * 255)))
                        square.opacity = int(1 * 255)
                        square.draw()
                        glEnable(GL_BLEND) # type: ignore
                        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # type: ignore
                        self.white_queen_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                        self.white_knight_image.blit(self.square_width*j + self.spacing, self.square_width*(i-1) + self.spacing)
                        self.white_rook_image.blit(self.square_width*j + self.spacing, self.square_width*(i-2) + self.spacing)
                        self.white_bishop_image.blit(self.square_width*j + self.spacing, self.square_width*(i-3) + self.spacing)
                        break
                    elif(piece != 'S' and piece.piece_char() == 'p' and i == 0):
                        square = pyglet.shapes.Rectangle(self.square_width*j + self.spacing, self.square_width*i + self.spacing, self.square_width, self.square_width, color=(int(1.0 * 255), int(1.0 * 255), int(1.0 * 255)))
                        square.opacity = int(1 * 255)
                        square.draw()
                        square = pyglet.shapes.Rectangle(self.square_width*j + self.spacing, self.square_width*(i+1) + self.spacing, self.square_width, self.square_width, color=(int(1.0 * 255), int(1.0 * 255), int(1.0 * 255)))
                        square.opacity = int(1 * 255)
                        square.draw()
                        square = pyglet.shapes.Rectangle(self.square_width*j + self.spacing, self.square_width*(i+2) + self.spacing, self.square_width, self.square_width, color=(int(1.0 * 255), int(1.0 * 255), int(1.0 * 255)))
                        square.opacity = int(1 * 255)
                        square.draw()
                        square = pyglet.shapes.Rectangle(self.square_width*j + self.spacing, self.square_width*(i+3) + self.spacing, self.square_width, self.square_width, color=(int(1.0 * 255), int(1.0 * 255), int(1.0 * 255)))
                        square.opacity = int(1 * 255)
                        square.draw()
                        glEnable(GL_BLEND) # type: ignore
                        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # type: ignore
                        self.black_queen_image.blit(self.square_width*j + self.spacing, self.square_width*i + self.spacing)
                        self.black_knight_image.blit(self.square_width*j + self.spacing, self.square_width*(i+1) + self.spacing)
                        self.black_rook_image.blit(self.square_width*j + self.spacing, self.square_width*(i+2) + self.spacing)
                        self.black_bishop_image.blit(self.square_width*j + self.spacing, self.square_width*(i+3) + self.spacing)
                        break

    def menu_handler(self):
        for button in self.buttons:
            button.draw()
            if(button.message == "Start game" and button.pressed == True):
                self.model.reset_game()
                self.menu = False
                return
        return
    
    def check_mate(self):
        if(self.model.is_mate == True):
            if(self.model.to_move == 'w'):
                label = pyglet.text.Label(
                    'Black Wins!',
                    font_name='Times New Roman',
                    font_size=72,
                    x=self.monitor_width/2, y=self.monitor_height/2,
                    anchor_x='center', anchor_y='center'
                )
            else:
                label = pyglet.text.Label(
                    'White Wins!',
                    font_name='Times New Roman',
                    font_size=72,
                    x=self.monitor_width/2, y=self.monitor_height/2,
                    anchor_x='center', anchor_y='center'
                )
            self.menu = True
            label.draw()
            glEnable(GL_BLEND) # type: ignore
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # type: ignore
        if(self.model.is_stalemate == True):
            if(self.model.to_move == 'w'):
                label = pyglet.text.Label(
                    'White is stalemated. Draw!',
                    font_name='Times New Roman',
                    font_size=72,
                    x=self.monitor_width/2, y=self.monitor_height/2,
                    anchor_x='center', anchor_y='center'
                )
            else:
                label = pyglet.text.Label(
                    'Black is stalemated. Draw!',
                    font_name='Times New Roman',
                    font_size=72,
                    x=self.monitor_width/2, y=self.monitor_height/2,
                    anchor_x='center', anchor_y='center'
                )
            self.menu = True
            label.draw()
            glEnable(GL_BLEND) # type: ignore
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # type: ignore

class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.keep_going = True
        self.keys_pressed = set()
        self.last_click_time = 0
        self.debounce_time = 0.001
        self.mouse_pressed = False

    def update(self, dt):
        var = 0

    def on_mouse_press(self, x, y, button, modifiers):
        # Handle mouse press event with debouncing
        current_time = time.time()
        if current_time - self.last_click_time > self.debounce_time:
            self.last_click_time = current_time
            if self.model.promotion == False:
                if button == pyglet.window.mouse.LEFT:
                    self.view.detection(x, y)
                elif button == pyglet.window.mouse.RIGHT:
                    self.view.red_detection(x, y)
            else:
                if button == pyglet.window.mouse.LEFT:
                    self.view.promotion_detection(x, y)
            self.view.mouse_held = True
            self.view.piece_held(x, y)
            self.view.held_coords = (int(x), int(y))
            self.mouse_pressed = True
            for button in self.view.buttons:
                if(button.is_mouse_over(int(x), int(y))):
                    button.on_press()
                else:
                    button.on_release()

    def on_mouse_release(self, x, y, button, modifiers):
        # Handle mouse press event with debouncing
        current_time = time.time()
        if current_time - self.last_click_time > self.debounce_time:
            self.last_click_time = current_time
            if self.model.promotion == False:
                if button == pyglet.window.mouse.LEFT:
                    self.view.detection(x, y)
                elif button == pyglet.window.mouse.RIGHT:
                    self.view.red_detection(x, y)
            else:
                if button == pyglet.window.mouse.LEFT:
                    self.view.promotion_detection(x, y)
            self.view.mouse_held = False
            self.mouse_pressed = False
            self.view.held_piece = None

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.view.held_coords = (int(x), int(y))
        
    def on_mouse_motion(self, x, y, dx, dy):
        for button in self.view.buttons:
            x = button.is_mouse_over(int(x), int(y))
    
    def update_model(self, model):
        self.model = model

class Model():
    class Graph:
        def __init__(self, board, mover):
            init_node = self.Node()
            init_node.board = board
            init_node.depth = 0
            init_node.mover = mover
            self.depth = 0
            self.root_node = init_node
        class Node:
            def __init__(self):
                self.board = [['S' for _ in range(8)] for _ in range(8)]
                self.evaluation = 0.0
                self.depth = 0
                self.future_positions = []
                self.mover = 'w'
        
        def create_new_position_node(self, node, board, depth, mover):
            new_node = self.Node()
            new_node.board = board
            new_node.depth = depth
            new_node.mover = mover
            self.evaluate_position_node(new_node)
            node.future_positions.append(new_node)
        
        def evaluate_position_node(self, node):
            for rank in range(8):
                for file in range(8):
                    piece = node.board[rank][file]
                    if(piece != 'S' and piece.piece_char() != 'k' and piece.piece_char() != 'K'):
                        match piece.piece_char():
                            case 'r':
                                node.evaluation -= 5
                            case 'n':
                                node.evaluation -= 3
                            case 'b':
                                node.evaluation -= 3.25
                            case 'q':
                                node.evaluation -= 9
                            case 'p':
                                node.evaluation -= 1
                            case 'R':
                                node.evaluation += 5
                            case 'N':
                                node.evaluation += 3
                            case 'B':
                                node.evaluation += 3.25
                            case 'Q':
                                node.evaluation += 9
                            case 'P':
                                node.evaluation += 1
            return
    def __init__(self):
        self.reset_game()
        
    def update(self, view):
        self.view = view
    
    def update_legal_moves(self):
        self.checkers = []
        self.in_check = False
        self.white_vision = [[False for _ in range(8)] for _ in range(8)]
        self.black_vision = [[False for _ in range(8)] for _ in range(8)]
        #updates the legal moves of pieces that are not the same color as the piece to move
        for rank in range(8):
            for file in range(8):
                piece = self.board[rank][file]
                if(piece != 'S' and piece.get_color() != self.to_move):
                    piece.update_legal_moves(self.board, rank, file, self.prevMove_rank, self.prevMove_file, self.in_check, self.checkers, self.double_move, self.white_king_rank, self.white_king_file, self.black_king_rank, self.black_king_file, self.black_vision, self.white_vision)
        #find king locations and check if in check
        for rank in range(8):
            for file in range(8):
                piece = self.board[rank][file]
                if(piece != 'S'):
                    #black king
                    if(piece.piece_char() == 'k'):
                        self.black_king_rank = rank
                        self.black_king_file = file
                        if(self.to_move == 'b'):
                            for Rank in range(8):
                                for File in range(8):
                                    Piece = self.board[Rank][File]
                                    if(Piece != 'S'):
                                        moves = Piece.get_legal_moves()
                                        if(moves[rank][file] == True):
                                            self.in_check = True
                                            checker = (Rank, File)
                                            self.checkers.append(checker)
                    elif(piece.piece_char() == 'K'):
                        self.white_king_rank = rank
                        self.white_king_file = file
                        if(self.to_move == 'w'):
                            for Rank in range(8):
                                for File in range(8):
                                    Piece = self.board[Rank][File]
                                    if(Piece != 'S'):
                                        moves = Piece.get_legal_moves()
                                        if(moves[rank][file] == True):
                                            self.in_check = True
                                            checker = (Rank, File)
                                            self.checkers.append(checker)
        #updates legal moves of pieces that are the same color            
        for rank in range(8):
            for file in range(8):
                piece = self.board[rank][file]
                if(piece != 'S' and piece.get_color() == self.to_move):
                    piece.update_legal_moves(self.board, rank, file, self.prevMove_rank, self.prevMove_file, self.in_check, self.checkers, self.double_move, self.white_king_rank, self.white_king_file, self.black_king_rank, self.black_king_file, self.black_vision, self.white_vision)
        self.check_mate()
    
    def check_mate(self):
        for rank in range(8):
            for file in range(8):
                piece = self.board[rank][file]
                if(piece != 'S' and piece.get_color() == self.to_move):
                    moves = piece.get_legal_moves()
                    for Rank in range(8):
                        for File in range(8):
                            if(moves[Rank][File] == True):
                                return
        if(self.in_check == True):
            self.is_mate = True
        else:
            self.is_stalemate = True
    
    def move_piece(self, mover_rank, mover_file, move_to_rank, move_to_file):
        mover_piece = self.board[mover_rank][mover_file]
        if(mover_piece != 'S' and mover_piece.get_color() == self.to_move):
            legal_moves = mover_piece.get_legal_moves()
            if(legal_moves[move_to_rank][move_to_file] == True):
                self.board[move_to_rank][move_to_file] = mover_piece
                self.board[mover_rank][mover_file] = 'S'
                
                #check for en pessant
                if(self.double_move == True and (mover_piece.piece_char() == 'p' or mover_piece.piece_char() == 'P')):
                    mover_piece = self.board[move_to_rank][move_to_file]
                    if(mover_piece.get_color() == 'w' and self.prevMove_rank == move_to_rank-1 and self.prevMove_file == move_to_file):
                        self.board[self.prevMove_rank][self.prevMove_file] = 'S'
                    elif(mover_piece.get_color() == 'b' and self.prevMove_rank == move_to_rank+1 and self.prevMove_file == move_to_file):
                        self.board[self.prevMove_rank][self.prevMove_file] = 'S'
                
                #update previous move
                self.prevMove_rank = move_to_rank
                self.prevMove_file = move_to_file
                
                #check if double pawn move occured
                if((mover_piece.piece_char() == 'p' or mover_piece.piece_char() == 'P') and (abs(move_to_rank - mover_rank) == 2)):
                    self.double_move = True
                else:
                    self.double_move = False
                
                #check for castling
                if((mover_piece.piece_char() == 'k' or mover_piece.piece_char() == 'K') and (abs(move_to_file - mover_file) == 2)):
                    #check long side castle
                    if(move_to_file < mover_file):
                        rook = self.board[mover_rank][mover_file-4]
                        self.board[mover_rank][move_to_file+1] = rook
                        self.board[mover_rank][mover_file-4] = 'S'
                    else:
                        rook = self.board[mover_rank][mover_file+3]
                        self.board[mover_rank][move_to_file-1] = rook
                        self.board[mover_rank][mover_file+3] = 'S'
                
                if(mover_piece.piece_char() == 'p' and move_to_rank == 0):
                    self.promotion = True
                    for i in range(8):
                        for j in range(8):
                            mover_piece.legal_moves[i][j] = False
                elif(mover_piece.piece_char() == 'P' and move_to_rank == 7):
                    self.promotion = True
                    for i in range(8):
                        for j in range(8):
                            mover_piece.legal_moves[i][j] = False
                else:
                    #update to move
                    if(self.to_move == 'w'):
                        self.to_move = 'b'
                    else:
                        self.to_move = 'w'
                    #update legal moves
                    self.update_legal_moves()
        return
    
    def board_loader(self):
        i = 0 # temp interval
        p = ''
        for j in self.layout:
            rank = i // 8
            file = i % 8
            p = j
            if(p.isdigit()):
                i = i + int(p)
                i -= 1
            elif(p == '/'):
                i -= 1
            else:
                self.set_piece(rank, file, p)
            i += 1
    
    def set_piece(self, rank, file, p):
        rank = 7 - rank
        match p:
            case 'r':
                self.board[rank][file] = Black_Rook()
            case 'n':
                self.board[rank][file] = Black_Knight()
            case 'b':
                self.board[rank][file] = Black_Bishop()
            case 'q':
                self.board[rank][file] = Black_Queen()
            case 'k':
                self.board[rank][file] = Black_King()
            case 'p':
                self.board[rank][file] = Black_Pawn()
            case 'R':
                self.board[rank][file] = White_Rook()
            case 'N':
                self.board[rank][file] = White_Knight()
            case 'B':
                self.board[rank][file] = White_Bishop()
            case 'Q':
                self.board[rank][file] = White_Queen()
            case 'K':
                self.board[rank][file] = White_King()
            case 'P':
                self.board[rank][file] = White_Pawn()
    
    def reset_game(self):
        self.board = [['S' for _ in range(8)] for _ in range(8)]
        self.to_move = 'w'
        self.layout = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        self.prevMove_rank = None
        self.prevMove_file = None
        self.checkers = None
        self.in_check = False
        self.double_move = False
        self.promotion = False
        self.white_king_rank = None
        self.white_king_file = None
        self.black_king_rank = None
        self.black_king_file = None
        self.white_vision = [[False for _ in range(8)] for _ in range(8)]
        self.black_vision = [[False for _ in range(8)] for _ in range(8)]
        self.is_mate = False
        self.is_stalemate = False
        self.board_loader()
        self.update_legal_moves()
        self.graph = self.Graph(self.board, self.to_move)
        

class Piece():
    def __init__(self):
        self.legal_moves = [[False for _ in range(8)] for _ in range(8)]
    def piece_char(self):
        return 'S'
    def update_legal_moves(self, board, pi_rank, pi_file, prev_move_rank, prev_move_file, in_check, checkers, prev_double_move, white_king_rank, white_king_file, black_king_rank, black_king_file, black_vision, white_vision):
        return
    def get_legal_moves(self):
        return self.legal_moves
    def get_color(self):
        return 'S'

class Black_Pawn(Piece):
    def __init__(self):
        super().__init__()
    def piece_char(self):
        return 'p'
    def update_legal_moves(self, board, pi_rank, pi_file, prev_move_rank, prev_move_file, in_check, checkers, prev_double_move, white_king_rank, white_king_file, black_king_rank, black_king_file, black_vision, white_vision):
        king_rank = black_king_rank
        king_file = black_king_file
        #check if double check
        if(checkers != None and len(checkers) > 1):
            for rank in range(8):
                for file in range(8):
                    self.legal_moves[rank][file] = False
            return
        #get generic possible moves without considering pins and checks
        for rank in range(8):
            for file in range(8):
                self.legal_moves[rank][file] = False
        if(pi_rank != 6):
            moved = True
        else:
            moved = False
        for rank in range(8):
            for file in range(8):
                piece = board[rank][file]
                if(piece != 'S'):
                    pi_exist = True
                else:
                    pi_exist = False
                if(rank == pi_rank-1 and file == pi_file):
                    if(pi_exist == False):
                        self.legal_moves[rank][file] = True
                elif(rank == pi_rank-2 and file == pi_file and moved == False):
                    if(pi_exist == False and board[rank+1][file] == 'S'):
                        self.legal_moves[rank][file] = True
                elif(rank == pi_rank-1 and (abs(pi_file - file) == 1) and pi_exist == True):
                    if(piece.get_color() == 'w'):
                        self.legal_moves[rank][file] = True
                    black_vision[rank][file] = True
                elif(rank == pi_rank-1 and pi_rank == 3 and (abs(pi_file - file) == 1) and prev_double_move == True):
                    if(prev_move_rank != None and prev_move_file != None):
                        prev_piece = board[prev_move_rank][prev_move_file]
                    else:
                        prev_piece = None
                    if(pi_exist == False and prev_piece != None and prev_piece.piece_char() == 'P' and prev_move_rank == rank + 1 and prev_move_file == file):
                        self.legal_moves[rank][file] = True
                    black_vision[rank][file] = True
                else:
                    if(rank == pi_rank-1 and (abs(pi_file - file) == 1)):
                        black_vision[rank][file] = True
        #check if in check
        if(in_check):
            moves = [[False for _ in range(8)] for _ in range(8)]
            checker = checkers[0]
            checker_rank = checker[0]
            checker_file = checker[1]
            checker_piece = board[checker_rank][checker_file]
            #check for knight check
            if(self.legal_moves[checker_rank][checker_file] == True):
                moves[checker_rank][checker_file] = True
            if(checker_piece.piece_char() == 'N'):
                if(self.legal_moves[checker_rank][checker_file] == True):
                    moves[checker_rank][checker_file] = True
            else:
                #same rank Rook, Queen
                if(checker_rank == king_rank):
                    if(checker_file < king_file):
                        file = king_file-1
                        while(file > checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file -=1
                    else:
                        file = king_file+1
                        while(file < checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file +=1
                #same file Rook, Queen
                elif(checker_file == king_file):
                    if(checker_rank < king_rank):
                        rank = king_rank-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank -=1
                    else:
                        rank = king_rank+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank +=1
                #diagonal Bishop, Queen
                else:
                    #check top left
                    if(checker_rank > black_king_rank and checker_file < black_king_file):
                        rank = king_rank+1
                        file = king_file-1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file -=1
                    #check top right
                    elif(checker_rank > black_king_rank and checker_file > black_king_file):
                        rank = king_rank+1
                        file = king_file+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file +=1
                    #check bottom left
                    elif(checker_rank < black_king_rank and checker_file < black_king_file):
                        rank = king_rank-1
                        file = king_file-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file -=1
                    #check bottom right
                    else:
                        rank = king_rank-1
                        file = king_file+1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file +=1
            self.legal_moves = moves
        #check if pinned
        if(king_rank != None):
            pinned_count = 0
            direction = 0
            for rank in range(8):
                for file in range(8):
                    piece = board[rank][file]
                    if(piece != 'S' and piece.get_color() != 'b' and piece.piece_char() != 'p' and piece.piece_char() != 'n' and piece.piece_char() != 'k'):
                        moves = piece.get_legal_moves()
                        if(moves[pi_rank][pi_file] == True):
                            #same rank: rook, queen
                            if(rank == pi_rank):
                                if(king_rank == pi_rank):
                                    if(king_file < pi_file and file > pi_file):
                                        f = pi_file-1
                                        pinned = True
                                        while(f > king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 4
                                    elif(king_file > pi_file and file < pi_file):
                                        f = pi_file+1
                                        pinned = True
                                        while(f < king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 8
                            #same file: rook, queen
                            elif(file == pi_file):
                                if(king_file == pi_file):
                                    if(king_rank < pi_rank and rank > pi_rank):
                                        f = pi_rank-1
                                        pinned = True
                                        while(f > king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 2
                                    elif(king_rank > pi_rank and rank < pi_rank):
                                        f = pi_rank+1
                                        pinned = True
                                        while(f < king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 6
                            #diag: bishop queen
                            else:
                                #top left
                                if(rank > pi_rank and file < pi_file):
                                    if(pi_rank - king_rank == king_file - pi_file):
                                        r = pi_rank-1
                                        f = pi_file+1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 1
                                #top right
                                elif(rank > pi_rank and file > pi_file):
                                    if(pi_rank - king_rank == pi_file - king_file):
                                        r = pi_rank-1
                                        f = pi_file-1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 3
                                #bottom left
                                elif(rank < pi_rank and file < pi_file):
                                    if(king_rank - pi_rank == king_file - pi_file):
                                        r = pi_rank+1
                                        f = pi_file+1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 7
                                #bottom right
                                else:
                                    if(king_rank - pi_rank == pi_file - king_file):
                                        r = pi_rank+1
                                        f = pi_file-1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 5
            if(pinned_count > 0):
                if(pinned_count > 1):
                    moves = [[False for _ in range(8)] for _ in range(8)]
                    self.legal_moves = moves
                    return
                else:
                    match(direction):
                        case 1:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 2:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank > pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 3:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 4:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file > pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 5:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 6:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank < pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 7:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 8:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file < pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
        return
    def get_legal_moves(self):
        return self.legal_moves
    def get_color(self):
        return 'b'

class Black_Knight(Piece):
    def __init__(self):
        super().__init__()
    def piece_char(self):
        return 'n'
    def update_legal_moves(self, board, pi_rank, pi_file, prev_move_rank, prev_move_file, in_check, checkers, prev_double_move, white_king_rank, white_king_file, black_king_rank, black_king_file, black_vision, white_vision):
        king_rank = black_king_rank
        king_file = black_king_file
        #check if double check
        if(checkers != None and len(checkers) > 1):
            for rank in range(8):
                for file in range(8):
                    self.legal_moves[rank][file] = False
            return
        for rank in range(8):
            for file in range(8):
                self.legal_moves[rank][file] = False
        for rank in range(8):
            for file in range(8):
                if(rank == pi_rank + 2 and file == pi_file + 1):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'w'):
                        self.legal_moves[rank][file] = True
                    black_vision[rank][file] = True
                elif(rank == pi_rank + 2 and file == pi_file - 1):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'w'):
                        self.legal_moves[rank][file] = True
                    black_vision[rank][file] = True
                elif(rank == pi_rank - 2 and file == pi_file + 1):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'w'):
                        self.legal_moves[rank][file] = True
                    black_vision[rank][file] = True
                elif(rank == pi_rank - 2 and file == pi_file - 1):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'w'):
                        self.legal_moves[rank][file] = True
                    black_vision[rank][file] = True
                elif(rank == pi_rank + 1 and file == pi_file + 2):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'w'):
                        self.legal_moves[rank][file] = True
                    black_vision[rank][file] = True
                elif(rank == pi_rank + 1 and file == pi_file - 2):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'w'):
                        self.legal_moves[rank][file] = True
                    black_vision[rank][file] = True
                elif(rank == pi_rank - 1 and file == pi_file + 2):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'w'):
                        self.legal_moves[rank][file] = True
                    black_vision[rank][file] = True
                if(rank == pi_rank - 1 and file == pi_file - 2):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'w'):
                        self.legal_moves[rank][file] = True
                    black_vision[rank][file] = True
                #check if in check
        if(in_check):
            moves = [[False for _ in range(8)] for _ in range(8)]
            checker = checkers[0]
            checker_rank = checker[0]
            checker_file = checker[1]
            checker_piece = board[checker_rank][checker_file]
            #check for knight check
            if(self.legal_moves[checker_rank][checker_file] == True):
                moves[checker_rank][checker_file] = True
            if(checker_piece.piece_char() == 'N'):
                if(self.legal_moves[checker_rank][checker_file] == True):
                    moves[checker_rank][checker_file] = True
            else:
                #same rank Rook, Queen
                if(checker_rank == king_rank):
                    if(checker_file < king_file):
                        file = king_file-1
                        while(file > checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file -=1
                    else:
                        file = king_file+1
                        while(file < checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file +=1
                #same file Rook, Queen
                elif(checker_file == king_file):
                    if(checker_rank < king_rank):
                        rank = king_rank-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank -=1
                    else:
                        rank = king_rank+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank +=1
                #diagonal Bishop, Queen
                else:
                    #check top left
                    if(checker_rank > black_king_rank and checker_file < black_king_file):
                        rank = king_rank+1
                        file = king_file-1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file -=1
                    #check top right
                    elif(checker_rank > black_king_rank and checker_file > black_king_file):
                        rank = king_rank+1
                        file = king_file+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file +=1
                    #check bottom left
                    elif(checker_rank < black_king_rank and checker_file < black_king_file):
                        rank = king_rank-1
                        file = king_file-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file -=1
                    #check bottom right
                    else:
                        rank = king_rank-1
                        file = king_file+1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file +=1
            self.legal_moves = moves
        #check if pinned
        if(king_rank != None):
            pinned_count = 0
            direction = 0
            for rank in range(8):
                for file in range(8):
                    piece = board[rank][file]
                    if(piece != 'S' and piece.get_color() != 'b' and piece.piece_char() != 'p' and piece.piece_char() != 'n' and piece.piece_char() != 'k'):
                        moves = piece.get_legal_moves()
                        if(moves[pi_rank][pi_file] == True):
                            #same rank: rook, queen
                            if(rank == pi_rank):
                                if(king_rank == pi_rank):
                                    if(king_file < pi_file and file > pi_file):
                                        f = pi_file-1
                                        pinned = True
                                        while(f > king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 4
                                    elif(king_file > pi_file and file < pi_file):
                                        f = pi_file+1
                                        pinned = True
                                        while(f < king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 8
                            #same file: rook, queen
                            elif(file == pi_file):
                                if(king_file == pi_file):
                                    if(king_rank < pi_rank and rank > pi_rank):
                                        f = pi_rank-1
                                        pinned = True
                                        while(f > king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 2
                                    elif(king_rank > pi_rank and rank < pi_rank):
                                        f = pi_rank+1
                                        pinned = True
                                        while(f < king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 6
                            #diag: bishop queen
                            else:
                                #top left
                                if(rank > pi_rank and file < pi_file):
                                    if(pi_rank - king_rank == king_file - pi_file):
                                        r = pi_rank-1
                                        f = pi_file+1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 1
                                #top right
                                elif(rank > pi_rank and file > pi_file):
                                    if(pi_rank - king_rank == pi_file - king_file):
                                        r = pi_rank-1
                                        f = pi_file-1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 3
                                #bottom left
                                elif(rank < pi_rank and file < pi_file):
                                    if(king_rank - pi_rank == king_file - pi_file):
                                        r = pi_rank+1
                                        f = pi_file+1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 7
                                #bottom right
                                else:
                                    if(king_rank - pi_rank == pi_file - king_file):
                                        r = pi_rank+1
                                        f = pi_file-1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 5
            if(pinned_count > 0):
                if(pinned_count > 1):
                    moves = [[False for _ in range(8)] for _ in range(8)]
                    self.legal_moves = moves
                    return
                else:
                    match(direction):
                        case 1:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 2:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank > pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 3:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 4:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file > pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 5:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 6:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank < pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 7:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 8:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file < pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
        return
    def get_legal_moves(self):
        return self.legal_moves
    def get_color(self):
        return 'b'

class Black_Bishop(Piece):
    def __init__(self):
        super().__init__()
    def piece_char(self):
        return 'b'
    def update_legal_moves(self, board, pi_rank, pi_file, prev_move_rank, prev_move_file, in_check, checkers, prev_double_move, white_king_rank, white_king_file, black_king_rank, black_king_file, black_vision, white_vision):
        king_rank = black_king_rank
        king_file = black_king_file
        #check if double check
        if(checkers != None and len(checkers) > 1):
            for rank in range(8):
                for file in range(8):
                    self.legal_moves[rank][file] = False
            return
        for rank in range(8):
            for file in range(8):
                self.legal_moves[rank][file] = False
        #check top right
        rank = pi_rank+1
        file = pi_file+1
        while(rank < 8 and file < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank += 1
            file += 1
        #check bottom left
        rank = pi_rank - 1
        file = pi_file - 1
        while(rank >= 0 and file >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank -= 1
            file -= 1
        #check bottom right
        rank = pi_rank - 1
        file = pi_file + 1
        while(rank >= 0 and file < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank -= 1
            file += 1
        #check top left
        rank = pi_rank + 1
        file = pi_file - 1
        while(rank < 8 and file >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank += 1
            file -= 1
        #check if in check
        if(in_check):
            moves = [[False for _ in range(8)] for _ in range(8)]
            checker = checkers[0]
            checker_rank = checker[0]
            checker_file = checker[1]
            checker_piece = board[checker_rank][checker_file]
            #check for knight check
            if(self.legal_moves[checker_rank][checker_file] == True):
                moves[checker_rank][checker_file] = True
            if(checker_piece.piece_char() == 'N'):
                if(self.legal_moves[checker_rank][checker_file] == True):
                    moves[checker_rank][checker_file] = True
            else:
                #same rank Rook, Queen
                if(checker_rank == king_rank):
                    if(checker_file < king_file):
                        file = king_file-1
                        while(file > checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file -=1
                    else:
                        file = king_file+1
                        while(file < checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file +=1
                #same file Rook, Queen
                elif(checker_file == king_file):
                    if(checker_rank < king_rank):
                        rank = king_rank-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank -=1
                    else:
                        rank = king_rank+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank +=1
                #diagonal Bishop, Queen
                else:
                    #check top left
                    if(checker_rank > black_king_rank and checker_file < black_king_file):
                        rank = king_rank+1
                        file = king_file-1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file -=1
                    #check top right
                    elif(checker_rank > black_king_rank and checker_file > black_king_file):
                        rank = king_rank+1
                        file = king_file+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file +=1
                    #check bottom left
                    elif(checker_rank < black_king_rank and checker_file < black_king_file):
                        rank = king_rank-1
                        file = king_file-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file -=1
                    #check bottom right
                    else:
                        rank = king_rank-1
                        file = king_file+1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file +=1
            self.legal_moves = moves
        #check if pinned
        if(king_rank != None):
            pinned_count = 0
            direction = 0
            for rank in range(8):
                for file in range(8):
                    piece = board[rank][file]
                    if(piece != 'S' and piece.get_color() != 'b' and piece.piece_char() != 'p' and piece.piece_char() != 'n' and piece.piece_char() != 'k'):
                        moves = piece.get_legal_moves()
                        if(moves[pi_rank][pi_file] == True):
                            #same rank: rook, queen
                            if(rank == pi_rank):
                                if(king_rank == pi_rank):
                                    if(king_file < pi_file and file > pi_file):
                                        f = pi_file-1
                                        pinned = True
                                        while(f > king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 4
                                    elif(king_file > pi_file and file < pi_file):
                                        f = pi_file+1
                                        pinned = True
                                        while(f < king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 8
                            #same file: rook, queen
                            elif(file == pi_file):
                                if(king_file == pi_file):
                                    if(king_rank < pi_rank and rank > pi_rank):
                                        f = pi_rank-1
                                        pinned = True
                                        while(f > king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 2
                                    elif(king_rank > pi_rank and rank < pi_rank):
                                        f = pi_rank+1
                                        pinned = True
                                        while(f < king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 6
                            #diag: bishop queen
                            else:
                                #top left
                                if(rank > pi_rank and file < pi_file):
                                    if(pi_rank - king_rank == king_file - pi_file):
                                        r = pi_rank-1
                                        f = pi_file+1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 1
                                #top right
                                elif(rank > pi_rank and file > pi_file):
                                    if(pi_rank - king_rank == pi_file - king_file):
                                        r = pi_rank-1
                                        f = pi_file-1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 3
                                #bottom left
                                elif(rank < pi_rank and file < pi_file):
                                    if(king_rank - pi_rank == king_file - pi_file):
                                        r = pi_rank+1
                                        f = pi_file+1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 7
                                #bottom right
                                else:
                                    if(king_rank - pi_rank == pi_file - king_file):
                                        r = pi_rank+1
                                        f = pi_file-1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 5
            if(pinned_count > 0):
                if(pinned_count > 1):
                    moves = [[False for _ in range(8)] for _ in range(8)]
                    self.legal_moves = moves
                    return
                else:
                    match(direction):
                        case 1:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 2:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank > pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 3:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 4:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file > pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 5:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 6:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank < pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 7:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 8:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file < pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
        return
    def get_legal_moves(self):
        return self.legal_moves
    def get_color(self):
        return 'b'

class Black_Rook(Piece):
    def __init__(self):
        super().__init__()
        self.has_moved = False
        self.starting_rank = None
        self.starting_file = None
    def piece_char(self):
        return 'r'
    def update_legal_moves(self, board, pi_rank, pi_file, prev_move_rank, prev_move_file, in_check, checkers, prev_double_move, white_king_rank, white_king_file, black_king_rank, black_king_file, black_vision, white_vision):
        king_rank = black_king_rank
        king_file = black_king_file
        #check if double check
        if(checkers != None and len(checkers) > 1):
            for rank in range(8):
                for file in range(8):
                    self.legal_moves[rank][file] = False
            return
        if(self.starting_rank == None):
            self.starting_rank = pi_rank
            self.starting_file = pi_file
        if(self.starting_rank != pi_rank or self.starting_file != pi_file):
            self.has_moved = True
        for rank in range(8):
            for file in range(8):
                self.legal_moves[rank][file] = False
        #check top
        rank = pi_rank + 1
        file = pi_file
        while(rank < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank += 1
        #check bottom
        rank = pi_rank - 1
        file = pi_file
        while(rank >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank -= 1
        #check left
        rank = pi_rank
        file = pi_file - 1
        while(file >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            file -= 1
        #check right
        rank = pi_rank
        file = pi_file + 1
        while(file < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            file += 1
        #check if in check
        if(in_check):
            moves = [[False for _ in range(8)] for _ in range(8)]
            checker = checkers[0]
            checker_rank = checker[0]
            checker_file = checker[1]
            checker_piece = board[checker_rank][checker_file]
            #check for knight check
            if(self.legal_moves[checker_rank][checker_file] == True):
                moves[checker_rank][checker_file] = True
            if(checker_piece.piece_char() == 'N'):
                if(self.legal_moves[checker_rank][checker_file] == True):
                    moves[checker_rank][checker_file] = True
            else:
                #same rank Rook, Queen
                if(checker_rank == king_rank):
                    if(checker_file < king_file):
                        file = king_file-1
                        while(file > checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file -=1
                    else:
                        file = king_file+1
                        while(file < checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file +=1
                #same file Rook, Queen
                elif(checker_file == king_file):
                    if(checker_rank < king_rank):
                        rank = king_rank-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank -=1
                    else:
                        rank = king_rank+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank +=1
                #diagonal Bishop, Queen
                else:
                    #check top left
                    if(checker_rank > black_king_rank and checker_file < black_king_file):
                        rank = king_rank+1
                        file = king_file-1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file -=1
                    #check top right
                    elif(checker_rank > black_king_rank and checker_file > black_king_file):
                        rank = king_rank+1
                        file = king_file+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file +=1
                    #check bottom left
                    elif(checker_rank < black_king_rank and checker_file < black_king_file):
                        rank = king_rank-1
                        file = king_file-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file -=1
                    #check bottom right
                    else:
                        rank = king_rank-1
                        file = king_file+1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file +=1
            self.legal_moves = moves
        #check if pinned
        if(king_rank != None):
            pinned_count = 0
            direction = 0
            for rank in range(8):
                for file in range(8):
                    piece = board[rank][file]
                    if(piece != 'S' and piece.get_color() != 'b' and piece.piece_char() != 'p' and piece.piece_char() != 'n' and piece.piece_char() != 'k'):
                        moves = piece.get_legal_moves()
                        if(moves[pi_rank][pi_file] == True):
                            #same rank: rook, queen
                            if(rank == pi_rank):
                                if(king_rank == pi_rank):
                                    if(king_file < pi_file and file > pi_file):
                                        f = pi_file-1
                                        pinned = True
                                        while(f > king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 4
                                    elif(king_file > pi_file and file < pi_file):
                                        f = pi_file+1
                                        pinned = True
                                        while(f < king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 8
                            #same file: rook, queen
                            elif(file == pi_file):
                                if(king_file == pi_file):
                                    if(king_rank < pi_rank and rank > pi_rank):
                                        f = pi_rank-1
                                        pinned = True
                                        while(f > king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 2
                                    elif(king_rank > pi_rank and rank < pi_rank):
                                        f = pi_rank+1
                                        pinned = True
                                        while(f < king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 6
                            #diag: bishop queen
                            else:
                                #top left
                                if(rank > pi_rank and file < pi_file):
                                    if(pi_rank - king_rank == king_file - pi_file):
                                        r = pi_rank-1
                                        f = pi_file+1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 1
                                #top right
                                elif(rank > pi_rank and file > pi_file):
                                    if(pi_rank - king_rank == pi_file - king_file):
                                        r = pi_rank-1
                                        f = pi_file-1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 3
                                #bottom left
                                elif(rank < pi_rank and file < pi_file):
                                    if(king_rank - pi_rank == king_file - pi_file):
                                        r = pi_rank+1
                                        f = pi_file+1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 7
                                #bottom right
                                else:
                                    if(king_rank - pi_rank == pi_file - king_file):
                                        r = pi_rank+1
                                        f = pi_file-1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 5
            if(pinned_count > 0):
                if(pinned_count > 1):
                    moves = [[False for _ in range(8)] for _ in range(8)]
                    self.legal_moves = moves
                    return
                else:
                    match(direction):
                        case 1:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 2:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank > pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 3:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 4:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file > pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 5:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 6:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank < pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 7:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 8:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file < pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
        return
    def get_legal_moves(self):
        return self.legal_moves
    def get_color(self):
        return 'b'

class Black_Queen(Piece):
    def __init__(self):
        super().__init__()
    def piece_char(self):
        return 'q'
    def update_legal_moves(self, board, pi_rank, pi_file, prev_move_rank, prev_move_file, in_check, checkers, prev_double_move, white_king_rank, white_king_file, black_king_rank, black_king_file, black_vision, white_vision):
        king_rank = black_king_rank
        king_file = black_king_file
        #check if double check
        if(checkers != None and len(checkers) > 1):
            for rank in range(8):
                for file in range(8):
                    self.legal_moves[rank][file] = False
            return
        for rank in range(8):
            for file in range(8):
                self.legal_moves[rank][file] = False
        #check top
        rank = pi_rank + 1
        file = pi_file
        while(rank < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank += 1
        #check bottom
        rank = pi_rank - 1
        file = pi_file
        while(rank >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank -= 1
        #check left
        rank = pi_rank
        file = pi_file - 1
        while(file >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            file -= 1
        #check right
        rank = pi_rank
        file = pi_file + 1
        while(file < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            file += 1
        #check top right
        rank = pi_rank+1
        file = pi_file+1
        while(rank < 8 and file < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank += 1
            file += 1
        #check bottom left
        rank = pi_rank - 1
        file = pi_file - 1
        while(rank >= 0 and file >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank -= 1
            file -= 1
        #check bottom right
        rank = pi_rank - 1
        file = pi_file + 1
        while(rank >= 0 and file < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank -= 1
            file += 1
        #check top left
        rank = pi_rank + 1
        file = pi_file - 1
        while(rank < 8 and file >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'w'):
                self.legal_moves[rank][file] = True
            black_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank += 1
            file -= 1
        #check if in check
        if(in_check):
            moves = [[False for _ in range(8)] for _ in range(8)]
            checker = checkers[0]
            checker_rank = checker[0]
            checker_file = checker[1]
            checker_piece = board[checker_rank][checker_file]
            #check for knight check
            if(self.legal_moves[checker_rank][checker_file] == True):
                moves[checker_rank][checker_file] = True
            if(checker_piece.piece_char() == 'N'):
                if(self.legal_moves[checker_rank][checker_file] == True):
                    moves[checker_rank][checker_file] = True
            else:
                #same rank Rook, Queen
                if(checker_rank == king_rank):
                    if(checker_file < king_file):
                        file = king_file-1
                        while(file > checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file -=1
                    else:
                        file = king_file+1
                        while(file < checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file +=1
                #same file Rook, Queen
                elif(checker_file == king_file):
                    if(checker_rank < king_rank):
                        rank = king_rank-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank -=1
                    else:
                        rank = king_rank+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank +=1
                #diagonal Bishop, Queen
                else:
                    #check top left
                    if(checker_rank > black_king_rank and checker_file < black_king_file):
                        rank = king_rank+1
                        file = king_file-1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file -=1
                    #check top right
                    elif(checker_rank > black_king_rank and checker_file > black_king_file):
                        rank = king_rank+1
                        file = king_file+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file +=1
                    #check bottom left
                    elif(checker_rank < black_king_rank and checker_file < black_king_file):
                        rank = king_rank-1
                        file = king_file-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file -=1
                    #check bottom right
                    else:
                        rank = king_rank-1
                        file = king_file+1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file +=1
            self.legal_moves = moves
        #check if pinned
        if(king_rank != None):
            pinned_count = 0
            direction = 0
            for rank in range(8):
                for file in range(8):
                    piece = board[rank][file]
                    if(piece != 'S' and piece.get_color() != 'b' and piece.piece_char() != 'p' and piece.piece_char() != 'n' and piece.piece_char() != 'k'):
                        moves = piece.get_legal_moves()
                        if(moves[pi_rank][pi_file] == True):
                            #same rank: rook, queen
                            if(rank == pi_rank):
                                if(king_rank == pi_rank):
                                    if(king_file < pi_file and file > pi_file):
                                        f = pi_file-1
                                        pinned = True
                                        while(f > king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 4
                                    elif(king_file > pi_file and file < pi_file):
                                        f = pi_file+1
                                        pinned = True
                                        while(f < king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 8
                            #same file: rook, queen
                            elif(file == pi_file):
                                if(king_file == pi_file):
                                    if(king_rank < pi_rank and rank > pi_rank):
                                        f = pi_rank-1
                                        pinned = True
                                        while(f > king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 2
                                    elif(king_rank > pi_rank and rank < pi_rank):
                                        f = pi_rank+1
                                        pinned = True
                                        while(f < king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 6
                            #diag: bishop queen
                            else:
                                #top left
                                if(rank > pi_rank and file < pi_file):
                                    if(pi_rank - king_rank == king_file - pi_file):
                                        r = pi_rank-1
                                        f = pi_file+1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 1
                                #top right
                                elif(rank > pi_rank and file > pi_file):
                                    if(pi_rank - king_rank == pi_file - king_file):
                                        r = pi_rank-1
                                        f = pi_file-1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 3
                                #bottom left
                                elif(rank < pi_rank and file < pi_file):
                                    if(king_rank - pi_rank == king_file - pi_file):
                                        r = pi_rank+1
                                        f = pi_file+1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 7
                                #bottom right
                                else:
                                    if(king_rank - pi_rank == pi_file - king_file):
                                        r = pi_rank+1
                                        f = pi_file-1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 5
            if(pinned_count > 0):
                if(pinned_count > 1):
                    moves = [[False for _ in range(8)] for _ in range(8)]
                    self.legal_moves = moves
                    return
                else:
                    match(direction):
                        case 1:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 2:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank > pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 3:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 4:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file > pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 5:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 6:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank < pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 7:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 8:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file < pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
        return
    def get_legal_moves(self):
        return self.legal_moves
    def get_color(self):
        return 'b'

class Black_King(Piece):
    def __init__(self):
        super().__init__()
        self.has_moved = False
        self.starting_rank = None
        self.starting_file = None
    def piece_char(self):
        return 'k'
    def update_legal_moves(self, board, pi_rank, pi_file, prev_move_rank, prev_move_file, in_check, checkers, prev_double_move, white_king_rank, white_king_file, black_king_rank, black_king_file, black_vision, white_vision):
        if(self.starting_rank == None):
            self.starting_rank = pi_rank
            self.starting_file = pi_file
        if(self.has_moved == False and (self.starting_rank != pi_rank or self.starting_file != pi_file or self.starting_rank != 7 or self.starting_file != 4)):
            self.has_moved = True
        for rank in range(8):
            for file in range(8):
                self.legal_moves[rank][file] = False
        #check legal moves
        if(in_check):
            for checker in checkers:
                checker_rank = checker[0]
                checker_file = checker[1]
                piece = board[checker_rank][checker_file]
                if(piece.piece_char() != 'p' and piece.piece_char() != 'n'):
                    #same rank
                    if(checker_rank == pi_rank):
                        if(checker_file < pi_file):
                            if(pi_file < 7):
                                white_vision[pi_rank][pi_file+1] = True
                            if(pi_file-1 != checker_file):
                                white_vision[pi_rank][pi_file-1] = True
                        else:
                            if(pi_file > 0):
                                white_vision[pi_rank][pi_file-1] = True
                            if(pi_file + 1 != checker_file):
                                white_vision[pi_rank][pi_file+1] = True
                    #same file
                    elif(checker_file == pi_file):
                        if(checker_rank < pi_rank):
                            if(pi_rank < 7):
                                white_vision[pi_rank+1][pi_file] = True
                            if(pi_rank-1 != checker_rank):
                                white_vision[pi_rank-1][pi_file] = True
                        else:
                            if(pi_rank > 0):
                                white_vision[pi_rank-1][pi_file] = True
                            if(pi_rank + 1 != checker_rank):
                                white_vision[pi_rank+1][pi_file] = True
                    #top left
                    elif(checker_rank > pi_rank and checker_file < pi_file):
                        if(pi_rank > 0 and pi_file < 7):
                            white_vision[pi_rank-1][pi_file+1] = True
                        if(pi_rank+1 != checker_rank and pi_file-1 != checker_file):
                            white_vision[pi_rank+1][pi_file-1] = True
                    #top right
                    elif(checker_rank > pi_rank and checker_file > pi_file):
                        if(pi_rank > 0 and pi_file > 0):
                            white_vision[pi_rank-1][pi_file-1] = True
                        if(pi_rank+1 != checker_rank and pi_file+1 != checker_file):
                            white_vision[pi_rank+1][pi_file+1] = True
                    #bottom left
                    elif(checker_rank < pi_rank and checker_file < pi_file):
                        if(pi_rank < 7 and pi_file < 7):
                            white_vision[pi_rank+1][pi_file+1] = True
                        if(pi_rank-1 != checker_rank and pi_file-1 != checker_file):
                            white_vision[pi_rank-1][pi_file-1] = True
                    #bottom right
                    else:
                        if(pi_rank < 7 and pi_file > 0):
                            white_vision[pi_rank+1][pi_file-1] = True
                        if(pi_rank-1 != checker_rank and pi_file+1 != checker_file):
                            white_vision[pi_rank-1][pi_file+1] = True
        for rank in range(8):
            for file in range(8):
                piece = board[rank][file]
                if(abs(rank - pi_rank) <= 1 and abs(file - pi_file) <= 1):
                    if((piece == 'S' or piece.get_color() == 'w') and white_vision[rank][file] == False):
                        self.legal_moves[rank][file] = True
                    black_vision[rank][file] = True
        #check castling
        if(self.has_moved == False):
            right_rook = board[pi_rank][pi_file + 3]
            left_rook = board[pi_rank][pi_file - 4]
            if(right_rook != 'S' and right_rook.piece_char() == 'r' and right_rook.has_moved == False and board[pi_rank][pi_file + 1] == 'S' and board[pi_rank][pi_file + 2] == 'S' and white_vision[pi_rank][pi_file + 1] == False and white_vision[pi_rank][pi_file + 2] == False):
                self.legal_moves[pi_rank][pi_file + 2] = True
            if(left_rook != 'S' and left_rook.piece_char() == 'r' and left_rook.has_moved == False and board[pi_rank][pi_file - 1] == 'S' and board[pi_rank][pi_file - 2] == 'S' and board[pi_rank][pi_file - 3] == 'S' and white_vision[pi_rank][pi_file - 1] == False and white_vision[pi_rank][pi_file - 2] == False and white_vision[pi_rank][pi_file - 3] == False):
                self.legal_moves[pi_rank][pi_file - 2] = True
        return
    def get_legal_moves(self):
        return self.legal_moves
    def get_color(self):
        return 'b'

class White_Pawn(Piece):
    def __init__(self):
        super().__init__()
    def piece_char(self):
        return 'P'
    def update_legal_moves(self, board, pi_rank, pi_file, prev_move_rank, prev_move_file, in_check, checkers, prev_double_move, white_king_rank, white_king_file, black_king_rank, black_king_file, black_vision, white_vision):
        king_rank = white_king_rank
        king_file = white_king_file
        #check if double check
        if(checkers != None and len(checkers) > 1):
            for rank in range(8):
                for file in range(8):
                    self.legal_moves[rank][file] = False
            return
        for rank in range(8):
            for file in range(8):
                self.legal_moves[rank][file] = False
        if(pi_rank != 1):
            moved = True
        else:
            moved = False
        for rank in range(8):
            for file in range(8):
                piece = board[rank][file]
                if(piece != 'S'):
                    pi_exist = True
                else:
                    pi_exist = False
                if(rank == pi_rank+1 and file == pi_file):
                    if(pi_exist == False):
                        self.legal_moves[rank][file] = True
                elif(rank == pi_rank+2 and file == pi_file and moved == False):
                    if(pi_exist == False and board[rank-1][file] == 'S'):
                        self.legal_moves[rank][file] = True
                elif(rank == pi_rank+1 and (abs(file - pi_file) == 1) and pi_exist == True):
                    if(piece.get_color() != 'w'):
                        self.legal_moves[rank][file] = True
                    white_vision[rank][file] = True
                elif(rank == pi_rank+1 and pi_rank == 4 and (abs(file - pi_file) == 1) and prev_double_move == True):
                    if(prev_move_rank != None and prev_move_file != None):
                        prev_piece = board[prev_move_rank][prev_move_file]
                    else:
                        prev_piece = None
                    if(pi_exist == False and prev_piece != None and prev_piece.piece_char() == 'p' and prev_move_rank == rank - 1 and prev_move_file == file):
                        self.legal_moves[rank][file] = True
                    white_vision[rank][file] = True
                else:
                    if(rank == pi_rank+1 and (abs(file - pi_file) == 1)):
                        white_vision[rank][file] = True
        #check if in check
        if(in_check):
            moves = [[False for _ in range(8)] for _ in range(8)]
            checker = checkers[0]
            checker_rank = checker[0]
            checker_file = checker[1]
            checker_piece = board[checker_rank][checker_file]
            #check for knight check
            if(self.legal_moves[checker_rank][checker_file] == True):
                moves[checker_rank][checker_file] = True
            if(checker_piece.piece_char() == 'n'):
                if(self.legal_moves[checker_rank][checker_file] == True):
                    moves[checker_rank][checker_file] = True
            else:
                #same rank Rook, Queen
                if(checker_rank == king_rank):
                    if(checker_file < king_file):
                        file = king_file-1
                        while(file > checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file -=1
                    else:
                        file = king_file+1
                        while(file < checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file +=1
                #same file Rook, Queen
                elif(checker_file == king_file):
                    if(checker_rank < king_rank):
                        rank = king_rank-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank -=1
                    else:
                        rank = king_rank+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank +=1
                #diagonal Bishop, Queen
                else:
                    #check top left
                    if(checker_rank > king_rank and checker_file < king_file):
                        rank = king_rank+1
                        file = king_file-1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file -=1
                    #check top right
                    elif(checker_rank > king_rank and checker_file > king_file):
                        rank = king_rank+1
                        file = king_file+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file +=1
                    #check bottom left
                    elif(checker_rank < king_rank and checker_file < king_file):
                        rank = king_rank-1
                        file = king_file-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file -=1
                    #check bottom right
                    else:
                        rank = king_rank-1
                        file = king_file+1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file +=1
            self.legal_moves = moves
        #check if pinned
        if(king_rank != None):
            pinned_count = 0
            direction = 0
            for rank in range(8):
                for file in range(8):
                    piece = board[rank][file]
                    if(piece != 'S' and piece.get_color() != 'w' and piece.piece_char() != 'p' and piece.piece_char() != 'n' and piece.piece_char() != 'k'):
                        moves = piece.get_legal_moves()
                        if(moves[pi_rank][pi_file] == True):
                            #same rank: rook, queen
                            if(rank == pi_rank):
                                if(king_rank == pi_rank):
                                    if(king_file < pi_file and file > pi_file):
                                        f = pi_file-1
                                        pinned = True
                                        while(f > king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 4
                                    elif(king_file > pi_file and file < pi_file):
                                        f = pi_file+1
                                        pinned = True
                                        while(f < king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 8
                            #same file: rook, queen
                            elif(file == pi_file):
                                if(king_file == pi_file):
                                    if(king_rank < pi_rank and rank > pi_rank):
                                        f = pi_rank-1
                                        pinned = True
                                        while(f > king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 2
                                    elif(king_rank > pi_rank and rank < pi_rank):
                                        f = pi_rank+1
                                        pinned = True
                                        while(f < king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 6
                            #diag: bishop queen
                            else:
                                #top left
                                if(rank > pi_rank and file < pi_file):
                                    if(pi_rank - king_rank == king_file - pi_file):
                                        r = pi_rank-1
                                        f = pi_file+1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 1
                                #top right
                                elif(rank > pi_rank and file > pi_file):
                                    if(pi_rank - king_rank == pi_file - king_file):
                                        r = pi_rank-1
                                        f = pi_file-1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 3
                                #bottom left
                                elif(rank < pi_rank and file < pi_file):
                                    if(king_rank - pi_rank == king_file - pi_file):
                                        r = pi_rank+1
                                        f = pi_file+1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 7
                                #bottom right
                                else:
                                    if(king_rank - pi_rank == pi_file - king_file):
                                        r = pi_rank+1
                                        f = pi_file-1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 5
            if(pinned_count > 0):
                if(pinned_count > 1):
                    moves = [[False for _ in range(8)] for _ in range(8)]
                    self.legal_moves = moves
                    return
                else:
                    match(direction):
                        case 1:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 2:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank > pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 3:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 4:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file > pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 5:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 6:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank < pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 7:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 8:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file < pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
        return
    def get_legal_moves(self):
        return self.legal_moves
    def get_color(self):
        return 'w'

class White_Knight(Piece):
    def __init__(self):
        super().__init__()
    def piece_char(self):
        return 'N'
    def update_legal_moves(self, board, pi_rank, pi_file, prev_move_rank, prev_move_file, in_check, checkers, prev_double_move, white_king_rank, white_king_file, black_king_rank, black_king_file, black_vision, white_vision):
        king_rank = white_king_rank
        king_file = white_king_file
        #check if double check
        if(checkers != None and len(checkers) > 1):
            for rank in range(8):
                for file in range(8):
                    self.legal_moves[rank][file] = False
            return
        for rank in range(8):
            for file in range(8):
                self.legal_moves[rank][file] = False
        for rank in range(8):
            for file in range(8):
                if(rank == pi_rank + 2 and file == pi_file + 1):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'b'):
                        self.legal_moves[rank][file] = True
                    white_vision[rank][file] = True
                elif(rank == pi_rank + 2 and file == pi_file - 1):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'b'):
                        self.legal_moves[rank][file] = True
                    white_vision[rank][file] = True
                elif(rank == pi_rank - 2 and file == pi_file + 1):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'b'):
                        self.legal_moves[rank][file] = True
                    white_vision[rank][file] = True
                elif(rank == pi_rank - 2 and file == pi_file - 1):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'b'):
                        self.legal_moves[rank][file] = True
                    white_vision[rank][file] = True
                elif(rank == pi_rank + 1 and file == pi_file + 2):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'b'):
                        self.legal_moves[rank][file] = True
                    white_vision[rank][file] = True
                elif(rank == pi_rank + 1 and file == pi_file - 2):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'b'):
                        self.legal_moves[rank][file] = True
                    white_vision[rank][file] = True
                elif(rank == pi_rank - 1 and file == pi_file + 2):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'b'):
                        self.legal_moves[rank][file] = True
                    white_vision[rank][file] = True
                if(rank == pi_rank - 1 and file == pi_file - 2):
                    piece = board[rank][file]
                    if(piece == 'S' or piece.get_color() == 'b'):
                        self.legal_moves[rank][file] = True
                    white_vision[rank][file] = True
        #check if in check
        if(in_check):
            moves = [[False for _ in range(8)] for _ in range(8)]
            checker = checkers[0]
            checker_rank = checker[0]
            checker_file = checker[1]
            checker_piece = board[checker_rank][checker_file]
            #check for knight check
            if(self.legal_moves[checker_rank][checker_file] == True):
                moves[checker_rank][checker_file] = True
            if(checker_piece.piece_char() == 'n'):
                if(self.legal_moves[checker_rank][checker_file] == True):
                    moves[checker_rank][checker_file] = True
            else:
                #same rank Rook, Queen
                if(checker_rank == king_rank):
                    if(checker_file < king_file):
                        file = king_file-1
                        while(file > checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file -=1
                    else:
                        file = king_file+1
                        while(file < checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file +=1
                #same file Rook, Queen
                elif(checker_file == king_file):
                    if(checker_rank < king_rank):
                        rank = king_rank-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank -=1
                    else:
                        rank = king_rank+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank +=1
                #diagonal Bishop, Queen
                else:
                    #check top left
                    if(checker_rank > king_rank and checker_file < king_file):
                        rank = king_rank+1
                        file = king_file-1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file -=1
                    #check top right
                    elif(checker_rank > king_rank and checker_file > king_file):
                        rank = king_rank+1
                        file = king_file+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file +=1
                    #check bottom left
                    elif(checker_rank < king_rank and checker_file < king_file):
                        rank = king_rank-1
                        file = king_file-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file -=1
                    #check bottom right
                    else:
                        rank = king_rank-1
                        file = king_file+1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file +=1
            self.legal_moves = moves
        #check if pinned
        if(king_rank != None):
            pinned_count = 0
            direction = 0
            for rank in range(8):
                for file in range(8):
                    piece = board[rank][file]
                    if(piece != 'S' and piece.get_color() != 'w' and piece.piece_char() != 'p' and piece.piece_char() != 'n' and piece.piece_char() != 'k'):
                        moves = piece.get_legal_moves()
                        if(moves[pi_rank][pi_file] == True):
                            #same rank: rook, queen
                            if(rank == pi_rank):
                                if(king_rank == pi_rank):
                                    if(king_file < pi_file and file > pi_file):
                                        f = pi_file-1
                                        pinned = True
                                        while(f > king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 4
                                    elif(king_file > pi_file and file < pi_file):
                                        f = pi_file+1
                                        pinned = True
                                        while(f < king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 8
                            #same file: rook, queen
                            elif(file == pi_file):
                                if(king_file == pi_file):
                                    if(king_rank < pi_rank and rank > pi_rank):
                                        f = pi_rank-1
                                        pinned = True
                                        while(f > king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 2
                                    elif(king_rank > pi_rank and rank < pi_rank):
                                        f = pi_rank+1
                                        pinned = True
                                        while(f < king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 6
                            #diag: bishop queen
                            else:
                                #top left
                                if(rank > pi_rank and file < pi_file):
                                    if(pi_rank - king_rank == king_file - pi_file):
                                        r = pi_rank-1
                                        f = pi_file+1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 1
                                #top right
                                elif(rank > pi_rank and file > pi_file):
                                    if(pi_rank - king_rank == pi_file - king_file):
                                        r = pi_rank-1
                                        f = pi_file-1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 3
                                #bottom left
                                elif(rank < pi_rank and file < pi_file):
                                    if(king_rank - pi_rank == king_file - pi_file):
                                        r = pi_rank+1
                                        f = pi_file+1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 7
                                #bottom right
                                else:
                                    if(king_rank - pi_rank == pi_file - king_file):
                                        r = pi_rank+1
                                        f = pi_file-1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 5
            if(pinned_count > 0):
                if(pinned_count > 1):
                    moves = [[False for _ in range(8)] for _ in range(8)]
                    self.legal_moves = moves
                    return
                else:
                    match(direction):
                        case 1:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 2:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank > pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 3:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 4:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file > pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 5:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 6:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank < pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 7:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 8:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file < pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
        return
    def get_legal_moves(self):
        return self.legal_moves
    def get_color(self):
        return 'w'

class White_Bishop(Piece):
    def __init__(self):
        super().__init__()
    def piece_char(self):
        return 'B'
    def update_legal_moves(self, board, pi_rank, pi_file, prev_move_rank, prev_move_file, in_check, checkers, prev_double_move, white_king_rank, white_king_file, black_king_rank, black_king_file, black_vision, white_vision):
        king_rank = white_king_rank
        king_file = white_king_file
        #check if double check
        if(checkers != None and len(checkers) > 1):
            for rank in range(8):
                for file in range(8):
                    self.legal_moves[rank][file] = False
            return
        for rank in range(8):
            for file in range(8):
                self.legal_moves[rank][file] = False
        #check top right
        rank = pi_rank+1
        file = pi_file+1
        while(rank < 8 and file < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank += 1
            file += 1
        #check bottom left
        rank = pi_rank - 1
        file = pi_file - 1
        while(rank >= 0 and file >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank -= 1
            file -= 1
        #check bottom right
        rank = pi_rank - 1
        file = pi_file + 1
        while(rank >= 0 and file < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank -= 1
            file += 1
        #check top left
        rank = pi_rank + 1
        file = pi_file - 1
        while(rank < 8 and file >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank += 1
            file -= 1
        #check if in check
        if(in_check):
            moves = [[False for _ in range(8)] for _ in range(8)]
            checker = checkers[0]
            checker_rank = checker[0]
            checker_file = checker[1]
            checker_piece = board[checker_rank][checker_file]
            #check for knight check
            if(self.legal_moves[checker_rank][checker_file] == True):
                moves[checker_rank][checker_file] = True
            if(checker_piece.piece_char() == 'n'):
                if(self.legal_moves[checker_rank][checker_file] == True):
                    moves[checker_rank][checker_file] = True
            else:
                #same rank Rook, Queen
                if(checker_rank == king_rank):
                    if(checker_file < king_file):
                        file = king_file-1
                        while(file > checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file -=1
                    else:
                        file = king_file+1
                        while(file < checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file +=1
                #same file Rook, Queen
                elif(checker_file == king_file):
                    if(checker_rank < king_rank):
                        rank = king_rank-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank -=1
                    else:
                        rank = king_rank+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank +=1
                #diagonal Bishop, Queen
                else:
                    #check top left
                    if(checker_rank > king_rank and checker_file < king_file):
                        rank = king_rank+1
                        file = king_file-1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file -=1
                    #check top right
                    elif(checker_rank > king_rank and checker_file > king_file):
                        rank = king_rank+1
                        file = king_file+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file +=1
                    #check bottom left
                    elif(checker_rank < king_rank and checker_file < king_file):
                        rank = king_rank-1
                        file = king_file-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file -=1
                    #check bottom right
                    else:
                        rank = king_rank-1
                        file = king_file+1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file +=1
            self.legal_moves = moves
        #check if pinned
        if(king_rank != None):
            pinned_count = 0
            direction = 0
            for rank in range(8):
                for file in range(8):
                    piece = board[rank][file]
                    if(piece != 'S' and piece.get_color() != 'w' and piece.piece_char() != 'p' and piece.piece_char() != 'n' and piece.piece_char() != 'k'):
                        moves = piece.get_legal_moves()
                        if(moves[pi_rank][pi_file] == True):
                            #same rank: rook, queen
                            if(rank == pi_rank):
                                if(king_rank == pi_rank):
                                    if(king_file < pi_file and file > pi_file):
                                        f = pi_file-1
                                        pinned = True
                                        while(f > king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 4
                                    elif(king_file > pi_file and file < pi_file):
                                        f = pi_file+1
                                        pinned = True
                                        while(f < king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 8
                            #same file: rook, queen
                            elif(file == pi_file):
                                if(king_file == pi_file):
                                    if(king_rank < pi_rank and rank > pi_rank):
                                        f = pi_rank-1
                                        pinned = True
                                        while(f > king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 2
                                    elif(king_rank > pi_rank and rank < pi_rank):
                                        f = pi_rank+1
                                        pinned = True
                                        while(f < king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 6
                            #diag: bishop queen
                            else:
                                #top left
                                if(rank > pi_rank and file < pi_file):
                                    if(pi_rank - king_rank == king_file - pi_file):
                                        r = pi_rank-1
                                        f = pi_file+1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 1
                                #top right
                                elif(rank > pi_rank and file > pi_file):
                                    if(pi_rank - king_rank == pi_file - king_file):
                                        r = pi_rank-1
                                        f = pi_file-1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 3
                                #bottom left
                                elif(rank < pi_rank and file < pi_file):
                                    if(king_rank - pi_rank == king_file - pi_file):
                                        r = pi_rank+1
                                        f = pi_file+1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 7
                                #bottom right
                                else:
                                    if(king_rank - pi_rank == pi_file - king_file):
                                        r = pi_rank+1
                                        f = pi_file-1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 5
            if(pinned_count > 0):
                if(pinned_count > 1):
                    moves = [[False for _ in range(8)] for _ in range(8)]
                    self.legal_moves = moves
                    return
                else:
                    match(direction):
                        case 1:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 2:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank > pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 3:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 4:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file > pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 5:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 6:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank < pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 7:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 8:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file < pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
        return
    def get_legal_moves(self):
        return self.legal_moves
    def get_color(self):
        return 'w'

class White_Rook(Piece):
    def __init__(self):
        super().__init__()
        self.has_moved = False
        self.starting_rank = None
        self.starting_file = None
    def piece_char(self):
        return 'R'
    def update_legal_moves(self, board, pi_rank, pi_file, prev_move_rank, prev_move_file, in_check, checkers, prev_double_move, white_king_rank, white_king_file, black_king_rank, black_king_file, black_vision, white_vision):
        king_rank = white_king_rank
        king_file = white_king_file
        #check if double check
        if(checkers != None and len(checkers) > 1):
            for rank in range(8):
                for file in range(8):
                    self.legal_moves[rank][file] = False
            return
        if(self.starting_rank == None):
            self.starting_rank = pi_rank
            self.starting_file = pi_file
        if(self.starting_rank != pi_rank or self.starting_file != pi_file):
            self.has_moved = True
        for rank in range(8):
            for file in range(8):
                self.legal_moves[rank][file] = False
        #check top
        rank = pi_rank + 1
        file = pi_file
        while(rank < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank += 1
        #check bottom
        rank = pi_rank - 1
        file = pi_file
        while(rank >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank -= 1
        #check left
        rank = pi_rank
        file = pi_file - 1
        while(file >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            file -= 1
        #check right
        rank = pi_rank
        file = pi_file + 1
        while(file < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            file += 1
        #check if in check
        if(in_check):
            moves = [[False for _ in range(8)] for _ in range(8)]
            checker = checkers[0]
            checker_rank = checker[0]
            checker_file = checker[1]
            checker_piece = board[checker_rank][checker_file]
            #check for knight check
            if(self.legal_moves[checker_rank][checker_file] == True):
                moves[checker_rank][checker_file] = True
            if(checker_piece.piece_char() == 'n'):
                if(self.legal_moves[checker_rank][checker_file] == True):
                    moves[checker_rank][checker_file] = True
            else:
                #same rank Rook, Queen
                if(checker_rank == king_rank):
                    if(checker_file < king_file):
                        file = king_file-1
                        while(file > checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file -=1
                    else:
                        file = king_file+1
                        while(file < checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file +=1
                #same file Rook, Queen
                elif(checker_file == king_file):
                    if(checker_rank < king_rank):
                        rank = king_rank-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank -=1
                    else:
                        rank = king_rank+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank +=1
                #diagonal Bishop, Queen
                else:
                    #check top left
                    if(checker_rank > king_rank and checker_file < king_file):
                        rank = king_rank+1
                        file = king_file-1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file -=1
                    #check top right
                    elif(checker_rank > king_rank and checker_file > king_file):
                        rank = king_rank+1
                        file = king_file+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file +=1
                    #check bottom left
                    elif(checker_rank < king_rank and checker_file < king_file):
                        rank = king_rank-1
                        file = king_file-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file -=1
                    #check bottom right
                    else:
                        rank = king_rank-1
                        file = king_file+1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file +=1
            self.legal_moves = moves
        #check if pinned
        if(king_rank != None):
            pinned_count = 0
            direction = 0
            for rank in range(8):
                for file in range(8):
                    piece = board[rank][file]
                    if(piece != 'S' and piece.get_color() != 'w' and piece.piece_char() != 'p' and piece.piece_char() != 'n' and piece.piece_char() != 'k'):
                        moves = piece.get_legal_moves()
                        if(moves[pi_rank][pi_file] == True):
                            #same rank: rook, queen
                            if(rank == pi_rank):
                                if(king_rank == pi_rank):
                                    if(king_file < pi_file and file > pi_file):
                                        f = pi_file-1
                                        pinned = True
                                        while(f > king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 4
                                    elif(king_file > pi_file and file < pi_file):
                                        f = pi_file+1
                                        pinned = True
                                        while(f < king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 8
                            #same file: rook, queen
                            elif(file == pi_file):
                                if(king_file == pi_file):
                                    if(king_rank < pi_rank and rank > pi_rank):
                                        f = pi_rank-1
                                        pinned = True
                                        while(f > king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 2
                                    elif(king_rank > pi_rank and rank < pi_rank):
                                        f = pi_rank+1
                                        pinned = True
                                        while(f < king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 6
                            #diag: bishop queen
                            else:
                                #top left
                                if(rank > pi_rank and file < pi_file):
                                    if(pi_rank - king_rank == king_file - pi_file):
                                        r = pi_rank-1
                                        f = pi_file+1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 1
                                #top right
                                elif(rank > pi_rank and file > pi_file):
                                    if(pi_rank - king_rank == pi_file - king_file):
                                        r = pi_rank-1
                                        f = pi_file-1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 3
                                #bottom left
                                elif(rank < pi_rank and file < pi_file):
                                    if(king_rank - pi_rank == king_file - pi_file):
                                        r = pi_rank+1
                                        f = pi_file+1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 7
                                #bottom right
                                else:
                                    if(king_rank - pi_rank == pi_file - king_file):
                                        r = pi_rank+1
                                        f = pi_file-1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 5
            if(pinned_count > 0):
                if(pinned_count > 1):
                    moves = [[False for _ in range(8)] for _ in range(8)]
                    self.legal_moves = moves
                    return
                else:
                    match(direction):
                        case 1:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 2:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank > pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 3:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 4:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file > pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 5:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 6:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank < pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 7:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 8:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file < pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
        return
    def get_legal_moves(self):
        return self.legal_moves
    def get_color(self):
        return 'w'

class White_Queen(Piece):
    def __init__(self):
        super().__init__()
    def piece_char(self):
        return 'Q'
    def update_legal_moves(self, board, pi_rank, pi_file, prev_move_rank, prev_move_file, in_check, checkers, prev_double_move, white_king_rank, white_king_file, black_king_rank, black_king_file, black_vision, white_vision):
        king_rank = white_king_rank
        king_file = white_king_file
        #check if double check
        if(checkers != None and len(checkers) > 1):
            for rank in range(8):
                for file in range(8):
                    self.legal_moves[rank][file] = False
            return
        for rank in range(8):
            for file in range(8):
                self.legal_moves[rank][file] = False
        #check top
        rank = pi_rank + 1
        file = pi_file
        while(rank < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank += 1
        #check bottom
        rank = pi_rank - 1
        file = pi_file
        while(rank >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank -= 1
        #check left
        rank = pi_rank
        file = pi_file - 1
        while(file >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            file -= 1
        #check right
        rank = pi_rank
        file = pi_file + 1
        while(file < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            file += 1
        #check top right
        rank = pi_rank+1
        file = pi_file+1
        while(rank < 8 and file < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank += 1
            file += 1
        #check bottom left
        rank = pi_rank - 1
        file = pi_file - 1
        while(rank >= 0 and file >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank -= 1
            file -= 1
        #check bottom right
        rank = pi_rank - 1
        file = pi_file + 1
        while(rank >= 0 and file < 8):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank -= 1
            file += 1
        #check top left
        rank = pi_rank + 1
        file = pi_file - 1
        while(rank < 8 and file >= 0):
            piece = board[rank][file]
            if(piece == 'S' or piece.get_color() == 'b'):
                self.legal_moves[rank][file] = True
            white_vision[rank][file] = True
            if(piece != 'S'):
                break
            rank += 1
            file -= 1
        #check if in check
        if(in_check):
            moves = [[False for _ in range(8)] for _ in range(8)]
            checker = checkers[0]
            checker_rank = checker[0]
            checker_file = checker[1]
            checker_piece = board[checker_rank][checker_file]
            #check for knight check
            if(self.legal_moves[checker_rank][checker_file] == True):
                moves[checker_rank][checker_file] = True
            if(checker_piece.piece_char() == 'n'):
                if(self.legal_moves[checker_rank][checker_file] == True):
                    moves[checker_rank][checker_file] = True
            else:
                #same rank Rook, Queen
                if(checker_rank == king_rank):
                    if(checker_file < king_file):
                        file = king_file-1
                        while(file > checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file -=1
                    else:
                        file = king_file+1
                        while(file < checker_file):
                            if(self.legal_moves[king_rank][file] == True):
                                moves[king_rank][file] = True
                            file +=1
                #same file Rook, Queen
                elif(checker_file == king_file):
                    if(checker_rank < king_rank):
                        rank = king_rank-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank -=1
                    else:
                        rank = king_rank+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][king_file] == True):
                                moves[rank][king_file] = True
                            rank +=1
                #diagonal Bishop, Queen
                else:
                    #check top left
                    if(checker_rank > king_rank and checker_file < king_file):
                        rank = king_rank+1
                        file = king_file-1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                print("True")
                                moves[rank][file] = True
                            rank += 1
                            file -=1
                    #check top right
                    elif(checker_rank > king_rank and checker_file > king_file):
                        rank = king_rank+1
                        file = king_file+1
                        while(rank < checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank += 1
                            file +=1
                    #check bottom left
                    elif(checker_rank < king_rank and checker_file < king_file):
                        rank = king_rank-1
                        file = king_file-1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file -=1
                    #check bottom right
                    else:
                        rank = king_rank-1
                        file = king_file+1
                        while(rank > checker_rank):
                            if(self.legal_moves[rank][file] == True):
                                moves[rank][file] = True
                            rank -= 1
                            file +=1
            self.legal_moves = moves
        #check if pinned
        if(king_rank != None):
            pinned_count = 0
            direction = 0
            for rank in range(8):
                for file in range(8):
                    piece = board[rank][file]
                    if(piece != 'S' and piece.get_color() != 'w' and piece.piece_char() != 'p' and piece.piece_char() != 'n' and piece.piece_char() != 'k'):
                        moves = piece.get_legal_moves()
                        if(moves[pi_rank][pi_file] == True):
                            #same rank: rook, queen
                            if(rank == pi_rank):
                                if(king_rank == pi_rank):
                                    if(king_file < pi_file and file > pi_file):
                                        f = pi_file-1
                                        pinned = True
                                        while(f > king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 4
                                    elif(king_file > pi_file and file < pi_file):
                                        f = pi_file+1
                                        pinned = True
                                        while(f < king_file):
                                            Piece = board[rank][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 8
                            #same file: rook, queen
                            elif(file == pi_file):
                                if(king_file == pi_file):
                                    if(king_rank < pi_rank and rank > pi_rank):
                                        f = pi_rank-1
                                        pinned = True
                                        while(f > king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f -= 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 2
                                    elif(king_rank > pi_rank and rank < pi_rank):
                                        f = pi_rank+1
                                        pinned = True
                                        while(f < king_rank):
                                            Piece = board[f][file]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f += 1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 6
                            #diag: bishop queen
                            else:
                                #top left
                                if(rank > pi_rank and file < pi_file):
                                    if(pi_rank - king_rank == king_file - pi_file):
                                        r = pi_rank-1
                                        f = pi_file+1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 1
                                #top right
                                elif(rank > pi_rank and file > pi_file):
                                    if(pi_rank - king_rank == pi_file - king_file):
                                        r = pi_rank-1
                                        f = pi_file-1
                                        pinned = True
                                        while(r > king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r-=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 3
                                #bottom left
                                elif(rank < pi_rank and file < pi_file):
                                    if(king_rank - pi_rank == king_file - pi_file):
                                        r = pi_rank+1
                                        f = pi_file+1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f+=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 7
                                #bottom right
                                else:
                                    if(king_rank - pi_rank == pi_file - king_file):
                                        r = pi_rank+1
                                        f = pi_file-1
                                        pinned = True
                                        while(r < king_rank):
                                            Piece = board[r][f]
                                            if(Piece != 'S'):
                                                pinned = False
                                                break
                                            f-=1
                                            r+=1
                                        if(pinned):
                                            pinned_count += 1
                                            direction = 5
            if(pinned_count > 0):
                if(pinned_count > 1):
                    moves = [[False for _ in range(8)] for _ in range(8)]
                    self.legal_moves = moves
                    return
                else:
                    match(direction):
                        case 1:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 2:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank > pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 3:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank > pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 4:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file > pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 5:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file > pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 6:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file == pi_file and rank < pi_rank):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 7:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and file < pi_file and rank < pi_rank and (abs(file-pi_file) == abs(rank-pi_rank))):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
                        case 8:
                            for rank in range(8):
                                for file in range(8):
                                    if(self.legal_moves[rank][file] == True and rank == pi_rank and file < pi_file):
                                        self.legal_moves[rank][file] = True
                                    else:
                                        self.legal_moves[rank][file] = False
        return
    def get_legal_moves(self):
        return self.legal_moves
    def get_color(self):
        return 'w'

class White_King(Piece):
    def __init__(self):
        super().__init__()
        self.has_moved = False
        self.starting_rank = None
        self.starting_file = None
    def piece_char(self):
        return 'K'
    def update_legal_moves(self, board, pi_rank, pi_file, prev_move_rank, prev_move_file, in_check, checkers, prev_double_move, white_king_rank, white_king_file, black_king_rank, black_king_file, black_vision, white_vision):
        if(self.starting_rank == None):
            self.starting_rank = pi_rank
            self.starting_file = pi_file
        if(self.has_moved == False and (self.starting_rank != pi_rank or self.starting_file != pi_file or self.starting_rank != 0 or self.starting_file != 4)):
            self.has_moved = True
        for rank in range(8):
            for file in range(8):
                self.legal_moves[rank][file] = False
        #check for x-ray vision
        if(in_check):
            for checker in checkers:
                checker_rank = checker[0]
                checker_file = checker[1]
                piece = board[checker_rank][checker_file]
                if(piece.piece_char() != 'p' and piece.piece_char() != 'n'):
                    #same rank
                    if(checker_rank == pi_rank):
                        if(checker_file < pi_file):
                            if(pi_file < 7):
                                black_vision[pi_rank][pi_file+1] = True
                            if(pi_file-1 != checker_file):
                                black_vision[pi_rank][pi_file-1] = True
                        else:
                            if(pi_file > 0):
                                black_vision[pi_rank][pi_file-1] = True
                            if(pi_file + 1 != checker_file):
                                black_vision[pi_rank][pi_file+1] = True
                    #same file
                    elif(checker_file == pi_file):
                        if(checker_rank < pi_rank):
                            if(pi_rank < 7):
                                black_vision[pi_rank+1][pi_file] = True
                            if(pi_rank-1 != checker_rank):
                                black_vision[pi_rank-1][pi_file] = True
                        else:
                            if(pi_rank > 0):
                                black_vision[pi_rank-1][pi_file] = True
                            if(pi_rank + 1 != checker_rank):
                                black_vision[pi_rank+1][pi_file] = True
                    #top left
                    elif(checker_rank > pi_rank and checker_file < pi_file):
                        if(pi_rank > 0 and pi_file < 7):
                            black_vision[pi_rank-1][pi_file+1] = True
                        if(pi_rank+1 != checker_rank and pi_file-1 != checker_file):
                            black_vision[pi_rank+1][pi_file-1] = True
                    #top right
                    elif(checker_rank > pi_rank and checker_file > pi_file):
                        if(pi_rank > 0 and pi_file > 0):
                            black_vision[pi_rank-1][pi_file-1] = True
                        if(pi_rank+1 != checker_rank and pi_file+1 != checker_file):
                            black_vision[pi_rank+1][pi_file+1] = True
                    #bottom left
                    elif(checker_rank < pi_rank and checker_file < pi_file):
                        if(pi_rank < 7 and pi_file < 7):
                            black_vision[pi_rank+1][pi_file+1] = True
                        if(pi_rank-1 != checker_rank and pi_file-1 != checker_file):
                            black_vision[pi_rank-1][pi_file-1] = True
                    #bottom right
                    else:
                        if(pi_rank < 7 and pi_file > 0):
                            black_vision[pi_rank+1][pi_file-1] = True
                        if(pi_rank-1 != checker_rank and pi_file+1 != checker_file):
                            black_vision[pi_rank-1][pi_file+1] = True
        #check legal moves
        for rank in range(8):
            for file in range(8):
                piece = board[rank][file]
                if(abs(rank - pi_rank) <= 1 and abs(file - pi_file) <= 1):
                    if((piece == 'S' or piece.get_color() == 'b') and black_vision[rank][file] == False):
                        self.legal_moves[rank][file] = True
                    white_vision[rank][file] = True
        #check castling
        if(self.has_moved == False):
            right_rook = board[pi_rank][pi_file + 3]
            left_rook = board[pi_rank][pi_file - 4]
            if(right_rook != 'S' and right_rook.piece_char() == 'R' and right_rook.has_moved == False and board[pi_rank][pi_file + 1] == 'S' and board[pi_rank][pi_file + 2] == 'S' and black_vision[pi_rank][pi_file + 1] == False and black_vision[pi_rank][pi_file + 2] == False):
                self.legal_moves[pi_rank][pi_file + 2] = True
            if(left_rook != 'S' and left_rook.piece_char() == 'R' and left_rook.has_moved == False and board[pi_rank][pi_file - 1] == 'S' and board[pi_rank][pi_file - 2] == 'S' and board[pi_rank][pi_file - 3] == 'S' and black_vision[pi_rank][pi_file - 1] == False and black_vision[pi_rank][pi_file - 2] == False and black_vision[pi_rank][pi_file - 3] == False):
                self.legal_moves[pi_rank][pi_file - 2] = True
        return
    def get_legal_moves(self):
        return self.legal_moves
    def get_color(self):
        return 'w'

def main():
    config = pyglet.gl.Config(vsync=True)
    model = Model()
    view = View(model, width=800, height=600, caption="Chess")
    controller = Controller(model, view)

    # Schedule the update method of the controller to be called every 1/240 seconds
    pyglet.clock.schedule_interval(controller.update, 1 / 240)

    # Push event handlers to the view's window
    view.push_handlers(controller)

    pyglet.app.run()

if __name__ == "__main__":
    main()