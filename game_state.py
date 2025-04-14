from enum import Enum

class GameStatus(Enum):
    IDLE = "idle"
    SELECTING_SCRIPT = "selecting_script"
    CREATING_CHARACTERS = "creating_characters"
    GAME_STARTED = "game_started"
    PAUSED = "paused"

class GameState:
    def __init__(self):
        self.status = GameStatus.IDLE
        self.current_script = None
        self.player_list = []
        self.round_number = 0
        self.current_player_index = 0

    def set_status(self, status):
        if isinstance(status, GameStatus):
            self.status = status
            return True
        return False

    def add_player(self, player_id):
        if player_id not in self.player_list:
            self.player_list.append(player_id)
            return True
        return False

    def remove_player(self, player_id):
        if player_id in self.player_list:
            self.player_list.remove(player_id)
            return True
        return False

    def get_current_player(self):
        if not self.player_list:
            return None
        return self.player_list[self.current_player_index]

    def next_round(self):
        self.round_number += 1
        self.current_player_index = 0

    def next_player(self):
        if not self.player_list:
            return None
        self.current_player_index = (self.current_player_index + 1) % len(self.player_list)
        return self.get_current_player()
