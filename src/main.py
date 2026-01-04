import discord
import dotenv

import datetime
import pathlib

class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.none()
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

def create_report(title: str) -> discord.Embed:
    embed = discord.Embed(title=title, timestamp=datetime.datetime.now())
    embed.set_footer(text="SecurityBOT | ErrorReport")

def create_log(title: str) -> discord.Embed:
    embed = discord.Embed(title=title, timestamp=datetime.datetime.now())
    embed.set_footer(text="SecurityBot | Action Log")

@discord.app_commands.command(name="ban", description="メンバーをBANします")
@discord.app_commands.guild_only
@discord.app_commands.default_permissions(ban_members=True)
@discord.app_commands.describe(
    target="BANするメンバー", reason="理由", delete="メッセージを削除する日数"
)
async def ban_cmd(
    interaction: discord.Interaction, target: discord.Member, reason: str, delete: int
):
    try:
        await target.ban(delete_message_days=delete, reason=reason)
    except discord.Forbidden:
        embed = create_report("BOTの権限が足りません")
        embed.add_field(
            name="対象", value=f"{target.name} (`{target.id}`)", inline=False
        )
        embed.add_field(
            name="実行者",
            value=f"{interaction.user.name} (`{interaction.user.id}`)",
            inline=False,
        )
    except Exception as e:
        embed = create_report("BANに失敗しました")
        embed.add_field(
            name="対象", value=f"{target.name} (`{target.id}`)", inline=False
        )
        embed.add_field(
            name="実行者",
            value=f"{interaction.user.name} (`{interaction.user.id}`)",
            inline=False,
        )
        embed.add_field(name="エラー", value=type(e).__name__, inline=False)
    else:
        embed = create_log("BANに成功しました")
        embed.add_field(
            name="対象", value=f"{target.name} (`{target.id}`)", inline=False
        )
        embed.add_field(
            name="実行者",
            value=f"{interaction.user.name} (`{interaction.user.id}`)",
            inline=False,
        )
        embed.add_field(name="理由", value=reason, inline=False)
    await interaction.response.send_message(embed=embed)

if __name__ == "__main__":
    client = Client()
    dotenv_path = pathlib.Path(__file__).parent.joinpath(".env")
    token = dotenv.get_key(dotenv_path, "DISCORD_TOKEN")
    client.run(token)
