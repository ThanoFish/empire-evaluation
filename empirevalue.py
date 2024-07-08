import discord
from discord import app_commands
from skyblockapiquery import get_prices, get_minion_data
import random
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

<<<<<<< HEAD
=======
load_dotenv()

api_key = os.getenv('API_KEY')
>>>>>>> b5413a0 (amogus)

@client.event
async def on_ready():
    print("Ready!")


@tree.command(name="test", description="replys omg")
async def test(ctx, arg: str):
    await ctx.response.send_message(arg)


@tree.command(name="sync", description="syncs commands")
async def sync(ctx):
    if (ctx.user.id == 700998149170397305):
        await tree.sync()
        await ctx.response.send_message("Done!")
    else:
        await ctx.response.send_message("You can't use this command!")


@tree.command(name="empirestats", description="get info about the stats of THE EMPIRE")
<<<<<<< HEAD
async def empirestats(ctx: discord.Interaction, api_key: str):
=======
async def empirestats(ctx: discord.Interaction):
>>>>>>> b5413a0 (amogus)
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

<<<<<<< HEAD
    for i in WOOD_TYPES:
        info = get_prices(i)

        embed.add_field(name=i, value=f"""
=======
    WOOD_TYPES = sorted(WOOD_TYPES, key=lambda x: get_prices(x)["sell_offer"], reverse=True)

    for i in WOOD_TYPES:
        info = get_prices(i)

        embed.add_field(name=i.title().replace("_", " "), value=f"""
>>>>>>> b5413a0 (amogus)
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
<<<<<<< HEAD
Price per stock: 34 coins
Total value: 340 000 000 coins
=======
Price per stock: 34 000 000 000 000 coins
Total value: 340 000 000 000 000 000 000 coins
>>>>>>> b5413a0 (amogus)

(updates once every 2 hours)
                                    """)

<<<<<<< HEAD
load_dotenv()
=======
>>>>>>> b5413a0 (amogus)

client.run(os.getenv('TOKEN'))
