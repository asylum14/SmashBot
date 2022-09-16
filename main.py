import discord
from discord.ext import commands
from discord.ui import Select, View,Button
import mysql.connector
import os
import time

TOKEN = 'MzYzNDYzNzYwMDA3OTIxNjc2.G_QNai.y0kRK-mzb0ppdzoIJ6KKJJfLqWDHZmzW7FdTWM'
dbPass = "MonoKuma21!"
whitelist = []
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
characterList = []
#let's me know that the bot is online
@bot.event
async def on_ready():
    print('Bot is online')


#this command is used for basic messaging/ image posting
@bot.command()
async def test(ctx):
    print('TESTING')
    await ctx.send(
        'https://tenor.com/view/suicidio-payaso-suicide-clow-gif-14176065')


##Admin Commands

#used to ping a certain user a set amount of times
#@client.command()
#async def ping(ctx, user, amount):
#  if ctx.message.author.top_role.permissions.administrator and ctx.message.channel in db:
#    for x in range(int(amount)):
#      time.sleep(1)
#      await ctx.send(user)
  
##used to add channels that can be pinged
#@client.command()
#async def addPingChannel(ctx):
#  if ctx.message.author.top_role.permissions.administrator:
#    if ctx.message.channel in db:
#      ctx.send('Channel is already a ping Channel')
#    else:
#      db[ctx.message.channel] = str(ctx.message.channel)
#      await ctx.send(f'added {ctx.message.channel} as a ping channel')

@bot.command()
async def purge(ctx , v):
  if ctx.message.author.top_role.permissions.administrator:
   await ctx.channel.purge(limit=int(v)+1)
   await ctx.send(f"{ctx.message.author} Deleted {v} messages. Gotta sweep sweep sweep!")

@bot.command()
async def report(ctx, c1, c2):
    sql = '''SELECT firstName from player ORDER BY firstName'''
    cursor.execute(sql)
    players = cursor.fetchall()

    sql = '''SELECT fighterName from fighter ORDER BY fighterName'''
    cursor.execute(sql)
    characters = cursor.fetchall()
    playerOptions=[]
    characterOptions=[]
    for p in players:
        playerOptions.append(discord.SelectOption(label=p[0]))
    for c in characters:
        characterOptions.append(c[0].upper())

    if c1.upper() not in characterOptions:
        await ctx.send(f"Character {c1} is not Valid")
    elif c2.upper() not in characterOptions:
        await ctx.send(f"Character {c2} is not Valid")
        return
    #TODO Initialize Button
    submitButton = Button(label="Submit",style=discord.ButtonStyle.green)
    p1select = Select(options=playerOptions)
    p2select = Select(options=playerOptions)
    stock = Select(options=[discord.SelectOption(label=1),
                            discord.SelectOption(label=2),
                            discord.SelectOption(label=3)
                            ])
    p1Win = Select(options=[discord.SelectOption(label=0),
                            discord.SelectOption(label=1)])

    data = {}
    data.update({"p1Character": c1})
    data.update({"p2Character": c2})
    async def p1Callback(interaction):
        data.update({"Player1": p1select.values[0]})
        print(data)
        await interaction.response.send_message("")
    async def p2Callback(interaction):
        data.update({"Player2": p2select.values[0]})
        print(data)
        await interaction.response.send_message("")
    async def p1win_callback(interaction):
        data.update({"P1Win": p1Win.values[0]})
        print(data)
        await interaction.response.send_message("")
    async def stockcallback(interaction):
        data.update({"stocks": stock.values[0]})
        print(data)
        await interaction.response.send_message("")
    async def buttonCallback(interaction):
        updateRating(data['Player1'],data['Player2'],data['P1Win'],data['p1Character'], data['p2Character'], data['stocks'])
        await interaction.response.send_message("Report Submitted")
        return

    p1select.callback = p1Callback
    p2select.callback = p2Callback
    p1Win.callback = p1win_callback
    stock.callback = stockcallback
    submitButton.callback = buttonCallback
    view = View()
    view.add_item(p1select)
    view.add_item(p2select)
    view.add_item(stock)
    view.add_item(p1Win)
    view.add_item(submitButton)

    await ctx.send("Please Report The game", view=view)

