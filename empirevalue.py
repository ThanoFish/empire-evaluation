import discord
from discord import app_commands

from skyblockapiquery import get_prices, get_minion_data, get_minion_craft_cost, get_bazaar_instabuy
from helper import format_coins, format_wood_type

from dotenv import load_dotenv
from os import getenv

import json
from random import random
from typing import Literal
from re import match
from time import time

AZ = 700998149170397305 # tova sum az
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

load_dotenv()

api_key = getenv('API_KEY')
THE_EMPIRE = "d12ac4434e7141baaf1fa09fd60651ce" # skyblock profile uuid
NIKEYBG = "badcaa4ac60a4f5c883b553c8a45bd63" # minecraft uuid
WOOD_TYPES = ['ENCHANTED_ACACIA_LOG', 'ENCHANTED_BIRCH_LOG', 'ENCHANTED_DARK_OAK_LOG',
                  'ENCHANTED_JUNGLE_LOG', 'ENCHANTED_OAK_LOG', 'ENCHANTED_SPRUCE_LOG',
                  "ENCHANTED_DIAMOND_BLOCK", "ENCHANTED_COBBLESTONE"]

@client.event
async def on_ready():
    print("Ready!")
    with open("./timers.empire", "r+") as f:
        timers_array = json.load(f)
        i = 0
        while i < len(timers_array):
            t = timers_array[i]
            if time() >= t["timestamp"]:
                timers_array.pop(i)
                i -= 1
                await client.get_channel(t["channel"]).send(f"@everyone {t['message']}")
            i += 1

@tree.command(name="test", description="replys omg")
async def test(ctx, arg: str):
    await ctx.response.send_message(arg + "1")


@tree.command(name="sync", description="syncs commands")
async def sync(ctx):
    if (ctx.user.id == AZ):
        await tree.sync()
        await ctx.response.send_message("Done!")
    else:
        await ctx.response.send_message("You can't use this command!")

@tree.command(name="empirestats", description="get info about the stats of THE EMPIRE")
async def empirestats(ctx: discord.Interaction):
    await ctx.response.defer(thinking=True);
    
    embed = discord.Embed(
        title="THE EMPIRE BUSINESS"
    )

    minion_data = get_minion_data(
        THE_EMPIRE, NIKEYBG, api_key)

    embed.add_field(name="Crafted minions:",
                    value=minion_data["crafted"], inline=False)
    embed.add_field(name="Minion slots:",
                    value=minion_data["slots"], inline=False)

    for i in sorted(WOOD_TYPES, key=lambda x: get_prices(x)["sell_offer"], reverse=True):
        info = get_prices(i)

        embed.add_field(name=format_wood_type(i), value=f"""
                        Sell offer: {format_coins(info["sell_offer"])}
                        Insta sell: {format_coins(info["insta_sell"])}
                        Spread: {round(info["spread"], 1)}
                        """, inline=False)

    embed.add_field(name="Gigachad?:", value=(
        "Yes 🥶" if random() < 0.968 else "No 💀"))

    await ctx.followup.send(embed=embed)


@tree.command(name="isgigachad", description="Checks if the empire is gigachad or not")
async def isgigachad(ctx):
    await ctx.response.send_message("Yes 🥶" if random() < 0.968 else "No 💀")

@tree.command(name="empirevalue", description="Responds with the price of one stock of The Empire.")
async def empirevalue(ctx):
    await ctx.response.send_message("""
Stock count: 10 000 000
Price per stock: 34 000 000 000 000 coins
Total value: 340 000 000 000 000 000 000 coins

(updates once every 2 hours)
                                    """)

@tree.command(name="minioncraft")
async def minioncraft(ctx, minion_type: str, tier: int):
    await ctx.response.defer(thinking=True);
    
    minion = f"{minion_type.upper()}_GENERATOR_{tier}"
    
    cost = get_minion_craft_cost(minion)
    
    message = ""
    
    total_price = 0
    
    for item in cost.keys():
        if "WOOD_" in item: continue
        price = get_bazaar_instabuy(item) * cost[item]
        total_price += price
        message += f"{cost[item]}x {item.replace('_', ' ').title()} ({format_coins(price)} coins)\n"
    
    message += "\nTotal: " + format_coins(total_price) + " coins"
    
    await ctx.followup.send(message)

