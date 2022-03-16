import discord
import random
from discord.ext import commands
from discord_components import Button, ButtonStyle
from database.WWII_db import *

weapon_set = [
    "medicine",
    "sniper",
    "attacker"
]

uniform_set = [
    "uniform_red",
    "uniform_blue"
]

teleport_set =[
    "teleport_blue",
    "teleport_red"
]


class WWII(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        run_cmd_channel = self.bot.get_channel(927796274676260944)
        member = interaction.author
        ww2_btn = interaction.component.custom_id
        check = event_exists(member.id)
        player = players_exists(member.id)
        code = random.randint(9, 99999)
        order_number = f'order{code}'
        message = None

        if ww2_btn == 'event_register':
            if check == 0:
                steam_id = player[3]
                event_register(member.name, member.id, steam_id)
                message = '🎉 ลงทุเบียนเข้าร่วมกิจกรรม เรียบร้อยแล้ว'
            elif check == 1:
                message = '⚠ Error : คุณได้ลงทะเบียนไว้แล้ว'
        elif ww2_btn == 'event_a':
            team = 'RED'
            select = select_team(member.id, team)
            message = f'คุณได้เลือกเข้าร่วมทีม **{team}** จำนวนสมาชิกทั้งหมด **{select}**'
        elif ww2_btn == 'event_b':
            team = 'BLUE'
            select = select_team(member.id, team)
            message = f'คุณได้เลือกเข้าร่วมทีม **{team}** จำนวนสมาชิกทั้งหมด **{select}**'

        elif ww2_btn in weapon_set:
            status = teleport_status(member.id)
            weapon = weapon_status(member.id)
            if status == 1:
                message = '⚠ Error : ระบบไม่สามารถจัดส่งอาวุธให้คุณได้ เนื่องจากคุณอยู่นอกพื้นที่กิจกรรม'
            elif status is False:
                message = "⚠ Error : โปรดตรวจสอบให้แน่ใจว่าได้ลงทะเบียนเข้าร่วมกิจกรรมเรียบร้อยแล้ว"
            elif weapon == 0:
                message = "⚠ Error : ขออภัยสิทธิ์ในการใช้งานคำสั่งของคุณหมดแล้ว"
            else:
                package = f'{ww2_btn}_set'
                update_weapon_status(member.id)
                message = f'โปรดรอสักครู่ ระบบกำลังจัดส่ง **{package.upper()}** ไปให้คุณ'
                add_to_cart(player[2], player[1], player[3], order_number, package)
                await run_cmd_channel.send('!checkout {}'.format(order_number))

        elif ww2_btn in uniform_set:
            status = teleport_status(member.id)
            uniform = uniform_status(member.id)
            team = team_check(member.id)
            if status == 1:
                message = '⚠ Error : ระบบไม่สามารถจัดส่งเครื่องแต่งกายให้คุณได้ เนื่องจากคุณอยู่นอกพื้นที่กิจกรรม'
            elif status is False:
                message = "⚠ Error : โปรดตรวจสอบให้แน่ใจว่าได้ลงทะเบียนเข้าร่วมกิจกรรมเรียบร้อยแล้ว"
            elif uniform == 0:
                message = "⚠ Error : ขออภัยสิทธิ์ในการใช้งานคำสั่งของคุณหมดแล้ว"
            else:
                if ww2_btn == 'uniform_red':
                    if team == 'BLUE':
                        message = f'⚠ ขออภัยคุณ คุณต้องเลือกชุดของทีม {team}'
                    else:
                        package = f'{ww2_btn}'
                        update_uniform_status(member.id)
                        message = f'โปรดรอสักครู่ ระบบกำลังจัดส่ง **{package.upper()}** ไปให้คุณ'
                        add_to_cart(player[2], player[1], player[3], order_number, package)
                        await run_cmd_channel.send('!checkout {}'.format(order_number))

                elif ww2_btn == "uniform_blue":
                    if team == 'RED':
                        message = f'⚠ ขออภัยคุณ คุณต้องเลือกชุดของทีม {team}'
                    else:
                        package = f'{ww2_btn}'
                        update_uniform_status(member.id)
                        message = f'โปรดรอสักครู่ ระบบกำลังจัดส่ง **{package.upper()}** ไปให้คุณ'
                        add_to_cart(player[2], player[1], player[3], order_number, package)
                        await run_cmd_channel.send('!checkout {}'.format(order_number))

        elif ww2_btn in teleport_set:
            teleport = teleport_status(member.id)
            team = team_check(member.id)
            if teleport == 0:
                message = '⚠ Error : สิทธิ์ในการใช้งานคำสั่งของคุณหมดแล้ว'
            elif teleport == 1:
                if ww2_btn == 'teleport_blue':
                    if team == 'BLUE':
                        message = f'{member.name} ระบบกำลังนำคุณไปฐานที่มั่นของคุณ'
                        update_teleport(member.id)
                        teleport = f'.set #teleport 589340.438 -127331.359 2079.710 {player[3]}'
                        await run_cmd_channel.send(teleport)
                        await run_cmd_channel.send(f'.location #Location {player[3]} true')
                    elif team == "RED":
                        message = "⚠ Error, คำสั่งไม่ทำงานเนื่องจากคุณอยู่ทีม {}".format(team)
                elif ww2_btn == 'teleport_red':
                    if team == 'RED':
                        message = f'{member.name} ระบบกำลังนำคุณไปฐานที่มั่นของคุณ'
                        update_teleport(member.id)
                        teleport = f'.set #teleport 584233.000 -84023.656 1666.030 {player[3]}'
                        await run_cmd_channel.send(teleport)
                        await run_cmd_channel.send(f'.location #Location {player[3]} true')
                    elif team == "BLUE":
                        message = "⚠ Error, คำสั่งไม่ทำงานเนื่องจากคุณอยู่ทีม {}".format(team)

        await interaction.respond(content=message)

    @commands.command(name='ww2')
    async def ww2_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/the_battle.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='REGISTER', emoji='📝', custom_id='event_register'),
                    Button(style=ButtonStyle.red, label='RED TEAM', emoji='🛡', custom_id='event_a'),
                    Button(style=ButtonStyle.blue, label='BLUE TEAM', emoji='⚔', custom_id='event_b')
                ]
            ]
        )
        await ctx.message.delete()

    @commands.command(name='weapon_set')
    async def weapon_set_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/the_battle_l2.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='MEDICINE', emoji='💉', custom_id='medicine'),
                    Button(style=ButtonStyle.blue, label='SNIPER', emoji='🏹', custom_id='sniper'),
                    Button(style=ButtonStyle.red, label='ATTACKER', emoji='⚔', custom_id='attacker')
                ]
            ]
        )
        await ctx.message.delete()

    @commands.command(name='uniform_set')
    async def uniform_set(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/the_battle_l.png'),
            components=[
                [
                    Button(style=ButtonStyle.red, label='RED UNIFORM', emoji='👔', custom_id='uniform_red'),
                    Button(style=ButtonStyle.blue, label='BLUE UNIFORM', emoji='👕', custom_id='uniform_blue')
                ]
            ]
        )
        await ctx.message.delete()

    @commands.command(name='teleport')
    async def teleport_command(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/teleport_event.png'),
            components=[
                [
                    Button(style=ButtonStyle.blue, label='GOTO TEAM BLUE', emoji='✈', custom_id='teleport_blue'),
                    Button(style=ButtonStyle.red, label='GOTO TEAM RED', emoji='✈', custom_id='teleport_red')
                ]
            ]
        )
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(WWII(bot))

