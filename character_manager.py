class Character:
    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name
        self.system_attributes = {}    # 系统属性，游戏中不可修改
        self.player_attributes = {}    # 玩家属性，游戏中可修改
        self.status = "creating"       # 状态：creating, playing, deleted

    def initialize_attributes(self, script_attributes):
        """根据剧本初始化角色属性"""
        self.system_attributes = script_attributes.get("system_attributes", {}).copy()
        self.player_attributes = script_attributes.get("player_attributes", {}).copy()

    def get_attribute(self, attr_name, attr_type="system"):
        """获取指定类型的属性值"""
        if attr_type == "system":
            return self.system_attributes.get(attr_name)
        return self.player_attributes.get(attr_name)

    def set_attribute(self, attr_name, value, attr_type="system"):
        """设置指定类型的属性值"""
        if self.status == "playing" and attr_type == "system":
            return False
        if attr_type == "system":
            self.system_attributes[attr_name] = value
        else:
            self.player_attributes[attr_name] = value
        return True

class CharacterManager:
    def __init__(self):
        self.characters = {}  # 使用玩家ID作为键存储角色

    def create_character(self, player_id, name, script_attributes):
        """创建新角色并初始化属性"""
        if player_id not in self.characters:
            character = Character(player_id, name)
            character.initialize_attributes(script_attributes)
            self.characters[player_id] = character
            return True
        return False

    def get_character(self, player_id):
        return self.characters.get(player_id)

    def update_attributes(self, player_id, attributes):
        if player_id in self.characters:
            self.characters[player_id].attributes.update(attributes)
            return True
        return False

    def set_character_status(self, player_id, status):
        if player_id in self.characters:
            self.characters[player_id].status = status
            return True
        return False

    def delete_character(self, player_id):
        """删除角色"""
        if player_id in self.characters:
            self.characters[player_id].status = "deleted"
            return True
        return False

    def edit_player_attribute(self, player_id, attr_name, value):
        """编辑玩家属性（任何状态都可以）"""
        if player_id in self.characters:
            return self.characters[player_id].set_attribute(attr_name, value, "player")
        return False
