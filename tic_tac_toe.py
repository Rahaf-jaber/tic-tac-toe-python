import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear") #cls for windows(nt), clear otherwise

class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""

    def choose_name(self):
        while True:
            name = input("Enter your name (letters only): ")
            if name.isalpha():
                self.name = name
                break
            print("Invalid name! please use letters only.")

    def choose_symbol(self):
        while True:
            symbol = input(f"{self.name}, choose your symbol (a single letter): ")
            if symbol.isalpha() and len(symbol) == 1:
                self.symbol = symbol
                break
            print("Invalid symbol! please choose a single letter.")


class Menu:
    def display_main_menu(self):

        while True:
            print("Welcome to my Tic Tac Toe Game!")
            print("1. Start Game")
            print("2. Quit Game")
            choice = input("Enter your choice (1 or 2): ")
            if choice == '1' or choice == '2':
                return choice
                break
            print("Invalid choice! Please choose 1 or 2.")

    def display_endgame_menu(self):
        while True:
            menu_text = """
            Game Over!
            1. Restart Game
            2. Quit Game
            Enter your choice (1 or 2):
            """
            choice = input(menu_text)
            if choice == '1' or choice == '2':
                return choice
                break
            print("Invalid choice! Please choose 1 or 2.")

class Board:
    def __init__(self):
        self.board = [str(i) for i in range(1,10)]
        # or
        # for i in range(1,10):
        #     self.board.append(str(i))#[1,2,3,4,5,6,7,8,9]

    def display_board(self):
        for i in range(0, 9, 3):
            print("|".join(self.board[i:i+3]))# [1,2,3] then [4,5,6] then [7,8,9]
            if i <6:
                print("-" *5)# no extra line

    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice-1] = symbol
            return True
        return False #if not valid

    def is_valid_move(self, choice):#helper method, "single responsipility principle: every method is responsible about specif task", help in reusability and readability
        return self.board[choice-1].isdigit() #-1 cuz it start by 1 for the user     
       
    def reset_board(self):
        self.board = [str(i) for i in range(1,10)]

class Game:
    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0

    def start_game(self):
        choice = self.menu.display_main_menu()
        if choice == '1':
            self.setup_players()
            self.play_game()

        else:
            self.quit_game()

    def setup_players(self):
        clear_screen()
        for num, player in enumerate(self.players, start=1):
            print(f"Player {num}, enter your details:")     
            player.choose_name()
            player.choose_symbol()
            print("_"*20)

    def play_game(self):#main game loop
        while True:
            self.play_turn()
            if self.check_win() or self.check_draw():#end game
                clear_screen()
                self.board.display_board()
                if self.check_win():
                    print(f"{self.players[1-self.current_player_index].name} win!")
                else:
                    print(f"No one win, It's a tie!")
                choice = self.menu.display_endgame_menu()
                if choice == '1':
                    self.restart_game()
                else:
                    self.quit_game()
                    break

    def play_turn(self):
        player = self.players[self.current_player_index] #[0] at first
        clear_screen()
        self.board.display_board()
        print(f"{player.name}'s turn ({player.symbol})")
        while True:#take correct input
            try:
                cell_choice = int(input("Choose a cell (1-9): "))
                if 1 <= cell_choice <= 9 and self.board.update_board(cell_choice, player.symbol):#check valid num + valid move
                    break
                else:
                    print("Invalid move, try again.")
            except ValueError:
                print("Please enter a number between 1 and 9.")
        #switch the player:
        self.switch_player()

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index #if player index 1, next will be player index 0(1-1)...

    def check_win(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], #rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], #columns
            [0, 4, 8], [2, 4, 6]             #diagonals
        ]

        for combo in win_combinations:
            if (self.board.board[combo[0]] == self.board.board[combo[1]] ==
                self.board.board[combo[2]]):
                return True
        return False

    def check_draw(self):#board is full + no one won
        #all check all, return true if all cells are not numbers
        return all(not cell.isdigit() for cell in self.board.board)#generator expression (loop in fly)

    def restart_game(self):
        self.board.reset_board()
        self.current_player_index = 0
        self.play_game()

    def quit_game(self):
        print("Thank you for Playing!")


game = Game()
game.start_game()


