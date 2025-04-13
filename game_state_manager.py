#游戏状态管理
import json

class GameStateManager:
    def __init__(self, save_file=None):
        self.state = {
            "player_name": "Hero",
            "player_stats": {"hp": 100, "max_hp": 100, "mp": 50, "max_mp": 50},
            "player_inventory": ["", ""],
            "player_location": {"map_id": "world", "x": 0, "y": 0},
            "current_map_data": None, # Will hold data for map drawing
            "current_turn": 0,
            "current_quest": None,
            "npc_states": {}, # {"npc_id": {"location": ..., "attitude": ...}}
            "world_time": "Day 1, Morning",
            "last_description": "",
            "last_image_prompt": "",
            "last_options": []
        }
        if save_file:
            self.load_state(save_file)
        print("Game State Initialized.")

    def get_state(self, key=None):
        if key:
            return self.state.get(key)
        return self.state

    def update_state(self, key, value):
        # Consider adding validation here
        self.state[key] = value
        print(f"Game State Updated: {key} = {value}")

    def get_player_location(self):
        return self.state['player_location']['x'], self.state['player_location']['y']

    def set_player_location(self, x, y, map_id=None):
        self.state['player_location']['x'] = x
        self.state['player_location']['y'] = y
        if map_id:
            self.state['player_location']['map_id'] = map_id
        print(f"Player location updated to ({x}, {y}) on map '{self.state['player_location']['map_id']}'")


    def add_to_inventory(self, item):
        self.state["player_inventory"].append(item)
        print(f"Item added to inventory: {item}")

    def save_state(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=4, ensure_ascii=False)
        print(f"Game State saved to {filepath}")

    def load_state(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.state = json.load(f)
            print(f"Game State loaded from {filepath}")
        except FileNotFoundError:
            print(f"Save file not found: {filepath}. Starting new game state.")
        except json.JSONDecodeError:
             print(f"Error decoding save file: {filepath}. Starting new game state.")


