from player_database import Player_Database

# this very simple python script connects the interface to the python script that interacts with the database

db = Player_Database()


class Binder:
    def login(self, username, password):
        return db.login(username, password)

    def register(self, username, password):
        return db.register(username, password)

    def get_won_games(self, username):
        return username + " has already won " + str(db.get_won_games(username)) + " games."

    def increase_score(self, username):
        db.increase_score(username)

    def close(self):
        db.close_db()
