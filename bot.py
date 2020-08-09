import time
import logging
import json
import os
import random
import asyncio
import discord
from discord.ext import commands

# Global Vars
logFile = './logs/discord.log'
botPrefix = '?'
role = 'admin'
manageRole = "factadmin"
status = 'with Your Mom'


# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=logFile, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Bot setup
# Bot Token


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

# Bot config
bot = commands.Bot(command_prefix=botPrefix)


@bot.event
async def on_ready():
    print('Bot is now working!')
    await bot.change_presence(activity=discord.Game(name=status))

# integer test function


def is_int(val):
    if type(val) == int:
        return True
    else:
        if val.is_integer():
            return True
        else:
            return False

# JSON stuff
# Read JSON files, build the stats and facts dicts


statsF = open('stats.json')
statsList = json.load(statsF)

factList = {}

for x in os.listdir('./facts/'):
    file = x
    fileName, fileExtension = os.path.splitext(file)
    xOpen = open('./facts/' + file)
    xData = json.load(xOpen)
    factList[fileName] = xData

# Function to dump JSON to files


def jsondump(name):
    fname = name
    if fname is None:
        pass
    else:
        with open('./facts/' + fname + '.json', 'w') as factsOutFile:
            json.dump(factList[fname], factsOutFile)

    with open('./stats.json', 'w') as statsOutFile:
        json.dump(statsList, statsOutFile)


# Commands
# Fact Commands

# Specific Fact (?fact category id)


@bot.command(name='fact',
                description="Displays a specific fact. Use '?fact <category> <id#>' to call up a specific fact.",
                brief=": Use '?fact <category> <id#>' to call up a specific fact.")
async def specificfact(ctx, arg1, arg2):
    global selected
    try:
        int_arg2 = int(arg2)
        is_int(int_arg2)
    except Exception as e:
        logging.exception(e)
        await ctx.send("Need to include a number to call a specific fact!")
        return
    try:
        if int(arg2) <= statsList[arg1]["currentIndex"]:
            for index, piece in enumerate(factList[arg1]):
                if factList[arg1][index]['id'] == arg2:
                    selected = factList[arg1][index]
                    factList[arg1][index]['times_printed'] += 1
                    factList[arg1][index]['last_printed'] = str(time.time())
            statsList[arg1]['totalFactsPrinted'] += 1
            statsList[arg1]['lastFactPrinted'] = selected['id']
            jsondump(arg1)
            await ctx.send('{} #{}:\n{}'.format(statsList[arg1]['tag'], selected['id'], selected['fact']))
    except Exception as e:
        logging.exception(e)
        await ctx.send("I don't recognize that fact number, try a different number")
        return

# Add Fact (?addfact category "fact")


@bot.command(name='addfact',
                description="Adds a fact. Use '?addfact <category> \"<fact>\"' to add a fact to a category.",
                brief=": Use '?addfact <category> \"<fact>\"' to add a fact.")
@commands.has_role(manageRole)
async def addfact(ctx, arg1, arg2):
    requestor = ctx.author
    newIndex = statsList[arg1]["currentIndex"] + 1
    msg1 = await ctx.send('Add "' + arg2 + '" as ' + statsList[arg1]['tag'] + ' #' + str(newIndex) + "?")
    # Check for response emoji
    def check(reaction, user):
        return user == requestor and str(reaction.emoji) == '👍'
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Add fact timed out, please re-submit your fact')
    else:
        factList[arg1].append({'id': str(newIndex), 'fact': arg2, 'added_by': str(requestor), 'times_printed': 0})
        statsList[arg1]["currentIndex"] = newIndex
        await ctx.send('Added ' + statsList[arg1]['tag'] + ' #' + str(newIndex) + ":\n" + arg2)
        jsondump(arg1)

# Edit Fact (?editfact category id "fact")

# Delete Fact (?deletefact category id)


@bot.command(name='deletefact',
                description="Deletes a fact. Use '?deletefact <category> <id#>' to delete a specific fact from the designated category.",
                brief=": Use '?deletefact <category> <id#>' to delete a fact.",
                pass_context=True)
@commands.has_role(role)
async def delete_fact(ctx, arg1, arg2):
    global selected
    requestor = ctx.author
    try:
        int_arg2 = int(arg2)
        is_int(int_arg2)
    except Exception as e:
        logging.exception(e)
        await ctx.send("Need to include a number to delete a fact!")
        return
    try:
        if int(arg2) <= statsList[arg1]["currentIndex"]:
            for index, object in enumerate(factList[arg1]):
                if factList[arg1][index]["id"] == arg2:
                    selected = factList[arg1][index]
    except Exception as e:
        logging.exception(e)
        await ctx.send("That fact doesn't exist!")
        return
    await ctx.send("Delete " + statsList[arg1]['tag'] + " #" + selected["id"] + ": " + selected["fact"] + "?")
    # Check for response emoji
    def check(reaction, user):
        return user == requestor and str(reaction.emoji) == '👍'
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Delete fact timed out, please re-submit your fact')
    else:
        factList[arg1].remove(selected)
        jsondump(arg1)
        await ctx.send('Deleted ' + statsList[arg1]['tag'] + ' #' + selected["id"] + ": " + selected["fact"])




