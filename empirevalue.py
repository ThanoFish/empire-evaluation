import discord
from discord import app_commands
from skyblockapiquery import get_prices, get_minion_data, get_minion_craft_cost, get_bazaar_instabuy
from helper import format_coins
import random
from dotenv import load_dotenv
import os
import sys

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

load_dotenv()

api_key = os.getenv('API_KEY')

@client.event
async def on_ready():
    print("Ready!")


@tree.command(name="test", description="replys omg")
async def test(ctx, arg: str):
    await ctx.response.send_message(arg + "1")


@tree.command(name="sync", description="syncs commands")
async def sync(ctx):
    if (ctx.user.id == 700998149170397305):
        await tree.sync()
        await ctx.response.send_message("Done!")
    else:
        await ctx.response.send_message("You can't use this command!")
        
@tree.command(name="reset")
async def reset(ctx):
    if (ctx.user.id != 700998149170397305): return
    os.execv(sys.executable, ["python"] + sys.argv)


@tree.command(name="empirestats", description="get info about the stats of THE EMPIRE")
async def empirestats(ctx: discord.Interaction):
    embed = discord.Embed(
        title="THE EMPIRE BUSINESS"
    )

    minion_data = get_minion_data(
        "d12ac4434e7141baaf1fa09fd60651ce", "badcaa4ac60a4f5c883b553c8a45bd63", api_key)

    embed.add_field(name="Crafted minions:",
                    value=minion_data["crafted"], inline=False)
    embed.add_field(name="Minion slots:",
                    value=minion_data["slots"], inline=False)

    WOOD_TYPES = ['ENCHANTED_ACACIA_LOG', 'ENCHANTED_BIRCH_LOG', 'ENCHANTED_DARK_OAK_LOG',
                  'ENCHANTED_JUNGLE_LOG', 'ENCHANTED_OAK_LOG', 'ENCHANTED_SPRUCE_LOG']

    WOOD_TYPES = sorted(WOOD_TYPES, key=lambda x: get_prices(x)["sell_offer"], reverse=True)

    for i in WOOD_TYPES:
        info = get_prices(i)

        embed.add_field(name=i.title().replace("_", " "), value=f"""
                        Sell offer: {info["sell_offer"]}
                        Insta sell: {info["insta_sell"]}
                        Spread: {round(info["spread"], 1)}
                        """, inline=False)

    embed.add_field(name="Gigachad?:", value=(
        "Yes 🥶" if random.random() < 0.968 else "No 💀"))

    await ctx.response.send_message(embed=embed)


@tree.command(name="isgigachad", description="Checks if the empire is gigachad or not")
async def isgigachad(ctx):
    await ctx.response.send_message("Yes 🥶" if random.random() < 0.968 else "No 💀")

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
    
    await ctx.response.send_message(message)

client.run(os.getenv('TOKEN'))
