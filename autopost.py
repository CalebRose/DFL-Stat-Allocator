# Extract CSVs and Post results to games forum
# Imports
import requests
import config
import os
from csv import reader
from csv import DictReader
# Reader - lets you iterate
# DictReader

message = ""
stadium = ""
location = ""
gaps = (7, 42, 43, 79, 80, 81, 82, 118, 119)
# Tuples to hold the different offensive plays to run
pass_plays = ('Slants', 'Flood', 'Scissors', 'Play Action',
              'Screen Pass', 'Max Protect', 'Streaks')
rush_plays = ('Blast', 'Power', 'Draw', 'Sweep', 'Option')
offensive_penalties = ('Offense: Delay of Game', 'Offense: False Start', 'Offense: Illegal Formation',
                       'Offense: Holding', 'Offense: Unnecessary Roughness', 'Offense: Pass Interference')
defensive_penalties = ('Defense: Pass Interference', 'Defense: Roughing the Passer', 'Defense: Unnecessary Roughness',
                       'Defense: Face Mask', 'Defense: Illegal Use of Hands', 'Defense: Holding', 'Defense: Offsides', 'Defense: Encroachment')


def score_allocator(team, iterator, points):
    if(iterator <= 42):
        team['q1_score'] += points
    elif(iterator <= 79):
        team['q2_score'] += points
    elif(iterator <= 118):
        team['q3_score'] += points
    else:
        team['q4_score'] += points


def play_allocation(offense, defense, row, iterator):
    #
    play = row[2]
    pass_play = False
    rush_play = False
    # kickoff = row[4]
    p_yds = int(row[8])
    incomplete = row[9]
    r_yds = int(row[10])
    k_yards = int(row[11])
    punt_yards = int(row[12])
    ret_yrds = int(row[13])
    sack = row[14]
    fg = row[15]
    td = row[16]
    saf = row[17]
    inter = row[18]
    fum = row[19]
    turnover = row[20]
    minor_injury = row[21]
    major_injury = row[22]
    injury = row[23]
    penalty = row[24]
    penalty_type = row[25]
    penalty_yards = int(row[26])
    was_accepted = row[27]
    # Pass Play
    if(play in pass_plays):
        pass_play = True
        offense['passing'] += p_yds
        if((incomplete == 'False' or incomplete == 'FALSE') and (sack == 'False' or sack == 'FALSE')):
            offense['p_completions'] += 1
        if(sack == 'True' or sack == 'TRUE'):
            offense['sck'] += 1
        else:
            offense['p_attempts'] += 1
        if(inter == 'True' or inter == 'TRUE'):
            offense['int'] += 1
        if(offense['p_attempts'] != 0):
            offense['cmp_percent'] = round(100 * (
                offense['p_completions'] / offense['p_attempts']), 2)
    # Rush Play
    elif(play in rush_plays):
        rush_play = True
        offense['rushing'] += r_yds
        if(was_accepted == 'False' or was_accepted == 'FALSE'):
            offense['r_att'] += 1
        if(offense['r_att'] != 0):
            offense['r_yds_att'] = round(
                (offense['rushing']/offense['r_att']), 2)
        if(fum == 'True'):
            offense['fum'] += 1
            if(turnover == 'True'):
                offense['lost'] += 1

    # Special Teams
    elif((play == 'Kickoff' or play == 'Punt') or (play == 'KICKOFF' or play == 'PUNT')):
        if(play == 'Kickoff'):
            offense['kickoff_yds'] += k_yards
        elif(play == 'Punt'):
            offense['punts'] += 1
            offense['punt_yds'] += punt_yards
            offense['punt_avg'] = round((offense['punt_yds'] /
                                         offense['punts']), 2)
            # Calculate Away Team Return Yards
            defense['rtn_yds'] += ret_yrds
            defense['rtn'] += 1
            defense['rtn_avg'] = round((defense['rtn_yds'] /
                                        defense['rtn']), 2)
    elif(play == 'Field Goal' or play == 'FIELD GOAL'):
        # If the FG is an extra point
        if(offense['xp'] == True):
            if(fg == 'True' or fg == 'TRUE'):
                score_allocator(offense, iterator, 1)
                offense['xpm'] += 1
            offense['xpa'] += 1
            offense['xp_percent'] = round(
                100 * (offense['xpm'] / offense['xpa']), 2)
            offense['xp'] = False
        # Else, it's just a field goal for 3
        else:
            if(fg == 'True' or fg == 'TRUE'):
                score_allocator(offense, iterator, 3)
                offense['fgm'] += 1
            offense['fga'] += 1
            offense['fg_percent'] = round(
                100 * (offense['fgm'] / offense['fga']), 2)
    # Touchdown Made
    if(td == 'True' or td == 'TRUE'):
        if(pass_play == True):
            offense['p_td'] += 1
        elif(rush_play == True):
            offense['r_td'] += 1
        score_allocator(offense, iterator, 6)
        pass_play = False
        rush_play = False
        offense['xp'] = True

    # Penalty Occurring
    if((penalty == 'True' and was_accepted == 'True') or (penalty == 'TRUE' and was_accepted == 'TRUE')):
        if(penalty_type in offensive_penalties):
            offense['pen'] = offense['pen'] + 1
            offense['pen_yds'] += abs(penalty_yards)
        elif(penalty_type in defensive_penalties):
            defense['pen'] = defense['pen'] + 1
            defense['pen_yds'] += abs(penalty_yards)

    # Safety
    if(saf == 'True' or saf == 'TRUE'):
        offense['saf'] += 1


