import random

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config

db = read_db_config()


def player_info(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('SELECT * FROM scum_players WHERE DISCORD_ID = %s', (discord_id,))
        row = cur.fetchall()
        while row is not None:
            for x in row:
                return x
    except Error as e:
        print(e)


def update_coins(discord_id, coins):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_players SET COINS = %s WHERE DISCORD_ID = %s', (coins, discord_id,))
        conn.commit()
        cur.execute('SELECT COINS FROM scum_players WHERE DISCORD_ID=%s', (discord_id,))
        row = cur.fetchone()
        while row is not None:
            res = list(row)
            return res[0]
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


def update_gift(discord_id):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('UPDATE scum_players SET GIFT = 0 WHERE DISCORD_ID=%s', (discord_id,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()


gift_list = [
    10, 20000, 30000, 40000, 50000, 6000, 7000, 800, 900, 100, 10010, 10020, 10030, 14000, 15000, 1600, 17000, 1800,
    190, 200,
    1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000,
    19000, 20000,
]


class DiscordServerEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        git_btn = interaction.component.custom_id
        lenght = len(gift_list)
        gift_random = random.randint(0, lenght - 1)
        gift = gift_list[gift_random]
        message = None
        if git_btn == 'get_free_gift':
            if player_info(member.id)[13] == 1:
                coins = player_info(member.id)[5]
                tatol = coins + gift
                coins_update = update_coins(member.id, tatol)
                message = 'โปรดรอสักครู่ คุณจะได้รับข้อความแจ้งเตือนผลการสุ่มรางวัลจากระบบ {}'.format(coins_update)
                await interaction.respond(content=message)
            else:
                await interaction.respond(content='สิทธิ์ในการรับของขวัญของคุณหมดแล้ว')

    @commands.command(name='free_gift')
    async def free_gift_commands(self, ctx):
        await ctx.send(
            file=discord.File('./img/gift_l.png'),
            components=[
                Button(style=ButtonStyle.gray, label='GET YOUR GIFT', emoji='🎁', custom_id='get_free_gift')
            ]
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(DiscordServerEvent(bot))
