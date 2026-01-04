import discord
import dotenv

import pathlib

class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.none()
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)
    
    async def setup_hook(self):
        await self.tree.sync()
    
if __name__ == "__main__":
    dotenv_path = pathlib.Path(__file__).parent.joinpath(".env")
    token = dotenv.get_key(dotenv_path, "DISCORD_TOKEN")
    Client().run(token)
