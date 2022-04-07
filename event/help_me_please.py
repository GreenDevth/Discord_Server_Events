import asyncio
import random
import time

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from database.Players import players_info
from event.parachutes import count_player, check_player, new_recode, players_event_info, status

teleport_list = [
    "178394.188 -145612.531 0",
    "162107.281 -145318.016 0",
    "142272.797 -148870.313 0",
    "137527.5835 -155085.5478 0",
    "132198.9122 -160118.1818 0",
    "128054.3901 -165742.8904 0",
    "122429.6814 -170479.4872 0",
    "113844.5998 -173735.8974 0",
    "117101.0101 -178472.4942 0",
    "113539.773 -182735.6378 0",
    "111602.0743 -187902.8342 0",
    "110740.8749 -192316.4812 0",
    "109556.7257 -196730.1281 0",
    "109556.7257 -200928.4752 0",
    "109664.3757 -205665.072 0",
    "107296.0773 -218367.7632 0",
    "107619.0271 -222781.4102 0",
    "109556.7257 -226118.5579 0",
    "111279.1246 -229455.7056 0",
    "114185.6726 -233654.0527 0",
    "116876.9207 -237637.1 0",
    "120859.968 -241512.4973 0",
    "124627.7154 -245280.2447 0",
    "127964.8631 -248832.6922 0",
    "133993.2589 -249370.9419 0",
    "140129.3047 -249693.8916 0",
    "144973.5513 -250555.0911 0",
    "148741.2987 -252492.7897 0",
    "154016.1451 -253031.0393 0",
    "160044.541 -253784.5888 0",
    "168333.5852 -258305.8857 0",
    "173285.4818 -261320.0836 0",
    "211285.9057 -258844.1353 0",
    "210209.4064 -250985.6908 0",
    "227433.3945 -250339.7912 0",
    "229048.1434 -246356.7439 0",
    "230662.8923 -241404.8474 0",
    "232062.3413 -235914.7011 0",
    "232923.5407 -229886.3053 0",
    "231631.7416 -224180.8592 0",
    "239274.8864 -216214.7647 0",
    "237660.1375 -208033.3704 0",
    "251977.5776 -192208.8313 0",
    "243796.1833 -170894.1459 0",
    "239948.2367 -160239.4945 0",
    "231955.2297 -151358.3756 0",
    "220187.7471 -141589.1449 0",
    "200427.2576 -139146.8372 0",
    "192212.2227 -139146.8372 0",
    "184441.2437 -137814.6694 0",
    "75083.4499 -187008.2362 0",
    "75083.4499 -198849.728 0",
    "71531.0023 -209901.7871 0",
    "67189.122 -221743.2789 0",
    "73504.5843 -230821.756 0",
    "83372.4942 -241479.0987 0",
    "98371.7172 -243057.9643 0",
    "102368.2207 -260425.4856 0",
    "107252.8361 -270194.7164 0",
    "170308.7801 -261313.5975 0",
    "199616.4724 -292841.5695 0",
    "177413.6752 -285292.6185 0",
    "228124.864 -283871.6395 0",
    "235585.0039 -279963.9472 0",
    "249794.7941 -277832.4786 0",
    "268622.7661 -247991.9192 0",
    "273951.4375 -237334.5765 0",
    "287095.4934 -219572.3388 0",
    "279990.5983 -147812.8982 0",
    "257965.4235 -149233.8772 0",
    "250505.2836 -131826.8842 0",
    "238782.2067 -128274.4367 0",
    "207520.6682 -115130.3807 0",
    "191179.4095 -119038.073 0",
    "174127.6612 -120103.8073 0",
    "146418.5703 -131826.8842 0"
]
list_lenght = len(teleport_list)

zombie_location = [
    "210721.469 -207343.313 24552.920",
    "179950.516 -223393.453 23974.830",
    "189888.609 -212709.359 25275.170",
    "204685.094 -200928.453 25405.629",
    "195649.672 -182983.828 26395.719",
    "182735.313 -170182.313 28327.549",
    "163728.953 -179034.063 30488.830",
    "147783.734 -182061.031 30506.430",
    "133321.641 -178498.172 30464.109",
    "117056.406 -172940.516 31317.369",
    "112503.977 -182772.578 30908.439"
]
zombie_lenght = len(zombie_location)


