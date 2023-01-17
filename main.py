"""A tic-tac-toe game built with Python using tkinter library
tkinter version >= 8.6 is required"""

from tkinter import Tk
import tkinter as tk
from tkinter import font
from itertools import cycle


class Player:
    """Class defining label - X or O and the color"""
    player_number = 1  # Initialize the Player with ID number 1

    def __init__(self, label: str, color: str) -> None:
        self.name: str = f'Player {Player.player_number}'
        self.label: str = label
        self.color: str = color
        Player.player_number += 1  # increment for next player's ID


class Move:
    """Create a move class. Each move represents position on board and a label (O or X)"""
    def __init__(self, row: int, col: int, label: str = '') -> None:
        self.row: int = row
        self.col: int = col
        self.label: str = label


# Default parameters, when not specified by the player(s)
DEFAULT_PLAYERS: tuple = (Player(label='X', color='blue'), Player(label='O', color='red'))
BOARD_SIZE: int = 3


class Game:
    def __init__(self, players: tuple = DEFAULT_PLAYERS, board_size: int = BOARD_SIZE):
        """Initialize the game"""
        self.players: tuple = players
        self._players: iter = cycle(players)  # create iterator which returns its value in cycle -> [a, b] -> a,b,a,b,...
        self.board_size: int = board_size  # board_size --> default = 3 --> 3x3
        self.current_player = next(self._players)  # select the first player for game
        self.winner_comb: list = []  # for all winning combinations
        self._current_moves: list = []  # current movement array
        self._has_winner: bool = False
        self._winning_combos: list = []  # winning combinations
        self._setup_board()  # start up the game
        self.score_table: dict = {players[0]: 0, players[1]: 0}


    def _setup_board(self) -> None:
        """Use Move class to create array of moves - empty at the beginning and set winning combinations"""
        self._current_moves = [[Move(row, col) for col in range(self.board_size)] for row in range(self.board_size)]
        # The above code returns [[(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)]] for 3x3
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self) -> list:
        """Return the list of winning combinations"""
        # All row-wise winning combinations
        rows = [[(move.row, move.col) for move in row] for row in self._current_moves]
        # All column-wise winning combinations:
        cols = [[row[i] for row in rows] for i in range(self.board_size)]
        # Diagonals:
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [row[i] for i, row in enumerate(reversed(cols))]
        return rows + cols + [first_diagonal, second_diagonal]  # square brackets to adjust the nested lists

    def is_move_valid(self, move: Move) -> bool:
        """Return True if the move can be executed, False if not"""
        row, col = move.row, move.col
        print(move.label, f'Label is:{self._current_moves[row][col].label}')
        if self._current_moves[row][col].label == '' and (self._has_winner is False):
            return True
        return False

    def process_move(self, move: Move) -> None:
        """Process the current move and check if this move is a win"""
        row, col = move.row, move.col  # get move coordinates
        self._current_moves[row][col].label = move.label  # assign label to the move
        move = self._current_moves[row][col]  # retrieve the correct move object
        for win_combo in self._winning_combos:
            label_set = set((self._current_moves[row][col].label for row, col in win_combo))  # set from the generator
            if len(label_set) == 1 and '' not in label_set:  # one value in set - homogenous, field not empty - move done
                self._has_winner = True
                self.winner_comb = win_combo
                self.score_table[self.current_player] += 1
                print(self.score_table[self.current_player])
                break

    def has_winner(self) -> bool:
        """Return if the game has a winner"""
        return self._has_winner

    def is_tie(self) -> bool:
        """Checks if there's a tie - all fields are taken and there was no winner"""
        all_fields_taken = all((move.label for row in self._current_moves for move in row))
        return all_fields_taken and self._has_winner is False

    def switch_player(self) -> None:
        """Simply switching the players after each move"""
        self.current_player = next(self._players)

    def reset_game(self) -> None:
        """Resetting the Move instances in _current_moves list"""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_comb = []