def time_indicator(time):
    if(time == "830PM"):
        return "8:30PM"
    elif(time == "100PM"):
        return "1:00PM"
    else:
        return "4:00PM"


# ==================================================
# Modify the Week and the Time before running script.
# Confirm that the proper folders are in the correct path
week = "8"
time = "830PM"
time_title = time_indicator(time)
file_path = config.file_path
directory_path = f'{file_path}\\W7{time}'
# ==================================================

directory = os.path.join(directory_path)
for root, dirs, files in os.walk(directory):
    print(files)
    for file in files:
        home_team = {
            "location": "",
            "mascot": "",
            "team": "",
            "abbreviation": "",
            "score": 0,
            "record": "",
            "passing": 0,
            "p_attempts": 0,
            "p_completions": 0,
            "cmp_percent": 0,
            "p_td": 0,
            "int": 0,
            "sck": 0,
            "rushing": 0,
            "r_att": 0,
            "r_yds_att": 0,
            "r_td": 0,
            "fum": 0,
            "lost": 0,
            "xp": False,
            "xpm": 0,
            "xpa": 0,
            "xp_percent": 0,
            "fgm": 0,
            "fga": 0,
            "fg_percent": 0,
            "kr_td": 0,
            "punts": 0,
            "punt_yds": 0,
            "punt_avg": 0,
            "kickoff_yds": 0,
            "rtn": 0,
            "rtn_yds": 0,
            "rtn_avg": 0,
            "pr_td": 0,
            "saf": 0,
            "pen": 0,
            "pen_yds": 0,
            "q1_score": 0,
            "q2_score": 0,
            "q3_score": 0,
            "q4_score": 0
        }
        away_team = {
            "location": "",
            "mascot": "",
            "team": "",
            "abbreviation": "",
            "score": 0,
            "record": "",
            "passing": 0,
            "p_attempts": 0,
            "p_completions": 0,
            "cmp_percent": 0,
            "p_td": 0,
            "int": 0,
            "sck": 0,
            "rushing": 0,
            "r_att": 0,
            "r_yds_att": 0,
            "r_td": 0,
            "fum": 0,
            "lost": 0,
            "xp": False,
            "xpm": 0,
            "xpa": 0,
            "xp_percent": 0,
            "fgm": 0,
            "fga": 0,
            "fg_percent": 0,
            "kr_td": 0,
            "punts": 0,
            "punt_yds": 0,
            "punt_avg": 0,
            "kickoff_yds": 0,
            "rtn": 0,
            "rtn_yds": 0,
            "rtn_avg": 0,
            "pr_td": 0,
            "saf": 0,
            "pen": 0,
            "pen_yds": 0,
            "q1_score": 0,
            "q2_score": 0,
            "q3_score": 0,
            "q4_score": 0
        }
        print(file)
        if(file.endswith('csv')):
            f = open(directory + '\\' + file)
            iterator = 0
            csv_r = reader(f)
            for row in csv_r:
                if(iterator <= 6):
                    if(row[0] == 'Home Team:'):
                        home_team['team'] = row[1]
                        home_team['score'] = row[2]
                        home_team['record'] = row[3]
                        home_team['location'] = row[4]
                        home_team['mascot'] = row[5]
                    elif(row[0] == 'Away Team:'):
                        away_team['team'] = row[1]
                        away_team['score'] = row[2]
                        away_team['record'] = row[3]
                        away_team['location'] = row[4]
                        away_team['mascot'] = row[5]
                    elif(row[0] == 'Stadium:'):
                        stadium = row[1]
                        location = row[2]
                # If the iterator is not at the beginning or within the gaps of the CSV format
                # Allocate Stats
                elif(iterator > 6):
                    # Home Team
                    if(len(row) <= 2):
                        iterator += 1
                        continue
                    if(row[1] == home_team['team']):
                        # Offense = Home Team; Defense = Away Team
                        play_allocation(home_team, away_team, row, iterator)
                    # If the team is the AWAY team
                    elif(row[1] == away_team['team']):
                        # Offense = Away Team; Defense = Home Team
                        play_allocation(away_team, home_team, row, iterator)
                iterator += 1
        print("##########################")
        print("Home: ")
        print(home_team)
        print("\n##########################")
        print("Away: ")
        print(away_team)
        print("\n##########################")
        f.close()
        template = f"[CENTER][SIZE=6]{away_team['location']} {away_team['mascot']} ({away_team['record']}) at {home_team['location']} {home_team['mascot']} ({home_team['record']}) [/SIZE]\n[SIZE=3]{stadium} -- {location}[/SIZE][/CENTER]\n\n[TABLE][TR][TH]Team[/TH][TH]Q1[/TH][TH]Q2[/TH][TH]Q3[/TH][TH]Q4[/TH][TH]Final[/TH][/TR][TR][TD]{home_team['location']}[/TD][TD]{home_team['q1_score']}[/TD][TD]{home_team['q2_score']}[/TD][TD]{home_team['q3_score']}[/TD][TD]{home_team['q4_score']}[/TD][TD]{home_team['score']}[/TD][/TR][TR][TD]{away_team['location']}[/TD][TD]{away_team['q1_score']}[/TD][TD]{away_team['q2_score']}[/TD][TD]{away_team['q3_score']}[/TD][TD]{away_team['q4_score']}[/TD][TD]{away_team['score']}[/TD][/TR][/TABLE]\n[CENTER]\n[B][U][SIZE=6]Match Stats[/SIZE][/U]\n\nPassing[/B][/CENTER]\n[TABLE][TR][TH][CENTER]Team[/CENTER][/TH][TH]CMP[/TH][TH]ATT[/TH][TH]CMP % [/TH][TH]YDS[/TH][TH]TD[/TH][TH]INT[/TH][TH]SK[/TH][/TR][TR][TD]{home_team['location']}[/TD][TD]{home_team['p_completions']}[/TD][TD]{home_team['p_attempts']}[/TD][TD]{home_team['cmp_percent']}%[/TD][TD]{home_team['passing']}[/TD][TD]{home_team['p_td']}[/TD]\n[TD]{home_team['int']}[/TD][TD]{home_team['sck']}[/TD][/TR][TR][TD]{away_team['location']}[/TD][TD]{away_team['p_completions']}[/TD][TD]{away_team['p_attempts']}[/TD][TD]{away_team['cmp_percent']}%[/TD][TD]{away_team['passing']}[/TD][TD]{away_team['p_td']}[/TD][TD]{away_team['int']}[/TD][TD]{away_team['sck']}[/TD][/TR][/TABLE]\n[CENTER][B]Rushing[/B][/CENTER]\n[TABLE][TR][TH]Team[/TH][TH]ATT[/TH][TH]YDS[/TH][TH]YDS/ATT[/TH][TH]TD[/TH][TH]FUM[/TH][TH]LOST[/TH][/TR][TR][TD]{home_team['location']}[/TD][TD]{home_team['r_att']}[/TD][TD]{home_team['rushing']}[/TD][TD]{home_team['r_yds_att']}[/TD][TD]{home_team['r_td']}[/TD][TD]{home_team['fum']}[/TD][TD]{home_team['lost']}[/TD][/TR][TR][TD]{away_team['location']}[/TD][TD]{away_team['r_att']}[/TD][TD]{away_team['rushing']}[/TD][TD]{away_team['r_yds_att']}[/TD][TD]{away_team['r_td']}[/TD][TD]{away_team['fum']}[/TD][TD]{away_team['lost']}[/TD][/TR][/TABLE]\n\n[CENTER][B]Kicking[/B][/CENTER]\n[TABLE][TR][TH]Team[/TH][TH]XPM[/TH][TH]XPA[/TH][TH]XP % [/TH][TH]FGM[/TH][TH]FGA[/TH][TH]FG % [/TH][TH]KR TD[/TH][/TR][TR][TD]{home_team['location']}[/TD][TD]{home_team['xpm']}[/TD][TD]{home_team['xpa']}[/TD][TD]{home_team['xp_percent']}%[/TD][TD]{home_team['fgm']}[/TD][TD]{home_team['fga']}[/TD][TD]{home_team['fg_percent']}%[/TD][TD]{home_team['kr_td']}[/TD][/TR][TR][TD]{away_team['location']}[/TD][TD]{away_team['xpm']}[/TD][TD]{away_team['xpa']}[/TD][TD]{away_team['xp_percent']}%[/TD][TD]{away_team['fgm']}[/TD][TD]{away_team['fga']}[/TD][TD]{away_team['fg_percent']}%[/TD][TD]{away_team['kr_td']}[/TD][/TR][/TABLE]\n\n[CENTER][B]Punting[/B][/CENTER]\n[TABLE][TR][TH]Team[/TH][TH]PUNTS[/TH][TH]PUNT YDS[/TH][TH]PUNT AVG[/TH][TH]RTN[/TH][TH]RTN YDS[/TH][TH]RTN AVG[/TH][TH]PR TD[/TH][/TR][TR][TD]{home_team['location']}[/TD][TD]{home_team['punts']}[/TD][TD]{home_team['punt_yds']}[/TD][TD]{home_team['punt_avg']}[/TD][TD]{home_team['rtn']}[/TD][TD]{home_team['rtn_yds']}[/TD][TD]{home_team['rtn_avg']}[/TD][TD]{home_team['pr_td']}[/TD][/TR][TR][TD]{away_team['location']}[/TD][TD]{away_team['punts']}[/TD][TD]{away_team['punt_yds']}[/TD][TD]{away_team['punt_avg']}[/TD][TD]{away_team['rtn']}[/TD][TD]{away_team['rtn_yds']}[/TD][TD]{away_team['rtn_avg']}[/TD][TD]{away_team['pr_td']}[/TD][/TR][/TABLE]\n\n[CENTER][B]Other[/B][/CENTER]\n[TABLE][TR][TH]Team[/TH][TH]SAF[/TH][TH]PEN[/TH][TH]PEN YDS[/TH][/TR][TR][TD]{home_team['location']}[/TD][TD]{home_team['saf']}[/TD][TD]{home_team['pen']}[/TD][TD]{home_team['pen_yds']}[/TD][/TR][TR][TD]{away_team['location']}[/TD][TD]{away_team['saf']}[/TD][TD]{away_team['pen']}[/TD][TD]{away_team['pen_yds']}[/TD][/TR][/TABLE]\n\nPlay-by-Play: "
        message += template + "\n\n\n\n"

print(message)
app = "application/json"
key = config.key
user = config.user
payload = {
    "Content-Type": "application/x-www-form-urlencoded",
    "XF-Api-Key": key,
    "XF-Api-User": user
}
params = {
    "node_id": 123,
    "title": f"Week {week}, {time_title}",
    "message": message,
    "discussion_open": True,
    "tags": ["Week3"]
}
url = "https://www.simfba.com/index.php?api/threads/"

res = requests.post(url, headers=payload, data=params)
print("RES SENT")
print(res)
print(res.json())
print("============ Game Posted ============")
