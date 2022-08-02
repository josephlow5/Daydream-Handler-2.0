import discord
import os
import douyin,douyin_reaction,douyin_utils
import crypto
import random
#from keep_alive import keep_alive
from discord.ext import tasks
  
client = discord.Client()

@client.event
async def on_ready():
  print('I am ready for hunting beauty!')
  activity = discord.Game(name="Beautiful Girl")
  await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_raw_reaction_add(payload):
  await douyin_reaction.on_raw_reaction_add(payload,client)

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  """This is only for backup all videos in the channel
  if message.content == "scrape":
    await douyin_utils.get_channel_history(message,client)
  """
  await douyin.on_message(message,client)   #handle message with dream keyword
  await crypto.on_message(message,client)  #handle crypto conversion

@tasks.loop(seconds=120.0)
async def change_activity():
  try:
    activities = ["Beautiful Girl","Befamous.cyou","Douyin YYDS","Market Info"]
    selected = random.choice(activities)
    if selected == "Market Info":
      market_info = crypto.random_market_info()
      if market_info == "Error!":
        selected = "Beautiful Girl"
      else:
        selected = market_info    
    activity = discord.Game(name=selected)
    await client.change_presence(status=discord.Status.online, activity=activity)
  except:
    pass
change_activity.start()

#keep_alive()
client.run("<BOT TOKEN>")
