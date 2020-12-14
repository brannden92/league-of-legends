import requests
import json
from collections import Counter

# Change these as needed
summoner_name = 'McPiece'
api_key = ''   ### Must get your own

# Get account ids from summoner name
r = requests.get(f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}')
r.json()

puuid = r.json()['puuid']
account_id = r.json()['accountId']
summoner_id = r.json()['id']

def count_roles(matches):
    '''Counts the roles played in provided matches'''
    roles = Counter(match['role'] for match in matches)
    lanes = Counter(match['lane'] for match in matches)
    return {**roles, **lanes}

# Get rank for summoner name
r1 = requests.get(f'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}')
r1.json()

# SoloQ information
soloq_tier = r1.json()[0]['tier']
soloq_div = r1.json()[0]['rank']
soloq_rank = soloq_tier +' '+ soloq_div
soloq_w = r1.json()[0]['wins']
soloq_l = r1.json()[0]['losses']
soloq_g = soloq_w + soloq_l
soloq_win_pct = round((soloq_w / soloq_g) * 100, 1)

# Flex information
flex_tier = r1.json()[1]['tier']
flex_rank = r1.json()[1]['rank']
flex_rank = flex_tier + ' ' + flex_rank
flex_w = r1.json()[1]['wins']
flex_l = r1.json()[1]['losses']
flex_g = flex_w + flex_l
flex_win_pct = round((flex_w / flex_g) * 100, 1)

# Print summary 
print('Summoner name: ' + summoner_name)
print(f'SoloQ: {soloq_rank} {soloq_win_pct}%')
print(f'Flex: {flex_rank} {flex_win_pct}%')

# Get match history for summoner name 
r2 = requests.get(f'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?api_key={api_key}')

# Get amount of games played in each role for past 100 games (includes ARAM / very inaccurate)
matches = r2.json()['matches']
roles_tally = count_roles(matches)

pct_top = round(roles_tally.get('TOP',0) / len(matches) * 100,2)
pct_jung = round(roles_tally.get('JUNGLE',0) / len(matches) * 100,2)
pct_mid = round(roles_tally.get('MID',0) / len(matches) * 100,2)
pct_adc = round(roles_tally.get('ADC',0) / len(matches) * 100,2)
pct_supp = round(roles_tally.get('SUPPORT',0) / len(matches) * 100,2)

print('Percentage of games played by role in past 100 (including ARAM):')
print(f'Top: {pct_top}')
print(f'Jungle: {pct_jung}')
print(f'Mid: {pct_mid}')
print(f'ADC: {pct_adc}')
print(f'Support: {pct_supp}')

# Get match history for past 100 games (not-ARAMs)
r5 = requests.get(f'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?queue=700&queue=400&queue=420&queue=430&api_key={api_key}')
not_aram_games = r5.json()['matches']

# Get amount of games played per role (no ARAM)
# Get amount of games played in each role for past 100 games (includes ARAM / very inaccurate)

roles_tally = count_roles(not_aram_games)

pct_top = round(roles_tally.get('TOP',0) / len(not_aram_games) * 100,2)
pct_jung = round(roles_tally.get('JUNGLE',0) / len(not_aram_games) * 100,2)
pct_mid = round(roles_tally.get('MID',0) / len(not_aram_games) * 100,2)
pct_adc = round(roles_tally.get('ADC',0) / len(not_aram_games) * 100,2)
pct_supp = round(roles_tally.get('SUPPORT',0) / len(not_aram_games) * 100,2)

print('Percentage of games played by role in past 100 (not ARAM):')
print(f'Top: {pct_top}')
print(f'Jungle: {pct_jung}')
print(f'Mid: {pct_mid}')
print(f'ADC: {pct_adc}')
print(f'Support: {pct_supp}')

#################################################
########### CLASH ANALYSIS ######################
#################################################

# Get match history for all Clash games
r3 = requests.get(f'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?queue=700&api_key={api_key}')
clash_hist = r3.json()['matches']
roles_tally = count_roles(clash_hist)

pct_top = round(roles_tally.get('TOP',0) / len(clash_hist) * 100,2)
pct_jung = round(roles_tally.get('JUNGLE',0) / len(clash_hist) * 100,2)
pct_mid = round(roles_tally.get('MID',0) / len(clash_hist) * 100,2)
pct_adc = round(roles_tally.get('ADC',0) / len(clash_hist) * 100,2)
pct_supp = round(roles_tally.get('SUPPORT',0) / len(clash_hist) * 100,2)

print('Percentage of games played by role in Clash:')
print(f'Top: {pct_top}')
print(f'Jungle: {pct_jung}')
print(f'Mid: {pct_mid}')
print(f'ADC: {pct_adc}')
print(f'Support: {pct_supp}')

roles, lanes = [], []
for i in range(0, 10):                # fix if range cant reach 10
    role = clash_hist[i]['role']
    roles.append(role)
    lane = clash_hist[i]['lane']
    lanes.append(lane)
    
num_supp = roles.count('DUO_SUPPORT')
num_adc = roles.count('DUO_CARRY')
num_mid = lanes.count('MID')
num_jung = lanes.count('JUNGLE')
num_top = lanes.count('TOP')

print(f'Last 10 Clash games played for {summoner_name}:')
print(f'Top: {num_top}')
print(f'Jungle: {num_jung}')
print(f'Mid": {num_mid}')
print(f'ADC: {num_adc}')
print(f'Support: {num_supp}')

###################################################
############# SPECIFIC MATCH DETAILS ##############
###################################################

game_id = 3665709273

r4 = requests.get(f'https://na1.api.riotgames.com/lol/match/v4/matches/{game_id}?api_key={api_key}')
game_details = r4.json()

stats = []
for i in range(10):
    stats.append({
        'name': game_details['participantIdentities'][i]['player']['summonerName'],
        'kill': game_details['participants'][i]['stats']['kills'],
        'death': game_details['participants'][i]['stats']['deaths'],
        'assist': game_details['participants'][i]['stats']['assists'],
        'win': game_details['participants'][i]['stats']['win'],
        'champ': game_details['participants'][i]['championId']
    })
    
print(json.dumps(stats, indent=2))