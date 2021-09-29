import sqlite3
from os import path
from pathlib import Path
import os
import discord
from discord.ext import commands , tasks
import time
import json
from ftplib import FTP
import config

TOKEN = config.TOKEN

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents = intents)
bot.remove_command('help')

admin_role = 851811799127949322
info_channel = 797481786682245172
log_channel = 797305288209596456
log_ngrok_channel = 851811718564413520
id_serveur = 796906968202608640

urls_https = ""


@bot.event
async def on_ready():
    print('---------------')
    print(bot.user.name)
    print('---------------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="BauveAnime"))
    print("------------------------ start fini ------------------------")

    ngrok.start()
    https_url.start(1)


@tasks.loop(seconds=10)
async def https_url(content):
    global urls_https
    os.system("curl http://localhost:4040/api/tunnels > tunnels.json")
    with open("tunnels.json") as data_file:
        datajson = json.load(data_file)

    for i in datajson['tunnels']:
        if i['proto'] == "https":
            urls_https = i['public_url']

    conn = sqlite3.connect('data.db')
    cursor = conn.execute("SELECT HTTP FROM URL")
    for row in cursor:
        content = row[0]
    conn.close()

    if (content != urls_https):
        conn = sqlite3.connect('data.db')
        conn.execute(f"DELETE FROM URL WHERE HTTP = '{content}';")
        conn.commit()
        conn.execute(f"INSERT INTO URL (HTTP) VALUES ('{urls_https}');")
        conn.commit()
        print("url change")
        cursor = conn.execute("SELECT ID,AUTO FROM USERS")
        for user_id in cursor:
            if user_id[1] == "on":
                user = await bot.fetch_user(int(user_id[0]))
                await user.send(f'**Voici la nouvelle url:** {urls_https}')
        conn.close()

        fin = open("p_json.txt" , "rt")
        data = fin.read()
        data = data.replace('ToChange', urls_https)
        fin.close()
        fin = open("url.json", "wt")
        fin.write(data)
        fin.close()

        ftp = FTP('files.000webhost.com')
        ftp.login('ba-api',config.LOGIN_FTP)
        ftp.cwd('config.URL_API')
        file_name = 'url.json'
        ftp.storbinary('STOR ' + file_name, open(file_name, 'rb'))

        os.system("ssh pi@yumina.local nohup python3 /home/pi/bot/yumina/test.py &")

@tasks.loop(seconds=0.5)
async def ngrok():
    f = open("ngrok.log", "r")
    lines = f.readline()
    f.close()
    if lines == "" or lines == "\n":
        pass
    else:
        channel = bot.get_channel(log_ngrok_channel)
        await channel.send(f"```{lines}```")

        with open('ngrok.log', 'r') as fin:
            data = fin.read().splitlines(True)
        with open('ngrok.log', 'w') as fout:
            fout.writelines(data[1:])


@bot.event
async def on_member_join(user):
    user_name = str(user)[:-5]
    print(f'{user_name} has joined a server!')
    await user.send("Bienvenue \n Je suis l’ordinateur qui vous permettras d’accéder au serveur BauveAnime. \n Pour connaitre les commandes disponibles envoyer moi **/help** dans cette conversation.")
    conn = sqlite3.connect('data.db')
    conn.execute(f"INSERT INTO USERS (ID, NAME, AUTO) VALUES ({user.id}, '{user_name}', 'off');")
    conn.commit()
    conn.close()

@bot.event
async def on_member_remove(user):
    user_name = str(user)[:-5]
    conn = sqlite3.connect('data.db')
    conn.execute(f"DELETE FROM USERS WHERE ID = {user.id};")
    conn.commit()
    conn.close()
    print(f"{user_name} leave BauveAnime")

@bot.command()
async def help(ctx):
    if ctx.author.id == 342051568356425728 or ctx.author.id == 533349028306616325:
        await ctx.send("__Commandes public:__ \n \n **/url** --> vous aurez la dernier adresse pour accéder à BauveAnime. \n **/auto on** --> vous serez alerté à chaque changement d'adresse. \n **/auto off** --> vous ne serez plus alerté au changement d'adresse. \n \n __Commandes admin:__ \n \n **/update {anime/film/all}** --> update le site. \n **/msg {nom/everyone} '{message}'** --> envoie un message en pv ou sur le channel info. \n **/list {user}** --> liste les user sur le serveur.")
    else:
        await ctx.send("__Voici les commandes du bot:__ \n \n **/url** --> vous aurez la dernier adresse pour accéder à BauveAnime. \n **/auto on** --> vous serez alerté à chaque changement d'adresse. \n **/auto off** --> vous ne serez plus alerté au changement d'adresse.")

@bot.command()
async def url(ctx):
    global urls_https
    if urls_https == "":
        await ctx.send(f"Une erreur est survenu. Contacter **bov** pour régler le problème.")
    else:
        await ctx.send(f"**Voici l'url de BauveAnime:** {urls_https}")

@bot.command()
async def update(ctx, arg=None):
    user_id = ctx.author.id
    if user_id == 342051568356425728 or user_id == 533349028306616325:
        if arg == None:
            await ctx/send("Argument manquant.")
        elif arg == "anime" or arg == "film" or arg == "all":
            await ctx.send(f"Start update of {arg}")
            os.system(f"sh update_{arg}.sh")
            await ctx.send(f"End update of {arg}")
    else:
        await ctx.send("Cette commande n'est pas pour vous.")

@bot.command()
async def msg(ctx, arg, arg1):
    user_id = ctx.author.id
    if user_id == 533349028306616325 or user_id == 342051568356425728:
        if arg == "everyone":
            channel = bot.get_channel(info_channel)
            await channel.send(f"{arg1}")
            await ctx.send("Message envoyer sur le serveur.")
        else:
            list_user = []
            guild = bot.get_guild(id_serveur)
            memberList = guild.members
            for name in memberList:
                list_user.append(str(name)[:-5])
            if arg in list_user:
                for name in memberList:
                    if str(name)[:-5] == arg:
                        user = await bot.fetch_user(int(name.id))
                        await user.send(f'{arg1}')
                        await ctx.send("Message envoyer.")
            else:
                await ctx.send("Cette utilisateur n'existe pas.")
    else:
        await ctx.send("Cette commande n'est pas pour vous.")

@bot.event
async def on_message(message):
    if (message.author.id != bot.user.id):
        channel = bot.get_channel(log_channel)
        await channel.send(f"{str(message.author.name)}: {message.content}")
    await bot.process_commands(message)

@bot.command()
async def list(ctx, arg=None):
    if ctx.author.id == 342051568356425728 or ctx.author.id == 533349028306616325:
        if arg == "user":
            guild = bot.get_guild(id_serveur)
            memberList = guild.members
            await ctx.send("__Voici la liste des utilisateurs:__")
            for name in memberList:
                await ctx.send(str(name)[:-5])
    else:
        pass

@bot.command()
async def special(ctx):
    url_special = f"Voici le lien special: {urls_https}/special/special.html"
    await ctx.send(url_special)



@bot.command()
async def auto(ctx ,arg=None):
    user_id = ctx.author.id
    user_name = str(ctx.author)[:-5]

    global auto
    if (arg == None):
      await ctx.send("il manque **on** ou **off** comme argument.")
    elif(arg == "on"):
        conn = sqlite3.connect('data.db')
        cursor = conn.execute(f"SELECT AUTO FROM USERS WHERE ID = {user_id}")
        for row in cursor:
            auto = row[0]
        conn.close()
        print(f"auto: {auto}")
        if auto == "off":
            conn = sqlite3.connect('data.db')
            conn.execute(f"DELETE FROM USERS WHERE ID = {user_id};")
            conn.commit()
            conn.execute(f"INSERT INTO USERS (ID, NAME, AUTO) VALUES ({user_id}, '{user_name}', 'on');")
            conn.commit()
            conn.close()
            await ctx.send("L'envoie automatique du changement d'adresse est enregistrer, pour arrêter l'alerte faites **/auto off**.")
        elif auto == "on":
            await ctx.send("Vous étes déjà enregistrer.")
    elif(arg == "off"):
        conn = sqlite3.connect('data.db')
        cursor = conn.execute(f"SELECT AUTO FROM USERS WHERE ID = {user_id}")
        for row in cursor:
            auto = row[0]
        conn.close()
        print(f"auto: {auto}")
        if auto == "on":
            conn = sqlite3.connect('data.db')
            conn.execute(f"DELETE FROM USERS WHERE ID = {user_id};")
            conn.commit()
            conn.execute(f"INSERT INTO USERS (ID, NAME, AUTO) VALUES ({user_id}, '{user_name}', 'off');")
            conn.commit()
            conn.close()
            await ctx.send("L'envoie auto a été stopper pour vous.")
        elif auto == "off":
            await ctx.send("Vous n'êtes pas enregistrer, pour vous enregister faite **/auto on**.")

bot.run(TOKEN)
