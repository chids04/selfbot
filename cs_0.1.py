from tkinter import *
import io
import aiohttp
import asyncio
import discord
import pytz
from pytz import timezone
from datetime import datetime, timedelta
from discord.ext import commands, tasks
import random
import socket
import struct
import sys
import os
import requests
import threading
import re
from PIL import Image

root = Tk()
root.title("chids's selfbot")

""" with open("tokens.txt", "r") as t:
    token = t.readline() """


e = Entry(root, width=75, borderwidth = 5)
e.grid(row=0, column=0)
# e.insert(0, token)




def sb(loop):
    asyncio.set_event_loop(loop)
    token = e.get()
    
    try:

        client = commands.Bot(command_prefix="=", help_command=None, self_bot=True)

        @client.command(pass_context=True)
        async def purge(ctx,amount):
            if ctx.message.author.id == client.user.id:
                await ctx.message.delete()
                async for message in ctx.message.channel.history(limit=int(amount)).filter(lambda m: m.author == client.user).map(
                        lambda m: m):
                    try:
                        await message.delete()
                        await asyncio.sleep(0.7)
                    except:
                        pass

        @client.command(pass_context=True)
        async def av(ctx, user: discord.Member):
            await ctx.message.delete()
            if client.user.id == ctx.message.author.id:
                u = user.avatar_url
            await ctx.send(u)

        @client.command()
        async def stealpfp(ctx, user:discord.Member):
            await ctx.message.delete()
            password = "enter your password here"
            with open("pfp/Stolen.png", "wb") as f:
                r = requests.get(user.avatar_url, stream=True)
                for block in r.iter_content(1024):
                    if not block:
                        break
                    f.write(block)

                Image.open("pfp/Stolen.png").convert("RGB")
                with open("pfp/Stolen.png", "rb") as f:
                    await client.user.edit(password=password, avatar=f.read())
                
        @client.command()
        async def prayer(ctx):
            await ctx.message.delete()
            await ctx.send("Our Father in heaven, hallowed be your name, your kingdom come, your will be done,on earth as in heaven. Give us today our daily bread. Forgive us our sins as we forgive those who sin against us. Lead us not into temptation but deliver us from evil. For the kingdom, the power, and the glory are yours now and for ever. Amen.")




        @client.command()
        async def time(ctx, zone):
            await ctx.message.delete()
            if zone == "pacific".lower():
                time = timezone("US/Pacific")
                sa_time = datetime.now(time)
                await ctx.send(sa_time.strftime("%H:%M"))
            elif zone == "eastern".lower():
                time = timezone("US/Eastern")
                sa_time = datetime.now(time)
                await ctx.send(sa_time.strftime("%H:%M"))
            elif zone == "mountain".lower():
                time = timezone("US/Mountain")
                sa_time = datetime.now(time)
                await ctx.send(sa_time.strftime("%H:%M"))
            elif zone == "central".lower():
                time = timezone("US/Central")
                sa_time = datetime.now(time)
                await ctx.send(sa_time.strftime("%H:%M"))

        @client.command()
        async def ip(ctx, name):
            await ctx.message.delete()
            ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
            await ctx.send(socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))

        @client.command()
        async def destroy(ctx): # b'\xfc'
            await ctx.message.delete()
            for channel in list(ctx.guild.channels):
                try:
                    await channel.delete()
                except:
                    pass
            for user in list(ctx.guild.members):
                try:
                    await user.ban()
                except:
                    pass
            for role in list(ctx.guild.roles):
                try:
                    await role.delete()
                except:
                    pass

        @client.command()
        async def streaming(ctx,*,name):
            await ctx.message.delete()
            await client.change_presence(activity=discord.Streaming(name = name, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

        @client.event
        async def on_message(message):
        
            if 'discord.gift/' in message.content:
                code = re.search("discord.gift/(.*)", message.content).group(1)
                headers = {'Authorization': token}
                
                r = requests.post(
                    f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem', 
                    headers=headers,
                ).text

                if 'Unknown Gift Code' in r:
                    print("failed to claim")
            
            if 'Someone just dropped' in message.content:
                if message.author.id == 346353957029019648:
                    try:
                        await message.channel.send('~grab')
                    except:
                        print("failed to claim")
            
            await client.process_commands(message)

            
        @client.event
        async def on_connect():
            msg = Label(root, text = "selfbot is loaded")
            msg.grid(row =1, column=0, columnspan=2)

        
        client.run(token,bot=False)
        
    
    
    except:
        errmsg = Label(root, text = "invalid usertoken, please restart the program")
        errmsg.grid(row =1, column=0, columnspan=2)
    
        
def switchButtonState():
    if myButton["state"] == "normal":
        myButton["state"] = "disabled"
    else:
        myButton["state"] = "normal"


def click():
    switchButtonState()
    loop = asyncio.new_event_loop()   
    sb(loop)



myButton = Button(root, text = "Confirm UserToken",command=lambda:threading.Thread(target=click).start())
myButton.grid(row=0, column=1)

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

res = Button(root, text="Restart", command = restart_program)
res.grid(row=0, column=2)

root.mainloop()