class TicTacToeBoard(Tk):  # inherit from TK class and create
    """Create a TicTacToe boards"""
    def __init__(self, game: Game):
        super().__init__()  # inherit from super Tk class
        self.title('Tic-Tac-Toe Game')
        self._cells: dict = {}  # initially empty, targeted to keep info about position of cells on the grid
        self._game = game  # create a game instance
        self._create_board_display()  # create the board when instantiating
        self._create_grid()  # create the grid for the board
        self._create_menu()
        self._create_scoreboard()

    def _create_board_display(self) -> None:
        """Creating top display frame - private methods"""
        display_frame = tk.Frame(master=self)  # create frame for a game status display // main window is frame's parent
        display_frame.pack(fill=tk.X)  # pack the frame on the top of the screen and make resize-compliant
        self.display = tk.Label(master=display_frame, text='Ready?', font=font.Font(size=28, weight='bold'))
        self.display.pack()  # pack label into a display_frame
        score_frame = tk.Frame(master=self)
        score_frame.pack(fill=tk.X)

    def _create_grid(self) -> None:
        """Create a game grid - private methods"""
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):  # create a board according to the given size
            self.rowconfigure(row, weight=1, minsize=75)  # size of the every cell on the grid // super class method
            self.columnconfigure(row, weight=2, minsize=75)  # size of the every cell on the grid // super class method
            for col in range(self._game.board_size):  # as given above - grid size according to given number
                # Creating buttons for O / X display:
                button = tk.Button(master=grid_frame, text='', font=font.Font(size=36, weight='bold'), fg='black',
                                   width=3, height=2, highlightbackground='lightblue')
                self._cells[button] = (row, col)  # saving the position of every button on the grid
                button.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')  # grid buttons to the grid_frame //
                # padx; pady - justification
                button.bind('<ButtonPress-1>', func=self.play)

    def _create_scoreboard(self) -> None:
        """Create a scoreboard using tk"""
        scoreboard = tk.Label(master=self, text='Score:', font=font.Font(size=20, weight='bold'))
        scoreboard.pack()
        score_frame = tk.Frame(master=self)
        score_frame.rowconfigure(1, weight=1)
        score_frame.columnconfigure(1, weight=1)
        player1_label = tk.Label(master=score_frame, text=f'{self._game.players[0].name}',
                                 font=font.Font(size=15, weight='bold'), padx=5)
        player1_label.grid(row=0, column=0)
        player2_label = tk.Label(master=score_frame, text=f'{self._game.players[1].name}',
                                 font=font.Font(size=15, weight='bold'), padx=5)
        player2_label.grid(row=0, column=1)
        self.player1_score = tk.Label(master=score_frame, text=f'{self._game.score_table[self._game.players[0]]}',
                                 font=font.Font(size=15, weight='bold'), padx=5)
        self.player1_score.grid(row=1, column=0)
        self.player2_score = tk.Label(master=score_frame, text=f'{self._game.score_table[self._game.players[1]]}',
                                 font=font.Font(size=15, weight='bold'), padx=5)
        self.player2_score.grid(row=1, column=1)
        score_frame.pack()

    def _update_score(self) -> None:
        """A method for updating the scores of both players after each round"""
        self.player1_score['text'] = f'{self._game.score_table[self._game.players[0]]}'
        self.player2_score['text'] = f'{self._game.score_table[self._game.players[1]]}'

    def _create_menu(self) -> None:
        """Create a drop down menu"""
        menu = tk.Menu(master=self)
        self.config(menu=menu)
        file_menu = tk.Menu(master=menu)
        file_menu.add_command(label='Restart', command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=quit)
        menu.add_cascade(label='File', menu=file_menu)

    def reset_board(self) -> None:
        """Clear the buttons' texts"""
        self._game.reset_game()
        self._update_display('Are You ready?')
        for button in self._cells:
            button.config(text='')  # Set new value on buttons to blank
            button.config(fg='black') # Set a label color to black
            button.config(bg='#F0F0F0')  # Set a buttons' background color to default

    def _update_button(self, clicked_btn) -> None:
        """Updating button when pressed"""
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color='black') -> None:
        """Invoked when top display needs to be updated"""
        self.display['text'] = msg
        self.display['fg'] = color

    def _highlight_cells(self) -> None:
        """Highlight winning combination"""
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_comb:
                button.config(bg='gold')

    def play(self, event) -> None:
        """Handle a player's move"""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]  # unpack button coordinates
        move = Move(row, col, self._game.current_player.label)  # create move instance
        if self._game.is_move_valid(move=move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tie():
                self._update_display(msg='Tied game!', color='red')
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player {self._game.current_player.label} won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
                self._update_score()

            else:
                self._game.switch_player()
                msg = f'{self._game.current_player.label}\'s turn!'
                self._update_display(msg)


def main():
    """Starting function"""
    game = Game()
    tictac = TicTacToeBoard(game)  # new instance of the TicTacToe
    tictac.mainloop()  #


if __name__ == '__main__':
    main()
