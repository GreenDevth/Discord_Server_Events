import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from database.Bank_db import plus_coins, minus_coins
from database.Players import exp_update, players_info, get_lates_player


class ManageAccounting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addexp')
    @commands.has_permissions(manage_roles=True)
    async def addexp_command(self, ctx, member: discord.Member, number: int):
        exp = exp_update(member.id, number)
        y_int = isinstance(exp, int)
        await ctx.reply(f'อัพเดทค่าประสบการณ์ให้กับ {member.display_name} จำนวน {number} เป็นที่เรียบร้อย',
                        mention_author=False)
        if y_int is True:
            await discord.DMChannel.send(member, f'คุณได้รับค่าประสบการณ์จำนวน {number} :'
                                                 f' ค่าประสบการณ์ปัจจุบันของคุณคือ {exp}')
        else:
            await discord.DMChannel.send(member, exp)

    @addexp_command.error
    async def addexp_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Your commands mission argument, Please verify again.', mention_author=False)
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('Your Role are can not used this commands.')

    @commands.command(name='addcoins')
    @commands.has_permissions(manage_roles=True)
    async def addcoins_command(self, ctx, member: discord.Member, number: int):
        coins = plus_coins(member.id, number)
        await ctx.reply(f'เติมเงินให้กับ {member.display_name} จำนวน {number} เป็นที่เรียบร้อย', mention_author=False)
        await discord.DMChannel.send(member, f'ระบบได้เติมเงินให้คุณจำนวน {number} ยอดเงินคงเหลือของคุณคือ {coins}')

    @addcoins_command.error
    async def addcoins_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Your commands mission argument, Please verify again.', mention_author=False)
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('Your Role are can not used this commands.')

    @commands.command(name='removecoins')
    @commands.has_permissions(manage_roles=True)
    async def removecoins_commands(self, ctx, member: discord.Member, number: int):
        message = None
        player = players_info(member.id)
        coin = player[5]
        if number <= coin:
            coins = minus_coins(member.id, number)
            player = players_info(member.id)
            message = f'ระบบได้หักเงินจำนวน {number} จากบัญชีของ {player[1]} ยอดคงเหลือคือ {player[5]}'
        elif coin < number:
            message = f'ยอดเงินในบัญชีของ {player[1]} มีไม่พอหรับหักค่าปรับ ยอดเงิน ของ {player[1]} คือ {player[5]}'
        await ctx.reply(message, mention_author=False)
        await discord.DMChannel.send(member, f'ระบบได้หักเงินจำนวน '
                                             f'{number} จากบัญชีของคุณ : ยอดคงเหลือของคุณคือ {player[5]}')

    @removecoins_commands.error
    async def removecoins_commands_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Your commands mission argument, Please verify again.', mention_author=False)
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('Your Role are can not used this commands.')

    @commands.command(name="last_player")
    async def last_player_command(self, ctx):
        player = get_lates_player()

        def get_ign():
            if player[12] is None:
                msg = "ยังไม่ได้ระบุชื่อตัวละคร"
                return msg.strip()
            else:
                return player[12]

        await ctx.reply(
            "```css\n"
            f"PLAYERS_ID : {player[0]}\n"
            f"DISCORD_NAME : '{player[1]}'\n"
            f"IGN : '{get_ign()}'\n"
            f"DISCORD_ID : {player[2]}\n"
            f"STEAM_ID : {player[3]}\n"
            f"GUILD_ID : {player[4]}\n"
            f"COINS : {player[5]}\n"
            f"LEVEL : {player[6]}\n"
            f"EXP : {player[7]}\n"
            f"STATUS : '{player[9]}'\n"
            "\n```",
            mention_author=False
        )

    @commands.command(name='famepoint')
    @commands.has_permissions(manage_roles=True)
    async def set_famepoint(self, ctx, member: discord.Member, amount: int):
        run = self.bot.get_channel(927796274676260944)
        command = "#setfamepoints"
        await ctx.reply(f'set {amount} famepont to {players_info(member.id)} successfull.')
        await run.send(f'.run {command} {amount} {players_info(member.id)[3]}')

    @set_famepoint.error
    async def set_famepoint_command(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('คุณไม่สามารถใช้งานคำสั่งนี้ได้')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument : {}'.format(error.param))

    @commands.command(name="set_fame")
    @commands.has_permissions(manage_roles=True)
    async def set_fame(self, ctx, amount: int, steam: int):
        run = self.bot.get_channel(927796274676260944)
        command = "#setfamepoints"
        await ctx.reply(f'set {amount} famepoints to {steam} successfully..')
        await run.send(f'.run {command} {amount} {steam}')

    @set_fame.error
    async def set_fame_command(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply('คุณไม่สามารถใช้งานคำสั่งนี้ได้')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument : {}'.format(error.param))

    @commands.command(name='setfamepoint_btn')
    async def set_fame_button(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/tractor.jpg'),
            components=[
                [
                    Button(style=ButtonStyle.red, label="1000 to all", emoji='📡', custom_id='to_all_1000'),
                    Button(style=ButtonStyle.green, label="1000 to all online", emoji='📡',
                           custom_id='to_all_1000_online')
                ]
            ]
        )

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        btn = interaction.component.custom_id
        btn_list = ["to_all_1000","to_all_1000_online"]
        run = self.bot.get_channel(927796274676260944)
        commandall = "#SetFamePointsToAll"
        commandallonline = "#SetFamePointsToAllOnline"
        if btn in btn_list:
            if btn == "to_all_1000_online":
                await interaction.respond(content='Set 1000 Fampoint to all online player successfull')
                await run.send(f'.run {commandallonline} 1000')
            if btn == "to_all_1000":
                await interaction.respond(content='Set 1000 Fampoint to all player successfull')
                await run.send(f'.run {commandall} 1000')


def setup(bot):
    bot.add_cog(ManageAccounting(bot))
