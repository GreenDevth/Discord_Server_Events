import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

""" Connect to Database """
from mysql.connector import MySQLConnection, Error
from database.db_config import read_db_config
from database.Players import players_info

db = read_db_config()


def count_player():
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select count(*) from server_event order by event_id')
        row = cur.fetchall()
        return row[0]
    except Error as e:
        print(e)


def check_player(discord_id):
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select count(*) from server_event where discord_id=%s', (discord_id,))
        row = cur.fetchone()
        return row[0]
    except Error as e:
        print(e)


def players_event_info(discord_id):
    """ Get player information. """
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('select * from server_event where DISCORD_ID = %s', (discord_id,))
        row = cur.fetchall()
        while row is not None:
            for x in row:
                return x
        return False
    except Error as e:
        print(e)
        return None


def new_recode(discord_id, discord_name, steam_id, event_name):
    conn = None
    try:
        conn = MySQLConnection(**db)
        cur = conn.cursor()
        cur.execute('insert into server_event(discord_id, discord_name, steam_id, event_name) VALUES (%s,%s,%s,%s)',
                    (discord_id, discord_name, steam_id, event_name,))
        conn.commit()
        cur.close()
    except Error as e:
        print(e)
    finally:
        if conn.is_connected():
            conn.close()
            return False


class ParachutesEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        btn = interaction.component.custom_id

        if btn == 'parachute_event_register':
            check = check_player(member.id)
            if check == 0:
                new_recode(member.id, member.name, players_info(member.id)[3], "parachutes")
                count = count_player()[0]
                await interaction.edit_origin(
                    components=[
                        [
                            Button(style=ButtonStyle.green, label='REGISTER', emoji='📝',
                                   custom_id='parachute_event_register'),
                            Button(style=ButtonStyle.blue, label=f'PLAYER : {count}',
                                   emoji='📝', custom_id='parachute_event_count'),
                            Button(style=ButtonStyle.gray, label='EVENT DETIAL', emoji='📝',
                                   custom_id='parachute_event_detail')
                        ]
                    ]
                )

                await interaction.channel.send(f'{member.mention}\n'
                                               f'คุณได้ลงทะเบียนเรียบร้อยแล้ว',
                                               delete_after=5)
            elif check != 0:
                await interaction.respond(content="คุณได้ลงทะเบียนไว้แล้ว")

        if btn == 'parachute_event_count':
            count = count_player()[0]
            await interaction.edit_origin(
                components=[
                    [
                        Button(style=ButtonStyle.green, label='REGISTER', emoji='📝',
                               custom_id='parachute_event_register'),
                        Button(style=ButtonStyle.blue, label=f'PLAYER : {count}',
                               emoji='📝', custom_id='parachute_event_count'),
                        Button(style=ButtonStyle.gray, label='EVENT DETIAL', emoji='📝',
                               custom_id='parachute_event_detail')
                    ]
                ]
            )
        if btn == 'parachute_event_detail':
            message = "===================================\n" \
                      "======= PARACHUTES ดิ่งฟ้าท้านรก ========\n\n" \
                      "**กิจกรรม ดิ่งฟ้าท้านรก**\n" \
                      "ผู้เล่นจะได้ร่มชูชีพและจะถูกส่งไปยังความสูง 20000\n" \
                      "ฟุตจากพื้นดิน และหลังจากนั้นผู้เล่นต้องควบคุมการ\n" \
                      "ดิ่งเวหาและบังคับร่มลงในพื้นที่ ที่เตรียมไว้ให้ได้อย่างปลอดภัย\n\n" \
                      "**รางวัลสำหรับกิจกรรม**\n" \
                      "- ผู้เล่นที่สามารถลงในพื้นที่ที่กำหนดให้อย่างปลอดภัย" \
                      " รับ **$10,000** และค่าประสบการณ์ **10000exp**\n" \
                      "- ผู้เล่นทุกคนที่ลงทะเบียนและเข้าร่วมกิจกรรม" \
                      " รับเพิ่ม **$3000** และค่าประสบการณ์ **3000exp**\n\n" \
                      "กิจกรรม จะเริ่ม ในวันเสาร์ที่ 2 เวลา 21:00 เป็นต้นไป"
            await interaction.respond(content=message)
        if btn == 'goto_event':
            check = check_player(member.id)
            if check != 0:
                await interaction.respond(content="โปรดรอสักครู่ ระบบกำลังนำท่านไปยังพื้นที่จัดกิจกรรม")
                player = players_event_info(member.id)
                run_cmd_channel = self.bot.get_channel(927796274676260944)
                teleport = f'.set #teleport 350920.344 -518363.219 7632.930 {player[3]}'
                await run_cmd_channel.send(teleport)
            else:
                await interaction.respond(content="คุณไม่ได้รับสิทธิ์ในการใช้งานคำสั่งนี้")

        if btn == 'jump':
            check = check_player(member.id)
            if check != 0:
                await interaction.respond(content="โปรดรอสักครู่ ระบบกำลังส่งคุณไปยังความสูงเริ่มต้น")
                player = players_event_info(member.id)
                run_cmd_channel = self.bot.get_channel(927796274676260944)
                teleport = f'.set #teleport 344852.344 -524494.250 275480.813 {player[3]}'
                await run_cmd_channel.send(teleport)

    @commands.command(name='parachutes')
    async def parachute_command(self, ctx):
        count = count_player()[0]
        await ctx.send(
            file=discord.File('./img/event/new_event.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='REGISTER', emoji='📝', custom_id='parachute_event_register'),
                    Button(style=ButtonStyle.blue, label=f'PLAYER : {count}',
                           emoji='📝', custom_id='parachute_event_count'),
                    Button(style=ButtonStyle.gray, label='EVENT DETIAL', emoji='📝', custom_id='parachute_event_detail')
                ]
            ]
        )

    @commands.command(name='goto_event')
    async def event_teleport(self, ctx):
        await ctx.channel.send(
            file=discord.File('./img/event/teleport_event.png'),
            components=[
                [
                    Button(style=ButtonStyle.red, label="TELEPORT TO EVENT", emoji='🚌', custom_id='goto_event')
                ]
            ]
        )

    @commands.command(name='jump')
    async def event_jump(self, ctx):
        await ctx.channel.send(
            file=discord.File('./img/event/jump.png'),
            components=[
                [
                    Button(style=ButtonStyle.gray, label="START PARACHUTES", emoji='🪂', custom_id='jump')
                ]
            ]
        )