# Add Category (?addcategory category "name" "lead line" "description")


@bot.command(name='addcategory',
                description="Adds a fact category. Use '?addcategory \"<name>\" <id> \"<tag>\" \"<description>\"' to add a category. "
                            "\n-The <name> should be wrapped in quotes, and is the proper name for the category (i.e. \"ChrisWorld Facts\") "
                            "\n-The <id> is the short identifier for the category (i.e. cwf); the <tag> should be wrapped in quotes, and is the "
                            "leader line you want used for each fact (i.e. \"ChrisWorld Fact\")"
                            "\n-The <description> should be wrapped in quotes, and is the description for the category (i.e. \"Facts about ChrisWorld, a terrible place for anyone but a Chris\").",
                brief=": Use '?addcategory \"<name>\" <id> \"<tag>\" \"<description>\"' to add a category.")
@commands.has_role(manageRole)
async def addcategory(ctx, arg1, arg2, arg3, arg4):
    requestor = ctx.author
    msg1 = await ctx.send('Add Category "' + arg1 + '" with the id "' + arg2 + '", the tag "' + arg3 + '" and the description "' + arg4 + '"?')
    # Check for response emoji
    def check(reaction, user):
        return user == requestor and str(reaction.emoji) == '👍'
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Add fact timed out, please re-submit your category')
    else:
        statsList['lastID'] += 1
        statsList[arg2] = {'id': statsList['lastID'], 'name': arg1, 'desc': arg3, 'tag': arg4, 'currentIndex': 0, 'totalFactsPrinted': 0}
        await ctx.send('Added "' + arg1 + '" as "' + arg2 + '"...')
        factList[arg2] = []
        jsondump(arg2)
# Edit Category (?editcategory category "name" "lead line" "description")

# Delete Category (?deletecategory category)


@bot.command(name='deletecategory',
                description="Deletes a category. Use '?deletecategory <category>' to delete a specific fact category.",
                brief=": Use '?deletefact <category>' to delete a category.",
                pass_context=True)
@commands.has_role(role)
async def delete_category(ctx, arg1):
    global selected
    requestor = ctx.author
    try:
        if isinstance(statsList[arg1], dict):
            selected = statsList[arg1]
    except Exception as e:
        logging.exception(e)
        await ctx.send("That category doesn't exist!")
        return
    await ctx.send("Delete category " + statsList[arg1]['name'] + "?")
    # Check for response emoji
    def check(reaction, user):
        return user == requestor and str(reaction.emoji) == '👍'
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Delete category timed out, please re-submit your deletecategory command')
    else:
        del statsList[arg1]
        jsondump(arg1)
        await ctx.send('Deleted category ' + selected['name'] + '...')

# List Categories (?listcategory)


@bot.command(name='listcategory',
                description="Lists available Categories. Use '?listcategory' to get a list of category IDs and their descriptions.",
                brief=": Use '?listcategory' to list categories.")
async def listcategory(ctx):
    clist = '```'
    for x in statsList:
        if isinstance(statsList[x], dict):
            category = x
            desc = statsList[x]['desc']
            item = ("\n " + category + ": " + desc)
            clist += item
    clist += '```'
    await ctx.send(clist)
# Category Details (?categorydetails category)

# Random Fact Generator (?random category)


@bot.command(name='random',
                description="Prints a random fact. Use '?random <category> <id#>' to print a random fact from the designated category.",
                brief=": Use '?random <category> <id#>' to to print a random fact.")
async def rfg(ctx, arg):
    try:
        selected = random.choice(factList[arg])
        if selected['id'] == statsList[arg]['lastFactPrinted']:
            selected = random.choice(factList[arg])
        for index, piece in enumerate(factList[arg]):
            if factList[arg][index] == selected['id']:
                factList[arg][index]['times_printed'] += 1
                factList[arg][index]['last_printed'] = str(time.time())
        statsList[arg]['totalFactsPrinted'] += 1
        statsList[arg]['lastFactPrinted'] = selected['id']
        jsondump(arg)
        await ctx.send('{} #{}:\n{}'.format(statsList[arg]['tag'], selected['id'], selected['fact']))
    except Exception as e:
        logging.exception(e)
        await ctx.send("I don't recognize that fact category, please try a different category, or "
                       "try listing the categories.")

# Start this bad boy up
bot.run(token)