def updateRating(p1,p2,p1win,c1,c2,stocks):
    p1win = bool(p1win)
    stocks = int(stocks)
    sql = f'''SELECT * from player WHERE player.firstName="{p1}"'''
    cursor.execute(sql)
    players = cursor.fetchall()
    p1pid = players[0][0]
    p1firstName = players[0][1]
    p1rating = players[0][2]
    p1games = players[0][3]
    p1wins = players[0][4]
    p1loses = players[0][5]

    sql = f'''SELECT * from player WHERE player.firstName="{p2}"'''
    cursor.execute(sql)
    players = cursor.fetchall()
    p2pid = players[0][0]
    p2firstName = players[0][1]
    p2rating = players[0][2]
    p2games = players[0][3]
    p2wins = players[0][4]
    p2loses = players[0][5]

    sql = f'''SELECT * from plays WHERE plays.pid={p1pid}'''
    cursor.execute(sql)
    plays = cursor.fetchall()
    sql = f'''SELECT fighterName from fighter'''
    cursor.execute(sql)
    result = cursor.fetchall()
    characters =[]
    for c in result:
        characters.append(c[0].upper())
    p1cid = []
    p1characterRatings = []
    p1characterGames = []
    p1characterWins = []
    p1characterLoses = []
    for i in range(len(plays)):
        p1cid.append(plays[i][2])
        p1characterRatings.append(plays[i][3])
        p1characterGames.append(plays[i][4])
        p1characterWins.append(plays[i][5])
        p1characterLoses.append(plays[i][6])
    p1characterName = []
    for i in p1cid:
        sql = f'''SELECT * from fighter WHERE fighter.fid={i}'''
        cursor.execute(sql)
        p1characterName.append(cursor.fetchall()[0][1])

    if c1 in p1characterName:
        cIndex = p1characterName.index(c1)
        p1characterGames[cIndex] += 1
        c1Rating = p1characterRatings[cIndex]
        if p1win == 1:
            p1characterWins[cIndex] += 1
        else:
            p1characterLoses[cIndex] += 1
    else:
        p1cid.append(characters.index(c1.upper()))
        p1characterName.append(c1)
        cIndex = p1characterName.index(c1)
        p1characterGames.append(1)
        p1characterRatings.append(1000)
        c1Rating = p1characterRatings[cIndex]
        p1characterLoses.append(0)
        p1characterWins.append(0)
        if p1win == 1:
            p1characterLoses[cIndex] += 1
        else:
            p1characterWins[cIndex] += 1


    sql = f'''SELECT * from plays WHERE plays.pid={p2pid}'''
    cursor.execute(sql)
    plays = cursor.fetchall()
    p2cid = []
    p2characterRatings = []
    p2characterGames = []
    p2characterWins = []
    p2characterLoses = []
    for i in range(len(plays)):
        p2cid.append(plays[i][2])
        p2characterRatings.append(plays[i][3])
        p2characterGames.append(plays[i][4])
        p2characterWins.append(plays[i][5])
        p2characterLoses.append(plays[i][6])
    p2characterName = []
    #if the player has played the character
    if c2 in p2characterName:
        cIndex = p2characterName.index(c2)
        p2characterGames[cIndex] += 1
        c2Rating = p2characterRatings[cIndex]
        if p1win == 1:
            p2characterLoses[cIndex] += 1
        else:
            p2characterWins[cIndex] += 1
    else:
        p2cid.append(characters.index(c2.upper()))
        p2characterName.append(c2)
        cIndex = p2characterName.index(c2)
        p2characterGames.append(1)
        p2characterRatings.append(1000)
        c2Rating = p2characterRatings[cIndex]
        p2characterLoses.append(0)
        p2characterWins.append(0)
        if p1win == 1:
            p2characterLoses[cIndex] += 1
        else:
            p2characterWins[cIndex] += 1

    for i in p2cid:
        sql = f'''SELECT * from fighter WHERE fighter.fid={i}'''
        cursor.execute(sql)
        p2characterName.append(cursor.fetchall()[0][1])

    k = 200
    mul = stocks/3
    pa = probability(c1Rating, c2Rating)
    pb = probability(c2Rating, c1Rating)

    if p1win:
        c1Rating += mul*(k*(1-pa))
        c2Rating += mul*(k*(0-pb))
    else:
        c1Rating += mul * (k * (0 - pa))
        c2Rating += mul * (k * (1 - pb))

    p2characterRatings[cIndex] = c2Rating
    cIndex = p2characterName.index(c2)
    p1characterRatings[cIndex] = c1Rating

    p1Index = p1firstName.index(p1)
    p2Index = p2firstName.index(p2)

    p1games += 1
    p2games += 1
    if p1win:
        p1wins += 1
        p2loses += 1
    else:
        p1loses += 1
        p2wins += 1
    count = 0
    sumRating = 0
    for i in p1characterRatings:
        g = p1characterGames[count]
        weight = g/p1games
        sumRating += (weight * i)
    p1rating = sumRating

    count = 0
    sumRating = 0
    for i in p2characterRatings:
        g = p2characterGames[count]
        weight = g / p2games
        sumRating += (weight * i)
    p2rating = sumRating

    sql = f'''select * from game'''
    cursor.execute(sql)
    gid=len(cursor.fetchall())+1
    sql = f'''INSERT into game VALUES ({gid},{p1pid},{p2pid},{int(p1win)},{p1cid[p1characterName.index(c1)]+1},
    {p2cid[p2characterName.index(c2)]+1},{stocks},{p1rating},{p2rating})'''
    cursor.execute(sql)
    mydb.commit()

    sql = f'''
        UPDATE player 
        SET player.rating ={p1rating}, player.gameCount ={p1games},
        player.wins ={p1wins}, player.loses= {p1loses}
        WHERE player.pid={p1pid}'''
    cursor.execute(sql)
    mydb.commit()

    sql = f'''
            UPDATE player 
            SET player.rating ={p2rating}, player.gameCount ={p2games},
            player.wins ={p2wins}, player.loses= {p2loses}
            WHERE player.pid={p2pid}'''
    cursor.execute(sql)
    mydb.commit()

    sql = f'''select * from plays'''
    cursor.execute(sql)
    uid = len(cursor.fetchall())
    uid2 = uid+1

    cIndex = p1characterName.index(c1)
    if c1 in p1characterName:
        sql = f'''
                    UPDATE plays 
                    SET plays.rating ={p1characterRatings[cIndex]}, plays.gameCount ={p1characterGames[cIndex]},
                    plays.wins ={p1characterWins[cIndex]}, plays.loses= {p1characterLoses[cIndex]}
                    WHERE plays.pid={p1pid} and plays.cid ={p1cid[cIndex]}'''
        cursor.execute(sql)
        mydb.commit()

    else:
        sql = f'''INSERT into plays VALUES ({uid},{p1pid},{p1cid[cIndex]},
        {p1characterRatings[cIndex]},{p1characterGames[cIndex]},{p1characterWins[cIndex]},{p1characterLoses[cIndex]})'''
        cursor.execute(sql)
        mydb.commit()

    cIndex = p2characterName.index(c2)
    if c2 in p2characterName:
        sql = f'''
                        UPDATE plays 
                        SET plays.rating ={p2characterRatings[cIndex]}, plays.gameCount ={p2characterGames[cIndex]},
                        plays.wins ={p2characterWins[cIndex]}, plays.loses= {p2characterLoses[cIndex]}
                        WHERE plays.pid={p2pid} and plays.cid ={p2cid[cIndex]}'''
    else:
        sql = f'''INSERT into plays VALUES ({uid2},{p2pid},{p2cid[cIndex]},
            {p2characterRatings[cIndex]},{p2characterGames[cIndex]},{p2characterWins[cIndex]},{p2characterLoses[cIndex]})'''
    cursor.execute(sql)

