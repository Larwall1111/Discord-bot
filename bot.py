import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} aktif!")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Sebep belirtilmedi"):
    await member.kick(reason=reason)
    await ctx.send(f"✅ {member.mention} sunucudan atıldı. Sebep: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Sebep belirtilmedi"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} banlandı. Sebep: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, kullanici):
    banned = [entry async for entry in ctx.guild.bans()]
    for ban_entry in banned:
        if ban_entry.user.name == kullanici:
            await ctx.guild.unban(ban_entry.user)
            await ctx.send(f"✅ {kullanici} banı kaldırıldı.")
            return
    await ctx.send("Kullanıcı bulunamadı.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason="Sebep belirtilmedi"):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False, speak=False)
    await member.add_roles(role)
    await ctx.send(f"🔇 {member.mention} susturuldu. Sebep: {reason}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send(f"🔊 {member.mention} susturması kaldırıldı.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, miktar: int):
    await ctx.channel.purge(limit=miktar + 1)
    await ctx.send(f"🗑️ {miktar} mesaj silindi.", delete_after=3)

uyarilar = {}

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, sebep="Sebep belirtilmedi"):
    uid = str(member.id)
    if uid not in uyarilar:
        uyarilar[uid] = []
    uyarilar[uid].append(sebep)
    sayi = len(uyarilar[uid])
    await ctx.send(f"⚠️ {member.mention} uyarıldı ({sayi}. uyarı). Sebep: {sebep}")

@bot.command()
async def uyari(ctx, member: discord.Member):
    uid = str(member.id)
    liste = uyarilar.get(uid, [])
    if not liste:
        await ctx.send(f"{member.mention} hiç uyarı almamış.")
    else:
        mesaj = "\n".join([f"{i+1}. {u}" for i, u in enumerate(liste)])
        await ctx.send(f"⚠️ {member.mention} uyarıları:\n{mesaj}")

bot.run(os.environ["TOKEN"])
