import discord
from discord.ext import commands, tasks
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import random as rand
import json
import requests
from datetime import datetime, timezone

real_date_cleared = []
status = ['Nurture', 'Titanfall 2', 'Planetside 2', 'a DJ set']
messagecounts = {}

client = commands.Bot(command_prefix = ">")
flag = True
addresses = {}
try:
	f = open('discord_Links.json')
	addresses = json.load(f)
except:
	addresses = {}
	flag = False
	with open('discord_Links.json', 'w') as f:
		json.dump(addresses, f)
	
@client.event
async def on_ready():
	print("Bot is ready af")
	change_status.start()

# Chaning the status
@tasks.loop(seconds = 60)
async def change_status():
	await client.change_presence(activity = discord.Game(rand.choice(status)))

@client.command()
async def send(ctx, number:float, member: discord.Member):
	f = open('discord_Links.json')
	addresses = json.load(f)
	timestamp = str(datetime.now(timezone.utc))
	value = float(number)
	
	try:
		sender = addresses[str(ctx.author)]
	except:
		await ctx.send("Sender did not link Discord with Floarea account yet!")
	try:
		receiver = addresses[str(member)]
	except:
		await ctx.send("Receiver did not link Discord with Florea account yet!")
	sender = str(ctx.author)
	receiver = str(member)
	trans_str = f"{value}|{sender}|{receiver}|{timestamp}"
	trans_dict = {"trans_str" : trans_str}
	response = requests.get(f'http://127.0.0.1:9999/discord-transact', json = trans_dict).json()
	response = response['response']
	if response == "Transaction Successful!":
		await ctx.send(f"\n{ctx.author.mention} sent {value} Floarea coins to {member.mention}")
		print(f"\n{ctx.author.mention} sent {value} Floarea coins to {member.mention}")
	else:
		await ctx.send(response)
	
	f.close()

@client.command()
async def balance(ctx):
	f = open('discord_Links.json')
	addresses = json.load(f)
	try:
		address = addresses[str(ctx.author)]
		data = requests.get(f'http://127.0.0.1:9999/get-balance', json = {"address":address}).text
		balance = json.loads(data)
		balance = balance["balance"]
		await ctx.send(f"{ctx.author.mention} Your balance: {balance}")
	except:
		await ctx.send("Floarea account not linked to discord yet!")
	return
# Logging the messages
#@client.event
#async def on_message(message):
#	pass

# Running the bot
TOKEN = ""
with open("TOKEN") as file:
	TOKEN = file.read()
client.run(TOKEN)