class HelpMePlease(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        event_btn = interaction.component.custom_id
        btn_list = ["event_register", "event_home", "start_event", "quantity", "event_details", "event_test_home",
                    "start_test_event", "event_option"]
        run = interaction.guild.get_channel(927796274676260944)
        location_command = self.bot.get_channel(961454973332377681)
        if event_btn in btn_list:
            btn = event_btn
            if btn == "event_register":
                check = check_player(member.id)
                if check == 0:
                    new_recode(member.id, member.name, players_info(member.id)[3], "THE LOST WILD")
                    player = count_player()
                    await interaction.edit_origin(
                        components=[
                            [
                                Button(style=ButtonStyle.green, label='REGISTER', emoji='🔐',
                                       custom_id='event_register'),
                                Button(style=ButtonStyle.red, label=f'QUANTITY : {player[0]}',
                                       emoji='📃', custom_id='quantity'),
                                Button(style=ButtonStyle.gray, label=f'EVENT DETAIL', emoji='📃',
                                       custom_id='event_details')
                            ]
                        ]
                    )
                    await interaction.channel.send(f'{member.mention}\n'
                                                   f'คุณได้ลงทะเบียนเรียบร้อยแล้ว',
                                                   delete_after=5)
                elif check != 0:
                    await interaction.respond(content="คุณได้ลงทะเบียนไว้แล้ว")

            if btn == "event_home":
                check = check_player(member.id)
                if check == 1:
                    if players_event_info(member.id)[4] == 1:
                        teleport = "2378.3066 -235506.977 0"
                        await interaction.respond(content=f"คุณ {players_info(member.id)[1]} ระบบกำลังนำคุณไปยัง Event")
                        get_location = await run.send(f'.location #Location {players_info(member.id)[3]} true')
                        await asyncio.sleep(3)
                        msg = await run.send(f".set #Teleport {teleport} {players_info(member.id)[3]}")
                        await asyncio.sleep(2)
                        await msg.delete()
                        await get_location.delete()
                    elif players_event_info(member.id) == 0:
                        await interaction.respond(content='กิจกรรมยังไม่เริ่มกรุณารอทีมงานแจ้งเตือนอีกครั้ง')
                elif check == 0:
                    await interaction.respond(content='คุณยังไม่ได้ ลงทะเบียนเข้าร่วมกิจกรรมในครั้งนี้')
            if btn == "start_event":
                check = check_player(member.id)
                if check == 1:
                    if players_event_info(member.id)[4] == 1:
                        teleport_to = random.randint(0, list_lenght - 1)
                        teleport = teleport_list[teleport_to]
                        await interaction.respond(content=f"คุณ {players_info(member.id)[1]}"
                                                          f" ระบบกำลังนำคุณไปยังจุดเริ่มต้น")
                        msg = await run.send(f".set #Teleport {teleport} {players_info(member.id)[3]}")
                        await asyncio.sleep(2)
                        await msg.delete()
                    elif players_event_info(member.id) == 0:
                        await interaction.respond(content='กิจกรรมยังไม่เริ่มกรุณารอทีมงานแจ้งเตือนอีกครั้ง')
                elif check == 0:
                    await interaction.respond(content='คุณยังไม่ได้ ลงทะเบียนเข้าร่วมกิจกรรมในครั้งนี้')

            if btn == "quantity":
                player = count_player()
                await interaction.edit_origin(
                    components=[
                        [
                            Button(style=ButtonStyle.green, label='REGISTER', emoji='🔐', custom_id='event_register'),
                            Button(style=ButtonStyle.red, label=f'QUANTITY : {player[0]}',
                                   emoji='📃', custom_id='quantity'),
                            Button(style=ButtonStyle.gray, label=f'EVENT DETAIL', emoji='📃', custom_id='event_details')
                        ]
                    ]
                )
            if btn == "event_details":
                message = "===================================\n" \
                          "=======  THE LOST WILD ป่ามรณะ ========\n\n" \
                          "**กิจกรรม ป่ามรณะ THE LOST WILD**\n" \
                          "ผู้เล่นจะถูกระบบส่งตัวกระจ่ายไปตามพื้นที่ต่าง ๆ\n" \
                          "ในรัศมี 700 ตารางเมตรจากจุดหมายที่ต้องเดินทางกลับ\n" \
                          "ผู้เล่นจะถูกปล่อยไว้โดยปราศจากเครื่องมือหรืออุปกรณ์ใด ๆ\n" \
                          "ช่วยเหลือและมีเวลาเพียง 15 นาทีก่อนวงจะเริ่มเคลื่อนที่\n" \
                          "ผู้เล่นที่กลับถึงที่หมายไม่ทันจะถูกวงฆ่าตาย\n\n" \
                          "**รางวัลสำหรับกิจกรรม**\n" \
                          "- ผู้เล่นที่สามารถลับเข้ามายังพื้นที่ที่กำหนดอย่างปลอดภัย" \
                          " รับ **$50,000** และค่าประสบการณ์ **35000exp**\n" \
                          "- ผู้เล่นทุกคนที่ลงทะเบียนและเข้าร่วมกิจกรรม" \
                          " รับเพิ่ม **$3000** และค่าประสบการณ์ **3000exp**\n\n" \
                          "กิจกรรม จะเริ่ม ~~ในวันเสาร์ที่ 9 ตั้งแต่เวลา 21:00~~ หรือ เมื่อผู้เล่นพร้อม"
                await interaction.respond(content=message)

            if btn == "event_test_home":
                teleport = "2378.3066 -235506.977 0"
                await interaction.respond(content=f"คุณ {players_info(member.id)[1]} ระบบกำลังนำคุณไปยัง Event")
                await asyncio.sleep(3)
                get_location = await run.send(f'.location #Location {players_info(member.id)[3]} true')
                msg = await run.send(f".set #Teleport {teleport} {players_info(member.id)[3]}")
                await asyncio.sleep(2)
                await msg.delete()
                await get_location.delete()

            if btn == "start_test_event":
                teleport_to = random.randint(0, list_lenght - 1)
                teleport = teleport_list[teleport_to]
                await interaction.respond(content=f"คุณ {players_info(member.id)[1]}"
                                                  f" ระบบกำลังนำคุณไปยังจุดเริ่มต้น")
                msg = await run.send(f".set #Teleport {teleport} {players_info(member.id)[3]}")
                await asyncio.sleep(2)
                await msg.delete()
            if btn == "event_option":
                await interaction.respond(content='ระบบกำลังส่งซอมบี้ไปประจำพื้นที่')
                for x in zombie_location:
                    await asyncio.sleep(1)
                    await run.send(f'.set #Teleport {x}')
                    await asyncio.sleep(15)
                    await run.send('.set #SpawnRandomZombie 10')
                    await asyncio.sleep(5)

                await interaction.channel.send('Send zomebie to event area successfull.', delete_after=5)

    @commands.command(name='register_event')
    async def register_event(self, ctx):
        player = count_player()
        await ctx.send(
            file=discord.File('./img/the_lost_wild.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='REGISTER', emoji='🔐', custom_id='event_register'),
                    Button(style=ButtonStyle.red, label=f'QUANTITY : {player[0]}', emoji='📃', custom_id='quantity'),
                    Button(style=ButtonStyle.gray, label=f'EVENT DETAIL', emoji='📃', custom_id='event_details')
                ]
            ]
        )
        await ctx.message.delete()

    @commands.command(name='help_me_please')
    async def help_me_event_commands(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/event_start.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='GOTO EVENT LOCATION', emoji='🏠', custom_id='event_home'),
                    Button(style=ButtonStyle.blue, label='TELEPORT NOW', emoji='🎉', custom_id='start_event')
                ]
            ]
        )
        await ctx.message.delete()

    @commands.command(name='start')
    async def start_event(self, ctx):
        status()
        await ctx.reply('Start Event', mention_author=False)
        await ctx.message.delete()

    @commands.command(name='test_event')
    async def test_event(self, ctx):
        await ctx.send(
            file=discord.File('./img/event/event_start.png'),
            components=[
                [
                    Button(style=ButtonStyle.green, label='GOTO EVENT LOCATION', emoji='🏠',
                           custom_id='event_test_home'),
                    Button(style=ButtonStyle.blue, label='TELEPORT NOW', emoji='🎉', custom_id='start_test_event')
                ]
            ]
        )
        await ctx.message.delete()

    @commands.command(name='final')
    async def final_place(self, ctx):
        run = self.bot.get_channel(927796274676260944)
        member = ctx.author
        steam = players_info(member.id)[3]
        teleport = "#Teleport 175201.875 -199213.156 29079.803"
        await ctx.reply('ระบบกำลังส่งคุณไปยังจุดเส้นชัย', mention_author=False)
        await run.send(f'.set {teleport} {steam}')

    @commands.command(name='event_option')
    async def send_event_option(self, ctx):
        await ctx.send(
            'Send Option',
            components=[Button(style=ButtonStyle.red, label='SEND EVENT OPTION', emoji='🧟', custom_id='event_option')]
        )