def probability(r1, r2):
    return 1.0 / (1+(10**((1.0 * (r2 - r1)) / 400)))

##Help Command
@bot.command()
async def commands(ctx):
    await ctx.send(
      '__**Admin Commands**__\n'+
      '**.addPingChannel**: sets the current channel to a ping Channel so the bot can post pings.\n'+
      '**.ping {user}**: allows admins to ping other users as many times as the would like\n'+
      '**.purge {amount}**: deletes a set amount of messages\n'
    )


@bot.command()
async def testDB(ctx):
        sql = '''SELECT * from player'''
        cursor.execute(sql)
        print(cursor.fetchall())


@bot.command()
async def playerInfo(ctx, plyer):
    if plyer == "<@142855512805998593>":
        plyer = "Michael"
    elif plyer == "<@336220036006019083>":
        plyer="Jaden"
    elif plyer == "<@281237935586672640>":
        plyer = "Steven"
    else:
        await ctx.send("User Not Valid. No Instance of Player in Database")

    sql = f'''SELECT * from player WHERE player.firstName="{plyer}"'''
    cursor.execute(sql)
    players = cursor.fetchall()
    pid = players[0][0]
    firstName = players[0][1]
    rating = players[0][2]
    games = players[0][3]
    wins = players[0][4]
    loses = players[0][5]

    sql = f'''SELECT * from plays WHERE plays.pid={pid}'''
    cursor.execute(sql)
    plays=cursor.fetchall()
    cid=[]
    characterRatings=[]
    characterGames=[]
    characterWins=[]
    characterLoses=[]
    for i in range(len(plays)):
        cid.append(plays[i][2])
        characterRatings.append(plays[i][3])
        characterGames.append(plays[i][4])
        characterWins.append(plays[i][5])
        characterLoses.append(plays[i][6])
    characterName =[]
    for i in cid:
        sql = f'''SELECT * from fighter WHERE fighter.fid={i}'''
        cursor.execute(sql)
        characterName.append(cursor.fetchall()[0][1])

    await ctx.send(f"PlayerID: {pid}\n"
          f"Player Name: {firstName}\n"
          f"Player Rating: {rating}\n"
          f"Games Played: {games}\n"
          f"Games Won: {wins}\n"
          f"Games Lost: {loses}\n"
          f"characters: {characterName}")
    return


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = dbPass,
    database = "player"
)

cursor = mydb.cursor()

#Retrieving single row
#sql = '''SELECT * from player'''

#Executing the query
#cursor.execute(sql)

#print(cursor.fetchall())

bot.run(TOKEN)
