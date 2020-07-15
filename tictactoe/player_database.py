import sqlite3

# database class that interacts with the players database

class Player_Database():
    # connecting the database
    def __init__(self):
        self.connection = sqlite3.connect("player.db")
        self.cursor = self.connection.cursor()

    # closing the connection
    def close_db(self):
        self.connection.close()

    # increases the score of a player by using its name
    def increase_score(self, nickname):
        self.cursor.execute("SELECT wins FROM players WHERE nickname = ?", (nickname,))
        wins = int(self.cursor.fetchone()[0])
        wins += 1
        with self.connection:
            self.cursor.execute("UPDATE players SET wins = ? WHERE nickname = ?", (wins, nickname))

    # player login, checks if the account exists and if the password is correct
    def login(self, username, password):
        self.cursor.execute("SELECT * FROM players WHERE nickname = ?", (username,))
        if self.cursor.fetchone() is None:
            return False
        else:
            self.cursor.execute("SELECT password FROM players WHERE nickname = ?", (username,))
            user_password = self.cursor.fetchone()[0]
            if password == user_password:
                return True
            else:
                return False

    # register player, checks if the player doesn't exist and in that case saves password and username in the database
    def register(self, username, password):
        self.cursor.execute("SELECT * FROM players WHERE nickname = ?", (username,))
        if self.cursor.fetchone() is None:
            with self.connection:
                self.cursor.execute("INSERT INTO players VALUES (?, ?, 0)", (username, password))
            return True
        else:
            return False

    # returns the amount of games won by username
    def get_won_games(self, nickname):
        self.cursor.execute("SELECT wins FROM players WHERE nickname = ?", (nickname, ))
        return self.cursor.fetchone()[0]
