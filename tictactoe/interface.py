from tkinter import *
from tkinter import messagebox
from binder import *
from library import *
import random

# initializing player1 and 2
player1 = Player(1, "Lorem", "Ipsum")
player2 = Player(0, "Dolor", "Sit")

# initializing the binder to connect the interface to the database
binder = Binder()

# initializing the game board
game_board = GameBoard()


# MainFrame: first  and main frame to be init
class Mainframe(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Tic Tac Toe")
        messagebox.showinfo(message="Welcome to Pello's Tic Tac Toe!")
        # start frame
        self.frame = PlayerOneFrame(self)
        self.frame.grid()

    # changing frame
    def change(self, frame):
        self.frame = frame(self)
        self.frame.grid()


# GenericFrame: all the other frames are children of this one which is a child of the class Frame from tkinter
class GenericFrame(Frame):
    # switching from a frame to another
    def switch_frame(self, frame):
        for widget in self.master.winfo_children():
            widget.grid_remove()
        self.master.change(frame)

    # closing the game
    def close_game(self):
        binder.close()
        self.master.destroy()


# MenuFrame: child of GenericFrame
class MenuFrame(GenericFrame):
    def __init__(self, master=None):
        # calling Frame __init__
        Frame.__init__(self, master)

        self.player_label = Label(text="Hi " + player1.username + "! Welcome Back!")
        self.player_label.grid(row=0, column=0)

        # setting player2 as AI in case player1 chooses to play against the Computer
        global player2
        player2 = Player(1 - player1.sign, "AI", "AI")

        self.computer_button = Button(text="Play against the Computer", command=lambda: self.switch_frame(GameFrame))
        self.computer_button.grid(row=1, column=0)

        self.friend_button = Button(text="Play against your friend", command=lambda: self.switch_frame(PlayerTwoFrame))
        self.friend_button.grid(row=2, column=0)


# PlayerFrame: parent of both players' login frames (they share the same login_register function)
class PlayerFrame(GenericFrame):
    # function used to log in or register and switch to the next frame
    def login_register(self, sign, username, password, function, next_frame, player_number):
        global player1
        global player2
        # players can't name themselves AI because that's the username for the Computer/CPU/AI
        if username == "AI":
            messagebox.showinfo(message="Can't use AI as username!")
            return
        # a player can only login once on the same instance of the game
        if player_number == 2 and username == player1.username:
            messagebox.showinfo(message="Player already logged in!")
            return
        # if signing in o up (depends on the function called) is successful show message, save player data,
        # display player wins and switch to next frame
        if function(username, password):
            if function == binder.login:
                messagebox.showinfo(message="Correct Password! Player logged in!")
            elif function == binder.register:
                messagebox.showinfo(message="Player successfully registered!")
            messagebox.showinfo(
                message=username + " has the " + signs.get(sign) + " sign. " + binder.get_won_games(username))
            if player_number == 1:
                player1 = Player(sign, username, password)
            elif player_number == 2:
                player2 = Player(sign, username, password)
            self.switch_frame(next_frame)
        else:
            messagebox.showinfo(message="Invalid Username or Password!")


# PlayerOneFrame: player1 signing
class PlayerOneFrame(PlayerFrame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.player_label = Label(text="Enter Player One Credentials: ")
        self.player_label.grid(row=0, column=0, columnspan=2)

        # username input
        self.username_entry = Entry(master)
        self.username_entry.grid(row=1, column=0, columnspan=2)
        self.username_entry.insert(0, "Enter username: ")

        # password input
        self.password_entry = Entry(master)
        self.password_entry.grid(row=2, column=0, columnspan=2)
        self.password_entry.insert(0, "Enter password: ")

        # being this the frame for player1 he gets to chose whether he wants to be the O or the X
        sign_choice = IntVar()
        self.o_radio = Radiobutton(master, text="O", variable=sign_choice, value=0)
        self.o_radio.grid(row=3, column=0)
        self.x_radio = Radiobutton(master, text="X", variable=sign_choice, value=1)
        self.x_radio.grid(row=3, column=1)

        # login button
        self.login_button = Button(text="Login", command=lambda: self.login_register(sign_choice.get(),
                                                                                     self.username_entry.get(),
                                                                                     self.password_entry.get(),
                                                                                     binder.login,
                                                                                     MenuFrame,
                                                                                     1))
        self.login_button.grid(row=4, column=0)

        # register button
        self.register_button = Button(text="Register", command=lambda: self.login_register(sign_choice.get(),
                                                                                           self.username_entry.get(),
                                                                                           self.password_entry.get(),
                                                                                           binder.register,
                                                                                           MenuFrame,
                                                                                           1))
        self.register_button.grid(row=4, column=1)


# PlayerTwoFrame: player2 signing
class PlayerTwoFrame(PlayerFrame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.player_label = Label(text="Enter Player Two Credentials: ", )
        self.player_label.grid(row=0, column=0, columnspan=2)

        # username input
        self.username_entry = Entry(master)
        self.username_entry.grid(row=1, column=0, columnspan=2)
        self.username_entry.insert(0, "Enter username: ")

        # password input
        self.password_entry = Entry(master)
        self.password_entry.grid(row=2, column=0, columnspan=2)
        self.password_entry.insert(0, "Enter password: ")

        # login button
        self.login_button = Button(text="Login", command=lambda: self.login_register(1 - player1.sign,
                                                                                     self.username_entry.get(),
                                                                                     self.password_entry.get(),
                                                                                     binder.login,
                                                                                     GameFrame,
                                                                                     2))
        self.login_button.grid(row=3, column=0)

        # register button
        self.register_button = Button(text="Register", command=lambda: self.login_register(1 - player1.sign,
                                                                                           self.username_entry.get(),
                                                                                           self.password_entry.get(),
                                                                                           binder.register,
                                                                                           GameFrame,
                                                                                           2))
        self.register_button.grid(row=3, column=1)


# GameFrame: the frame that contains the game itself
class GameFrame(GenericFrame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # setting the window size
        master.geometry("350x350")

        # initializing current_player and turn_count
        self.current_player = None
        self.turn_count = 1

        # randomly picking a start_player
        start_player = random.randint(0, 1)
        if start_player:
            self.current_player = player1
        else:
            self.current_player = player2

        self.turn_label = Label(text="Turn: " + str(self.turn_count))
        self.turn_label.place(x=280, y=10)

        self.current_player_label = Label(text="Current Player: " + self.current_player.username)
        self.current_player_label.place(x=20, y=10)

        # creating new canvas for the lines that make the tic-tac-toe game board
        canvas = Canvas(master, height=265, width=265, bd=0, highlightthickness=0, relief='ridge')

        # default line color
        line_color = "black"

        # get background color
        background_color = str(master["bg"]).replace("#", "")
        # if the background color is more close to black than white change line_color to "white"
        if int(background_color[0:2], 16) < 125 and \
                int(background_color[2:4], 16) < 125 and \
                int(background_color[4:6], 16) < 125:
            line_color = "white"

        # create the four lines for the tic-tac-toe game board
        canvas.create_line(0, 86, 300, 86, fill=line_color, width=3)
        canvas.create_line(0, 176, 300, 176, fill=line_color, width=3)
        canvas.create_line(86, 0, 86, 300, fill=line_color, width=3)
        canvas.create_line(176, 0, 176, 300, fill=line_color, width=3)

        # place the canvas
        canvas.place(x=40, y=60)

        # create array of buttons and fill it with clickable buttons
        self.buttons = [[self.create_button(0, 0), self.create_button(1, 0), self.create_button(2, 0)],
                        [self.create_button(0, 1), self.create_button(1, 1), self.create_button(2, 1)],
                        [self.create_button(0, 2), self.create_button(1, 2), self.create_button(2, 2)]]

        # showing changes
        self.master.update()

        # if the start player is the AI/CPU/Computer make a (the best) move
        if not start_player and player2.username == "AI":
            self.ai_move()

    # creating buttons used as clickable areas to put Xs or Os on the game board and placing them on the frame
    def create_button(self, x, y):
        tmp = Button(text="", font="Arial 32 bold", command=lambda: self.make_play(x, y), borderwidth=0)
        tmp.place(x=40 + (90 * x), y=60 + (90 * y), height=85, width=85)
        return tmp

    # making a play
    def make_play(self, x, y):
        # waiting 0.1s
        self.master.after(100)
        # check if cell is taken, if not take it, update the game state and check if the game ended in a win or a tie
        if game_board.check_cell(x, y, signs.get(self.current_player.sign)):
            messagebox.showinfo(message="Position already taken!")
        else:
            self.buttons[y][x]['text'] = signs.get(self.current_player.sign)
            self.turn_count += 1
            self.turn_label['text'] = "Turn: " + str(self.turn_count)
            self.current_player_label['text'] = "Current Player: " + self.current_player.username
            if game_board.check_game_end(signs.get(self.current_player.sign)):
                messagebox.showinfo(message=self.current_player.username + " wins this game!!!")
                db.increase_score(self.current_player.username)
                self.close_game()
            elif self.turn_count == 10:
                messagebox.showinfo(message="Game ended in a Tie!")
                self.close_game()
            else:
                # if the game has not ended change current_player to the other player
                if self.current_player == player1:
                    self.current_player = player2
                    self.current_player_label['text'] = "Current Player: " + self.current_player.username
                    # if it's AI's turn
                    if player2.username == "AI":
                        # call function to make the AI's move
                        self.ai_move()
                else:
                    self.current_player = player1
                    self.current_player_label['text'] = "Current Player: " + self.current_player.username

    # make the best possible move as an AI
    def ai_move(self):
        best_move = player2.best_move(game_board)
        self.make_play(best_move[0], best_move[1])


# starts mainframe if the main script is directly run
if __name__ == "__main__":
    app = Mainframe()
    app.mainloop()