@tree.command(name="addstock", description="Add information about the empire's stock.")
@app_commands.describe(amount=
                       "d - double chest; c - chest; r - red; s - stack. primerno: 2d+5r+3s+56 - 2 double chesta + 5 reda + 3 staka + 56")
async def addstock(ctx, wood_type: Literal[tuple(WOOD_TYPES)], amount: str):
    
    if not match("^[0-9dcrs+\-]+$", amount):
        await ctx.response.send_message("еби си майката педераст")
        return
    
    # prevedi go na chisla
    amount = amount.replace("d", "*2c").replace("c", "*3r").replace("r", "*9s").replace("s", "*64")
    x = eval(amount)
    
    with open("./data.empire", "r+") as f:
        data = json.load(f)
        data[wood_type] += x;
        f.seek(0)
        json.dump(data, f);
    
    await ctx.response.send_message(f"Added {x} to {wood_type}")

@tree.command(name="resetstock", description="Resets the empire's stock tracker.")
async def resetstock(ctx):
    with open("./data.empire", "w") as f:
        json.dump({w: 0 for w in WOOD_TYPES}, f)
    
    await ctx.response.send_message("Reset stock tracker.")
    
@tree.command(name="checkstock", description="Check stock worth.")
async def checkstock(ctx):
    await ctx.response.defer(thinking=True)
    
    with open("./data.empire", "r") as f:
        data = json.load(f)
        
    embed = discord.Embed(title="Stock Tracker")
    total = 0

    for wood in WOOD_TYPES:
        cur_price = data[wood]*get_prices(wood)['sell_offer']
        total += cur_price
        
        embed.add_field(name=format_wood_type(wood),
                        value=f"{format_coins(data[wood])} **({format_coins(cur_price)})**", inline=False)
    
    embed.add_field(name="**TOTAL**", value=f"**{format_coins(total)}**")
    
    await ctx.followup.send(embed=embed)

@tree.command(name="minionpredict", description="Predicts minion profits")
async def minionpredict(ctx, days: int):
    await ctx.response.defer(thinking=True)
    
    days *= 24 * 60 * 60
    
    MAX_COOLDOWN = 27 # seconds
    FUEL = .25 # lava bucket boost
    WOOD_PER_ACTION = 4 # 4 loga v edno durvo
    WOOD_PER_ENCH = 160 # 160 loga v 1 ench log
    DIAMOND_RATE = .1 # kolko diamanti na vseki item
    
    TIME_BETWEEN_ACTIONS = (MAX_COOLDOWN / (1 + FUEL)) * 2 # time between actions (*2 zashtoto zasqva posle seche)
    
    with open("./minions.empire", "r") as f:
        data = json.load(f)
    
    embed = discord.Embed(title="Minion Prediction")
    
    total = 0
    
    diamond_price = get_prices("ENCHANTED_DIAMOND_BLOCK")["sell_offer"]
    
    for wood, count in data.items():
        produced_items = days / TIME_BETWEEN_ACTIONS * WOOD_PER_ACTION * count / WOOD_PER_ENCH
        items_price = get_prices(wood)["sell_offer"] * produced_items
        diamonds = produced_items * WOOD_PER_ENCH * DIAMOND_RATE / WOOD_PER_ENCH / WOOD_PER_ENCH
        diamonds_price = diamond_price * diamonds
        
        total += items_price + diamonds_price
        
        embed.add_field(name=f"{count}x **{wood.title().replace('_', ' ').replace('Enchanted ', '').replace('Log', 'Minion')}**",
                        value=f"""{format_coins(produced_items)}x {format_wood_type(wood)} - **{format_coins(items_price)}**
                        {format_coins(diamonds)}x {format_wood_type('ENCHANTED_DIAMOND_BLOCK')} - **{format_coins(diamonds_price)}**""",
                        inline=False)
        
    embed.add_field(name="**TOTAL**", value=f"**{format_coins(total)}**", inline=False)
    
    await ctx.followup.send(embed=embed)

@tree.command(name="timer", description="start timer")
async def timer(ctx, days: int, message: str, channel: discord.TextChannel):
    timer_data = {
        "timestamp": time() + days*24*60*60,
        "message": message,
        "channel": channel.id
    }
        
    with open("./timers.empire", "r+") as f:
        timer_array = json.load(f)
        timer_array.append(timer_data)
        f.seek(0)
        f.write(json.dumps(timer_array))
    
    await ctx.response.send_message("Created timer.")

client.run(getenv('TOKEN'))
