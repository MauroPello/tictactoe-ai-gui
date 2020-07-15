import math

# dictionary to translate from binary to Xs and Os
signs = {
    0: "O",
    1: "X"
}


class Player:
    def __init__(self, sign, username, password):
        self.sign = sign
        self.username = username
        self.password = password

    # figuring out the best move for the current player by using the minimax algorithm
    def best_move(self, game_board):
        best_score = -math.inf
        move = (0, 0)
        for x in range(3):
            for y in range(3):
                if game_board.grid[x][y] == " ":
                    game_board.grid[x][y] = signs.get(self.sign)
                    score = self.minimax(game_board, 0, False)
                    game_board.grid[x][y] = " "
                    if score > best_score:
                        best_score = score
                        move = (x, y)
        return move

    # minimax algorithm used to figure out the absolute best move based on the current state of the game
    def minimax(self, game_board, depth, is_maximizing):
        this_player_win = game_board.check_game_end(signs.get(self.sign))
        other_player_win = game_board.check_game_end(signs.get(1 - self.sign))
        if this_player_win:
            return 10
        elif other_player_win:
            return -10
        elif game_board.check_tie():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for x in range(3):
                for y in range(3):
                    if game_board.grid[x][y] == " ":
                        game_board.grid[x][y] = signs.get(self.sign)
                        score = self.minimax(game_board, depth + 1, False)
                        game_board.grid[x][y] = " "
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = math.inf
            for x in range(3):
                for y in range(3):
                    if game_board.grid[x][y] == " ":
                        game_board.grid[x][y] = signs.get(1 - self.sign)
                        score = self.minimax(game_board, depth + 1, True)
                        game_board.grid[x][y] = " "
                        best_score = min(best_score, score)
            return best_score


class GameBoard:
    def __init__(self):
        self.grid = [[" ", " ", " "],
                     [" ", " ", " "],
                     [" ", " ", " "]]
        pass

    # check if cell is available if it is take it
    def check_cell(self, x, y, player_sign):
        if self.grid[x][y] == "X" or self.grid[x][y] == "O":
            return True
        else:
            self.grid[x][y] = player_sign
            return False

    # check if the game ended with a tie
    def check_tie(self):
        tie = True
        for x in range(3):
            for y in range(3):
                if self.grid[x][y] == "X" or self.grid[x][y] == "O":
                    tie and True
                else:
                    tie = False
        return tie

    # check if X or O player won the game
    def check_game_end(self, player_sign):
        # x axis
        for x in range(3):
            if self.grid[x][0] == player_sign and self.grid[x][1] == player_sign and self.grid[x][2] == player_sign:
                return True

        # y axis
        for y in range(3):
            if self.grid[0][y] == player_sign and self.grid[1][y] == player_sign and self.grid[2][y] == player_sign:
                return True

        # negative oblique
        if self.grid[0][0] == player_sign and self.grid[1][1] == player_sign and self.grid[2][2] == player_sign:
            return True

        # positive oblique
        if self.grid[2][0] == player_sign and self.grid[1][1] == player_sign and self.grid[0][2] == player_sign:
            return True

        return False

