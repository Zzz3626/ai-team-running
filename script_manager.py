class ScriptManager:
    def __init__(self):
        self.scriptlist = [
            {"id": "1", "name": "失落的遗迹", "player_count": "3-5", "difficulty": "简单"},
            {"id": "2", "name": "诡秘古宅", "player_count": "4-6", "difficulty": "中等"},
            {"id": "3", "name": "永夜杀机", "player_count": "3-4", "difficulty": "困难"}
        ]

    def get_script_list(self):
        return self.scriptlist

    def get_script_by_id(self, script_id):
        return next((script for script in self.scriptlist if script["id"] == script_id), None)

    def format_script_list(self):
        script_display = "可选剧本列表：\n"
        for script in self.scriptlist:
            script_display += f"{script['id']}. {script['name']} (人数:{script['player_count']}, 难度:{script['difficulty']})\n"
        return script_display
