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

# constants
API_KEY = "01f03fd6-8de4-4a06-bde8-3726ad9da3d1"
# PROFILE_ID = "d12ac4434e7141baaf1fa09fd60651ce"
# PLAYER_UUID = "badcaa4ac60a4f5c883b553c8a45bd63"

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
