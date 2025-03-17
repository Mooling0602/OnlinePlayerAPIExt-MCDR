import re
import online_player_api as opapi

from mcdreforged.api.all import *

builder = SimpleCommandBuilder()
psi = ServerInterface.psi()
reply_player = []


def on_load(server: PluginServerInterface, old):
    builder.register(server)

@builder.command('!!list')
def on_command_list(src: CommandSource, ctx: CommandContext):
    global reply_player
    if src.is_player:
        reply_player.append(src.player)
    psi.execute('list')

def on_info(server: PluginServerInterface, info: Info):
    match = re.match(r"There are \d+ of a max of \d+ players online:", info.content)
    if match:
        names_section = info.content[match.end():].strip()
        result = [name.strip() for name in names_section.split(",")]
        opapi.online_players = result
        if len(reply_player) > 0:
            title = "------ Online Players / 在线玩家 ------"
            for i in reply_player:
                server.tell(i, title)
                for p in result:
                    server.tell(i, f"- {p}")
                reply_player.remove(i)