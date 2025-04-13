#主进程

from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
from script_manager import ScriptManager  # 添加新的导入

# 注册插件
@register(name="Ai Team Running", description="Ai Team Running", version="0.1", author="Zzz3262")
class MyPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.game_state = None
        self.current_state = "idle"  # 可能的状态：idle, creating_characters
        self.player_list = []  # 存储报名玩家的QQ号
        self.script_manager = ScriptManager()  # 初始化脚本管理器

    # 异步初始化
    async def initialize(self):
        pass

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 这里的 event 即为 PersonNormalMessageReceived 的对象
        qq_number = ctx.event.launcher_id  # 获取发送者的QQ号
        if msg == "跑团":  # 开始跑团
            # 回复跑团主页面（创建新的跑团，存档列表，以及使用介绍）
            ctx.add_return("reply", ["输入新跑团或加载存档指令"])
            ctx.prevent_default()
        
        if msg == "新跑团":


            ctx.prevent_default()


        if msg == "加载存档":        
            
            ctx.prevent_default()  # 阻止该事件默认行为（向接口获取回复）

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        # 获取消息内容和发送者QQ号
        msg = ctx.event.text_message  
        sender_qq = ctx.event.sender_id 

        # 处理"跑团"命令 - 显示主菜单
        if msg == "跑团":
            ctx.add_return("reply", ["输入新跑团或加载存档指令"])
            ctx.prevent_default()
            
        # 处理"新跑团"命令 - 进入剧本选择阶段
        if msg == "新跑团":
            self.current_state = "selecting_script"  # 更新状态为选择剧本
            script_display = self.script_manager.format_script_list()  # 获取剧本列表
            ctx.add_return("reply", [script_display])
            ctx.prevent_default()

        # 处理剧本选择 - 当状态为selecting_script且收到数字时
        if self.current_state == "selecting_script" and msg.isdigit():
            script_number = msg
            selected_script = self.script_manager.get_script_by_id(script_number)
            if selected_script:
                self.current_state = "creating_characters"  # 更新状态为创建角色
                self.player_list = []  # 初始化玩家列表
                ctx.add_return("reply", [f"已选择剧本：{selected_script['name']}\n已进入角色创建阶段，请输入'报名'参加跑团"])
            else:
                ctx.add_return("reply", ["无效的剧本编号，请重新选择"])
            ctx.prevent_default()

        # 处理玩家报名 - 当状态为creating_characters时
        if msg == "报名" and self.current_state == "creating_characters":
            if sender_qq not in self.player_list:  # 检查是否重复报名
                self.player_list.append(sender_qq)  # 添加玩家到列表
                await ctx.send_private_message(sender_qq, "Hello，欢迎参加跑团！请开始创建你的角色。")
                ctx.add_return("reply", [f"玩家 {sender_qq} 已报名成功！"])
            else:
                ctx.add_return("reply", ["你已经报名过了！"])
            ctx.prevent_default()

        # 处理准备开始 - 当状态为creating_characters时
        if msg == "准备" and self.current_state == "creating_characters":
            if len(self.player_list) > 0:  # 检查是否有玩家报名
                self.current_state = "game_started"  # 更新状态为游戏开始
                ctx.add_return("reply", ["所有玩家已准备就绪，游戏开始！"])
            else:
                ctx.add_return("reply", ["还没有玩家报名，无法开始游戏！"])
            ctx.prevent_default()

        if msg == "加载存档":        
            ctx.add_return("reply", ["{}/n".format(filelist)]) #回复已有的存档列表
            ctx.prevent_default()  # 阻止该事件默认行为（向接口获取回复）

    # 插件卸载时触发
    def __del__(self):
        pass