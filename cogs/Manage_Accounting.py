import discord
from discord.ext import commands

from database.Bank_db import plus_coins, minus_coins
from database.Players import exp_update, players_info


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


def setup(bot):
    bot.add_cog(ManageAccounting(bot))
