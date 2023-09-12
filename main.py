import discord
from discord import app_commands
import asyncio
import os
from keep_alive import keep_alive

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="help",
              description="I will help you!",
              guild=discord.Object(id=1040967504006217808))
async def help_command(interaction):
  embed = discord.Embed(
    title="If you need any help, feel free to open a ticket",
    description=f"<#{1040967504006217808}>",
    color=0xffffff)
  await interaction.response.send_message(embed=embed)


@client.event
async def on_ready():

  await tree.sync(guild=discord.Object(id=1040967504006217808))
  await reminder()

  print("Ready!")


TIMER = 600
from datetime import datetime


def NextSession(time):
  now = datetime.utcnow()
  nowh = now.hour
  nowm = now.minute
  print(nowh)
  if time == [0, 6] and nowh > 7:
    diffh = 24 - nowh - 1
  else:
    diffh = abs(nowh - time[0]) - 1
  diffm = abs(60 - nowm)
  return str(diffh) + "h " + str(round(diffm / 10) * 10) + "m"

  return ""


def WhatSession():
  now = datetime.utcnow()
  nowh = now.hour
  times = [[0, 6], [7, 11], [12, 16], [20, 22]]  #summer
  #times = [[1, 7], [6, 12], [13, 17], [21, 23]]#winter
  sessions = ["Asia", "London", "New York", "Spread hours"]
  if now.isoweekday() == 6:
    return "Market is closed", "Opens in: 1d " + NextSession([21, -1])
  elif now.isoweekday() == 7 and now.hour < 21:
    return "Market is closed", "Opens in: " + NextSession([21, -1])
  elif now.isoweekday() == 5 and now.hour > 20:
    return "Market is closed", "Opens in: 2d " + NextSession([21, -1])

  for i, x in enumerate(times):
    if nowh >= x[0] and nowh < x[1]:
      if i + 1 == 4:
        return sessions[i], "Asia opens in " + NextSession(
          times[0])  #itt a hiba
      else:
        if i + 1 == 2:
          return sessions[i], "NY" + " opens in: " + NextSession(times[i + 1])
        elif i + 1 == 3:
          return sessions[i], "Spread" + " starts in: " + NextSession(
            times[i + 1])
        else:
          return sessions[i], sessions[i + 1] + " opens in: " + NextSession(
            times[i + 1])

  #
  if i == 2:
    return "nothing is open", "NY" + " opens in: " + NextSession(times[i])
  elif i == 3:
    return "nothing is open", "Spread" + " starts in: " + NextSession(times[i])
  return "nothing is open", sessions[i] + " opens in: " + NextSession(times[i])


async def reminder():
  print("timer started")

  while True:
    global TIMER
    TIMER += 1
    #print(TIMER)
    if TIMER == 601:
      channel = client.get_channel(1089297423811231764)
      channel2 = client.get_channel(1089298036070547577)

      TIMER = 0
      asd = WhatSession()
      if channel.name != asd[0]:
        await channel.edit(name=asd[0])
        print(asd[0])
      if channel2.name != asd[1]:
        await channel2.edit(name=asd[1])
        print(asd[1])

    await asyncio.sleep(1)  #Sleeps 2 hours.


@client.event
async def on_message(message):
  print(message.content)

  msg = ""
  reaction = ""
  if 'in' == message.content.lower():
    msg = "and **Out**"
    reaction = "<:IAOTLogo:1066784613424431245>"
  elif len([
      x for x in ['niga', "nigger", "nigga", "niger", "nig", "black monkey"]
      if x in message.content.lower()
  ]) > 0:
    msg = ""
    reaction = "😴"
  elif 'ping' == message.content.lower():
    msg = "**pong**"
  elif 'are you racist' in message.content.lower():
    msg = "No, it is not appropriate to use racial slurs or hate speech, including the N-word. Such language is harmful and can be offensive to individuals or groups based on their race, ethnicity, or background. It's important to be respectful and considerate in our communication, and to avoid language that can hurt or marginalize others."
  elif len([x for x in ['helpwwww'] if x in message.content.lower()
            ]) > 0 and "@" not in message.content.lower(
            ) and message.author.id != 882241695293526116:
    msg = "<@&1043655353457451038>"
  elif message.channel.id == 1114996240506159204:
    await message.add_reaction("🔥")
  
  if msg != "":
    await message.reply(msg)
  if reaction != "":
    await message.add_reaction(reaction)


keep_alive()

try:
  client.run(
    "TOKEN HERE")
except discord.errors.HTTPException:
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  os.system('kill 1')
  os.system("python restarter.py")
