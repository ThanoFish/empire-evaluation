import requests
import json

# functions
def get_slots(crafted_minions, comm_upgrades):
    SLOT_REQS = [0, 5, 15, 30, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 350, 400, 450, 500, 550, 600]

    # get amount of minion slots obtained for craftinf more minions
    for i in range(len(SLOT_REQS)):
        if SLOT_REQS[i] > crafted_minions:
            slots_from_crafting = i - 1
            break

    # get amount of minion slots obtained from community upgrades
    slots_from_comm_upgrades = 0
    for i in comm_upgrades['upgrade_states']:
       if i['upgrade'] == "minion_slots" and i['tier'] > slots_from_comm_upgrades:
           slots_from_comm_upgrades = i['tier']
    
    # 5 is the default amount of minion slots
    return slots_from_crafting + slots_from_comm_upgrades + 5

def get_prices(item):
    bazaar = json.loads(requests.get('https://api.hypixel.net/skyblock/bazaar').text)
    
    sell_offer = bazaar['products'][item]['buy_summary'][0]['pricePerUnit'] # get first sell offer price
    insta_sell = bazaar['products'][item]['sell_summary'][0]['pricePerUnit'] # get first insta sell price
    spread = sell_offer - insta_sell
    
    return {
        'sell_offer': sell_offer,
        'insta_sell': insta_sell,
        'spread': spread,
    }

def get_minion_data(profile_id, player_id, key):
    data = json.loads(
    requests.get(f"https://api.hypixel.net/skyblock/profile?key={key}&profile={profile_id}").text
    )
    
    crafted_minions = len(data['profile']['members'][player_id]['crafted_generators'])
    
    slots = get_slots(crafted_minions, data['profile']['community_upgrades'])
    
    return {
        "crafted": crafted_minions,
        "slots": slots
    }

def get_bazaar_instabuy(item):
    if "WOOD_" in item: return 0  
    return requests.get(f"https://api.hypixel.net/skyblock/bazaar").json()["products"][item]["sell_summary"][0]["pricePerUnit"]

def get_minion_craft_cost(minion):
    repo = "https://raw.githubusercontent.com/NotEnoughUpdates/NotEnoughUpdates-REPO/master/items/"
    
    cost = {}
    
    for item in requests.get(repo + minion + ".json").json()["recipe"].values():
        item_type, count = item.split(":")
        if "_GENERATOR_" in item_type:
            parent_cost = get_minion_craft_cost(item_type)
            for x in parent_cost:
                cost.setdefault(x, 0)
                cost[x] += parent_cost[x]
            continue
        cost.setdefault(item_type, 0)
        cost[item_type] += int(count)
    
    return cost