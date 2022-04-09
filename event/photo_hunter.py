import asyncio

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from database.Event_db import *
from database.Bank_db import plus_coins, minus_coins


class PhotoHunterEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        member = interaction.author
        btn = interaction.component.custom_id
        btn_list = photo_hunter_code()
        check = players(member.id)
        winner_channel = interaction.guild.get_channel(914043582564954114)
        event_log = interaction.guild.get_channel(962272375179739148)  # in dev channel use 962272375179739148;
        if check != 1:
            await interaction.respond(content="ไม่พบข้อมูลของคุณในระบบ")
        else:
            player = player_info(member.id)
            permission = player[17]
            if permission == 0:
                await interaction.respond(content=f"{member.mention} : คุณใช้สิทธิ์ในการตอบคำถามจำนวน 5 ครั้งจนหมดแล้ว")

            if btn in btn_list:
                if photho_hunter_status(btn) != 1:
                    await interaction.respond(content=f"{member.mention} : ขออภัยด้วยมีผู้ชนะของกิจกรรมนี้ไปแล้ว")
                    return

                else:
                    player_photo_hunter_update(member.id, permission - 1)
                    await interaction.respond(content=f"{member.mention}, กรุณากรอกคำตอบของคุณ ภายใน 10 วินาที")

                    def check(res):
                        return res.author == interaction.author and res.channel.id == interaction.channel.id

                    try:
                        msg = await self.bot.wait_for('message', check=check, timeout=10)
                        if msg.content == btn:
                            photo_hunter_update_status(btn)
                            mission_win = get_coin_and_exp(btn)
                            embed = discord.Embed(
                                title="ผู้ชนะรางวัลอีเว้นเฉพาะกิจประจำสัปดาห์นี้",
                                color=discord.Colour.green()
                            )
                            embed.set_thumbnail(url=member.avatar_url)
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            embed.set_image(url=mission_win[2])
                            embed.add_field(name="ผู้ชนะกิจกรรม", value=member.mention, inline=False)
                            embed.add_field(name="รางวัลที่ได้รับ", value="```cs\n${:,d}\n```".format(mission_win[0]))
                            embed.add_field(name="ค่าประสบการณ์ที่ได้รับ",
                                            value="```cs\n{}\n```".format(mission_win[1]))

                            await winner_channel.send(embed=embed)
                            await interaction.channel.send(
                                f"{member.mention} : "
                                f"ยินดีด้วย คำตอบของคุณเป็นคำตอบที่ถูกต้อง "
                                f"ระบบกำลังนำจ่ายรางวัลและค่าประสบการณ์ให้กับคุณ โปรดรอข้อความจากระบบตอบกลับ",
                                delete_after=10
                            )
                            mission = get_coin_and_exp(btn)
                            coins = player[5] + mission[0]
                            exps = player[7] + mission[1]
                            exp = exp_update(member.id, exps)
                            con = plus_coins(member.id, mission[0])
                            y_int = isinstance(exp, int)

                            if y_int is True:
                                award = "${:,d}".format(mission[0])
                                coin = "${:,d}".format(coins)
                                await discord.DMChannel.send(
                                    member,
                                    f'คุณได้รับรางวัลจำนวน {award} และ ค่าประสบการณ์จำนวน {mission[1]}exp \n'
                                    f'\nจำนวนเงินปัจจุบันของคุณคือ {coin}'
                                    f'\nค่าประสบการณ์ปัจจุบันของคุณคือ {exps}exp'
                                )
                            else:
                                award = "${:,d}".format(mission[0])
                                coin = "${:,d}".format(coins)
                                await discord.DMChannel.send(
                                    member,
                                    f'คุณได้รับรางวัลจำนวน {award} และ ค่าประสบการณ์จำนวน {mission[1]}exp \n'
                                    f'\nจำนวนเงินปัจจุบันของคุณคือ {coin}'
                                    f'\nค่าประสบการณ์ปัจจุบันของคุณคือ {exps}exp\n' +
                                    exp
                                )
                            await msg.delete()
                        elif msg.content != btn:
                            await interaction.channel.send(f'{member.mention} : คำตอบของคุณไม่ถูกต้อง',
                                                           delete_after=10)
                    except asyncio.TimeoutError:
                        await interaction.channel.send(f'{member.mention} : คุณตอบคำถามช้าเกินไป กรุณาลองใหม่อีกครั้ง',
                                                       delete_after=10)
            if btn == "hunter_reset":
                player_coins = "${:,d}".format(player_info(member.id)[5])
                fine = player_info(member.id)[5] // 100
                coin = "${:,d}".format(fine)
                total = "${:,d}".format(player_info(member.id)[5] - fine)
                if fine == 0:
                    await interaction.respond(
                        content="คุณมียอดเงินไม่เพียงพอสำหรับใช้ในการปรับสิทธิ์การใช้งานในครั้งนี้"
                    )
                elif fine != 0:
                    embed = discord.Embed(
                        title=f"ใบเสนอราคาค่าบริการปรับสิทธิ์ : {player_info(member.id)[1]}",
                        color=discord.Colour.red()
                    )
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_author(name=member.display_name, icon_url=member.avatar_url)
                    embed.add_field(name="ค่าปรับ", value=f"```cs\n{coin}\n```", inline=False)
                    embed.add_field(name="คุณยังมีสิทธิ์ใช้งานคงเหลือ",
                                    value=f"```cs\n{player_info(member.id)[17]}\n```", inline=False)
                    embed.add_field(name="ยอดเงินปัจจุบัน", value=f"```cs\n{player_coins}\n```")
                    embed.add_field(name="ยอดเงินหลังหักบัญชี", value=f"```cs\n{total}\n```")
                    await interaction.respond(
                        embed=embed,
                        components=[
                            [
                                Button(style=ButtonStyle.red, label='YES, I NEED RESET', emoji="💵",
                                       custom_id="pay_for_reset"),
                                Button(style=ButtonStyle.green, label="NO, I DON'T NEED RESET", emoji="🚫",
                                       custom_id="cancle_for_reset")
                            ]
                        ]
                    )

            if btn == "pay_for_reset":
                check = reset_photo_hunter(member.id)
                if check != 0:
                    await interaction.respond(content='ระบบทำการรายปรับสิทธิ์ให้คุณไม่สำเร็จ')
                    return
                elif check == 0:
                    await interaction.respond(content="ระบบได้ทำการปรับสิทธิ์การใช้งานของคุณเรียบร้อยแล้ว")
                    player_coins = "${:,d}".format(player_info(member.id)[5])
                    fine = player_info(member.id)[5] // 100
                    coin = "${:,d}".format(fine)
                    after = minus_coins(member.id, fine)
                    after_coins = "${:,d}".format(after)
                    await event_log.send(
                        f"**Statement ของ {member.mention}**\n"
                        f"```cs\n"
                        f"Title : 'รายการหักค่าปรับสิทธิ์การใช้งาน Event Photo Hunter'\n"
                        f"Fee Money : {coin}\n"
                        f"Bank Account : '{player_info(member.id)[1]}'\n"
                        f"Bank Balance Before : {player_coins}\n"
                        f"Bank Balance After : {after_coins}\n"
                        f"Status : 🟢 Successfully"
                        f"\n```"
                    )
            if btn == "cancle_for_reset":
                await interaction.edit_origin(
                    content=f'คุณได้ทำการยกเลิกคำสั่งเป็นที่เรียบร้อยแล้วครับ',
                    components=[]
                )

    @commands.command(name='photo_hunter')
    async def photo_hunter(self, ctx, number):
        check = photo_count(number)
        if check == 1:
            photo = photo_hunter(number)
            embed = discord.Embed(
                title="EVENT PHOTHO HUNTER (อีเว้นเฉพาะกิจ)",
                # description="**คำสั่ง** : ให้ผู้เล่นตามหาที่อยู่ของภาพและจดจำตัวเลขหรือข้อความที่อยู่ในวงสีแดง"
                #             "เมื่อได้คำตอบแล้วให้ผู้เล่นกดปุ่มสีฟ้า SEND YOUR ANSWER ระบบจะให้ผู้เล่นใส่คำตอบและ"
                #             "จะตรวจสอบว่าข้อความหรือตัวเลขที่กรอกถูกต้องหรือไม่"
            )
            embed.set_image(url=photo[4])
            embed.add_field(
                name="คำอธิบาย",
                value="```cs\n"
                      "ให้ผู้เล่นตามหาที่อยู่ของภาพและจดจำตัวเลขหรือข้อความที่อยู่ในวงสีแดง"
                      "เมื่อได้คำตอบแล้วให้ผู้เล่นกดปุ่มสีฟ้า SEND YOUR ANSWER ระบบจะให้ผู้เล่นใส่คำตอบ "
                      "และจะตรวจสอบว่าข้อความหรือตัวเลขที่กรอกถูกต้องหรือไม่\n```", inline=False)
            embed.add_field(
                name="คำเตือน",
                value="```cs\n"
                      "ผู้เล่นจะได้รับสิทธิ์ในการกดปุ่มตอบคำถามเพียง 5 ครั้งเท่านั้น "
                      "ดังนั้นหากไม่มั่นใจอย่ากดตอบคำถามเป็นอันขาด ผู้ชนะจะมีเพียงหนึ่งเดียวเท่านั้น"
                      "\n```", inline=False)
            embed.add_field(name='รางวัลกิจกรรม', value="```cs\n${:,d}\n```".format(photo[2]))
            embed.add_field(name='ค่าประสบการณ์', value=f"```cs\n🎖{photo[3]}\n```")
            await ctx.send(
                # file=discord.File('./img/photo/photo_hunter.png'),
                embed=embed,
                components=[
                    [
                        Button(style=ButtonStyle.blue, label='SEND YOUR ANSWER', emoji='🧾', custom_id=f"{number}"),
                        Button(style=ButtonStyle.red, label='RESET YOUR PERMISSION', emoji='⏱',
                               custom_id="hunter_reset")
                    ]
                ]
            )
            await ctx.message.delete()
        elif check == 0:
            await ctx.reply(f'ไม่พบ Photo Hunter รหัส {number} ในฐานข้อมูล', mention_author=False)
            await ctx.message.delete()

    @photo_hunter.error
    async def photo_hunter_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('Missing a required argument : {}'.format(error.param), mention_author=False)
