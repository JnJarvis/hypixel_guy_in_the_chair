import requests
import json
from pprint import pprint
import pyperclip
import time
import hypixel

API_KEY = 'f0cf4f20-3aea-44d7-9820-dc9a80b28c82'
PLAYER_NAME = '7b9ee1ea-3fea-4649-87a3-e726f7165534'
hypixel.setKeys([API_KEY])
print("success!!")
"""
['slumber', 'games_played_bedwars_1', 'packages', 'coins', 'Experience', 'first_join_7', 'favourites_2', 'beds_lost_bedwars', 'entity_attack_final_deaths_bedwars', 'entity_attack_kills_bedwars', 'final_deaths_bedwars', 'games_played_bedwars', 'gold_resources_collected_bedwars', 'iron_resources_collected_bedwars', 'kills_bedwars', 'losses_bedwars', 'resources_collected_bedwars', 'void_final_deaths_bedwars', '_items_purchased_bedwars', 'deaths_bedwars', 'diamond_resources_collected_bedwars', 'emerald_resources_collected_bedwars', 'items_purchased_bedwars', 'permanent_items_purchased_bedwars', 'void_deaths_bedwars', 'magic_deaths_bedwars', 'entity_attack_deaths_bedwars', 'fall_kills_bedwars', 'projectile_kills_bedwars', 'void_kills_bedwars', 'magic_final_deaths_bedwars', 'favorite_slots', 'practice', 'entity_attack_final_kills_bedwars', 'final_kills_bedwars', 'winstreak', 'wins_bedwars', 'fire_tick_final_deaths_bedwars', 'fall_final_kills_bedwars', 'void_final_kills_bedwars', 'entity_explosion_kills_bedwars', 'fall_final_deaths_bedwars', 'selected_challenge_type', 'beds_broken_bedwars', 'fall_deaths_bedwars', 'activeDeathCry', 'entity_explosion_final_deaths_bedwars', 'entity_explosion_deaths_bedwars', 'fire_tick_kills_bedwars', 'projectile_final_kills_bedwars', 'magic_final_kills_bedwars', 'projectile_deaths_bedwars', 'activeKillMessages', 'activeKillEffect', 'activeProjectileTrail', 'selected_ultimate', 'magic_kills_bedwars', 'fire_tick_final_kills_bedwars', 'fire_final_deaths_bedwars', 'fire_deaths_bedwars', 'understands_resource_bank', 'understands_streaks', 'fire_tick_deaths_bedwars', 'shop_sort_enable_owned_first']
"""
def get_bedwars_stats(uuid):
    player = hypixel.Player(uuid)
    name = player.getName()
    rank = player.getRank()
    data = player.JSON['stats']['Bedwars']
    try:
        data["projectile_kills_bedwars"]
    except Exception:
        data['projectile_kills_bedwars'] = 0.0000000000000000000000000001
        data['projectile_deaths_bedwars']=1
    r = f"[{rank['rank']}] " if rank["rank"]!="Non" else ""
    skill = (data['wins_bedwars']/data['losses_bedwars']*20) + (data['kills_bedwars']/data['deaths_bedwars']*20) + (data['final_kills_bedwars']/data['final_deaths_bedwars']*20) \
            + (data['void_kills_bedwars']/data['void_deaths_bedwars']*20) + (min(data['projectile_kills_bedwars']/data['projectile_deaths_bedwars']*10,10)) + (data['beds_broken_bedwars']/data["beds_lost_bedwars"]*10) \
            + 0
    stringy = f"""Player: {r}{name}
-------------------------------
Total number of games played: {data['games_played_bedwars_1']}
Total number of games won: {data['wins_bedwars']}
Total number of games lost: {data['losses_bedwars']}
Total number of players killed: {data['kills_bedwars']}
Total number of final kills: {data['final_kills_bedwars']}
Total number of deaths: {data['deaths_bedwars']}
Total number of final deaths: {data['final_deaths_bedwars']}
Total number of projectile kills: {data['projectile_kills_bedwars']+data['projectile_final_kills_bedwars']}
Total number of projectile deaths: {data['projectile_deaths_bedwars']}
Total number of beds destroyed: {data['beds_broken_bedwars']}
Total number of beds lost: {data["beds_lost_bedwars"]}
Total number of void kills: {data['void_kills_bedwars']}
Total number of void deaths: {data['void_deaths_bedwars']}
Total number of fall deaths: {data['fall_deaths_bedwars']}
Total number of fall kills: {data['fall_kills_bedwars']}

Win to Loss ratio: {data['wins_bedwars']/data['losses_bedwars']}
Kill to Death ratio: {data['kills_bedwars']/data['deaths_bedwars']}
Final Kill to Death ratio: {data['final_kills_bedwars']/data['final_deaths_bedwars']}
Void Kill to Death ratio: {data['void_kills_bedwars']/data['void_deaths_bedwars']}
Projectile Kill to Death ratio: {(data['projectile_kills_bedwars']+data['projectile_final_kills_bedwars'])/data['projectile_deaths_bedwars']}
Fall Kill to Death ratio: {data['fall_kills_bedwars']/data['fall_deaths_bedwars']}

Average number of deaths per game: {data['deaths_bedwars']/data['games_played_bedwars_1']}
Average number of kills per game: {data['kills_bedwars']/data['games_played_bedwars_1']}
Average number of final kills per game: {data['final_kills_bedwars']/data['games_played_bedwars_1']}

Average number of void deaths per game: {data['void_deaths_bedwars']/data['games_played_bedwars_1']}
Average number of projectile kills per game: {(data['projectile_kills_bedwars']+data['projectile_final_kills_bedwars'])/data['games_played_bedwars_1']}
Average number of fall kills per game: {data['fall_kills_bedwars']/data['games_played_bedwars_1']}


Overall skill rating: {skill}

"""
    return stringy

def get_uuid_api(username):
    api_url_base = 'https://api.mojang.com/users/profiles/minecraft/' + username
    response = requests.get(f"{api_url_base}")
    if response.status_code == 404:
        return "Username is not registered, its free or Input is Illegal"

    else:
        uuid = json.dumps(response.json())
        uuid_hyphen = uuid[:16] + '-' + uuid[16:20] + '-' + uuid[20:24] + '-' + uuid[24:28] + '-' + uuid[28:]
        return uuid_hyphen
        #return json.dumps(response.json())


def parse_who_command(txt:str):
    
    try:
        if txt.startswith("ONLINE:"):
            txt = txt.removeprefix("ONLINE:")
            players = txt.split(",")
            uuids = [eval(get_uuid_api(player.replace(" ",""))) for player in players]
            return uuids
        else:return []
    except:
        return []

def on_clipboard_change(text):
    uuids = parse_who_command(text)
    # print(uuids)
    for uuid in uuids:
        try:
            print(get_bedwars_stats(uuid["id"]))
        except Exception as e:print("couldn't get the User Data.",e)


previous_text = ""
# pyperclip.copy(previous_text)
# while True:
#     current_text = pyperclip.paste()
#     if current_text != previous_text:
#         on_clipboard_change(current_text)
#         previous_text = current_text
#     time.sleep(1)
print(on_clipboard_change("ONLINE: Shades1984, warshock1181, iron_anarchist"))