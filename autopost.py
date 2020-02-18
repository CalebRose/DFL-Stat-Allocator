# Extract CSVs and Post results to games forum
# Imports
import requests
from csv import reader
from csv import DictReader
# Reader - lets you iterate
# DictReader

home_team = {
    "team": "",
    "score": 0,
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
    "team": "",
    "score": 0,
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

stadium = ""
location = ""
iterator = 0
gaps = (7, 42, 43, 79, 80, 81, 82, 118, 119)
# Tuples to hold the different offensive plays to run
pass_plays = ('Slants', 'Flood', 'Scissors', 'Play Action',
              'Screen Pass', 'Max Protect', 'Streaks')
rush_plays = ('Blast', 'Power', 'Draw', 'Sweep', 'Option')
offensive_penalties = ('Offense: Delay of Game', 'Offense: False Start', 'Offense: Illegal Formation', 'Offense: Holding', 'Offense: Unnecessary Roughness', 'Offense: Pass Interference')
defensive_penalties = ('Defense: Pass Interference', 'Defense: Roughing the Passer', 'Defense: Unnecessary Roughness', 'Defense: Face Mask', 'Defense: Illegal Use of Hands', 'Defense: Holding', 'Defense: Offsides', 'Defense: Encroahment')


def score_allocator(team, iterator, points):
    if(iterator < 42):
        team['q1_score'] += points
    elif(iterator < 79):
        team['q2_score'] += points
    elif(iterator < 118):
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
        if(incomplete == 'False'):
            offense['p_completions'] += 1
        if(sack == 'True'):
            offense['sck'] += 1
        else:
            offense['p_attempts'] += 1
        if(inter == 'True'):
            offense['int'] += 1
        offense['cmp_percent'] = round(100 * (
            offense['p_completions'] / offense['p_attempts']), 2)
    # Rush Play
    elif(play in rush_plays):
        rush_play = True
        offense['rushing'] += r_yds
        if(was_accepted == 'False'):
            offense['r_att'] += 1
        if(offense['r_att'] != 0):
            offense['r_yds_att'] = round(
                (offense['rushing']/offense['r_att']), 2)
        if(fum == 'True'):
            offense['fum'] += 1
            if(turnover == 'True'):
                offense['lost'] += 1

    # Special Teams
    elif(play == 'Kickoff' or play == 'Punt'):
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

    # Touchdown Made
    if(td == 'True'):
        if(pass_play == True):
            offense['p_td'] += 1
        elif(rush_play == True):
            offense['r_td'] += 1
        score_allocator(offense, iterator, 6)
        pass_play = False
        rush_play = False
        offense['xp'] = True
    if(play == 'Field Goal'):
        # If the FG is an extra point
        if(offense['xp'] == True):
            if(fg == 'True'):
                score_allocator(offense, iterator, 1)
                offense['xpm'] += 1
            offense['xpa'] += 1
            offense['xp_percent'] = round(
                100 * (offense['xpm'] / offense['xpa']), 2)
            offense['xp'] = False
        # Else, it's just a field goal for 3
        else:
            if(fg == 'True'):
                score_allocator(offense, iterator, 3)
                offense['fgm'] += 1
            offense['fga'] += 1
            offense['fg_percent'] = round(
                100 * (offense['fgm'] / offense['fga']), 2)

    # Penalty Occurring
    if(penalty == 'True' and was_accepted == 'True'):
        if(penalty_type in offensive_penalties):
            offense['pen'] = offense['pen'] + 1
            offense['pen_yds'] += abs(penalty_yards)
        elif(penalty_type in defensive_penalties):
            defense['pen'] = defense['pen'] + 1
            defense['pen_yds'] += abs(penalty_yards)

    # Safety
    if(saf == 'True'):
        offense['saf'] += 1


with open("CSV\\W3100PM\\BGP@NYC.csv") as file:
    csv_reader = reader(file)
    for row in csv_reader:
        if(iterator <= 6):
            if(row[0] == 'Home Team:'):
                home_team['team'] = row[1]
                home_team['score'] = row[2]
            elif(row[0] == 'Away Team:'):
                away_team['team'] = row[1]
                away_team['score'] = row[2]
            elif(row[0] == 'Stadium:'):
                stadium = row[1]
                location = row[2]
        # If the iterator is not at the beginning or within the gaps of the CSV format
        # Allocate Stats
        elif(iterator > 6):
            # Home Team
            if(len(row) <= 2):
                continue
            if(row[1] == home_team['team']):
                # Offense = Home Team; Defense = Away Team
                play_allocation(home_team, away_team, row, iterator)
            # If the team is the AWAY team
            elif(row[1] == away_team['team']):
                # Offense = Away Team; Defense = Home Team
                play_allocation(away_team, home_team, row, iterator)
        iterator += 1
        # print(row)
template = f"[CENTER][SIZE=6]{home_team['team']} (0-0) vs {away_team['team']} (0-0)[/SIZE]\n[SIZE=3]{stadium} - - {location}[/SIZE][/CENTER]\n\n[TABLE]\n[TR]\n[TH]Team[/TH]\n[TH]Q1[/TH]\n[TH]Q2[/TH]\n[TH]Q3[/TH]\n[TH]Q4[/TH]\n[TH]Final[/TH]\n[/TR]\n[TR]\n[TD]{home_team['team']}[/TD]\n[TD]{home_team['q1_score']}[/TD]\n\n[TD]{home_team['q2_score']}[/TD]\n\n[TD]{home_team['q3_score']}[/TD]\n\n[TD]{home_team['q4_score']}[/TD]\n\n[TD]{home_team['score']}[/TD]\n[/TR]\n[TR]\n[TD]{away_team['team']}[/TD]\n\n[TD]{away_team['q1_score']}[/TD]\n\n[TD]{away_team['q2_score']}[/TD]\n\n[TD]{away_team['q3_score']}[/TD]\n\n[TD]{away_team['q4_score']}[/TD]\n\n[TD]{away_team['score']}[/TD]\n[/TR]\n[/TABLE]\n[CENTER]\n[B][U][SIZE=6]Match Stats[/SIZE][/U]\n\nPassing[/B][/CENTER]\n\n[TABLE]\n[TR]\n[TH][CENTER]Team[/CENTER][/TH]\n\n[TH]CMP[/TH]\n[TH]ATT[/TH]\n[TH]CMP % [/TH]\n[TH]YDS[/TH]\n[TH]TD[/TH]\n[TH]INT[/TH]\n[TH]SK[/TH]\n[/TR]\n[TR]\n[TD]{home_team['team']}[/TD]\n[TD]{home_team['p_completions']}[/TD]\n[TD]{home_team['p_attempts']}[/TD]\n[TD]{home_team['cmp_percent']}[/TD]\n[TD]{home_team['passing']}[/TD]\n[TD]{home_team['p_td']}[/TD]\n[TD]{home_team['int']}[/TD]\n[TD]{home_team['sck']}[/TD]\n[/TR]\n[TR]\n[TD]{away_team['team']}[/TD]\n[TD]{away_team['p_completions']}[/TD]\n[TD]{away_team['p_attempts']}[/TD]\n[TD]{away_team['cmp_percent']}[/TD]\n[TD]{away_team['passing']}[/TD]\n[TD]{away_team['p_td']}[/TD]\n[TD]{away_team['int']}[/TD]\n[TD]{away_team['sck']}[/TD]\n[/TR]\n[/TABLE]\n\n[CENTER][B]Rushing[/B][/CENTER]\n\n[TABLE]\n[TR]\n[TH]Team[/TH]\n[TH]ATT[/TH]\n[TH]YDS[/TH]\n[TH]YDS/ATT[/TH]\n[TH]TD[/TH]\n[TH]FUM[/TH]\n[TH]LOST[/TH]\n[/TR]\n[TR]\n[TD]{home_team['team']}[/TD]\n[TD]{home_team['r_att']}[/TD]\n[TD]{home_team['rushing']}[/TD]\n[TD]{home_team['r_yds_att']}[/TD]\n[TD]{home_team['r_td']}[/TD]\n[TD]{home_team['fum']}[/TD]\n[TD]{home_team['lost']}[/TD][/TR]\n[TR]\n[TD]{away_team['team']}[/TD]\n[TD]{away_team['r_att']}[/TD]\n[TD]{away_team['rushing']}[/TD]\n[TD]{away_team['r_yds_att']}[/TD]\n[TD]{away_team['r_td']}[/TD]\n[TD]{away_team['fum']}[/TD]\n[TD]{away_team['lost']}[/TD][/TR][/TABLE]\n\n[CENTER][B]Kicking[/B][/CENTER]\n\n[TABLE][TR][TH]Team[/TH][TH]XPM[/TH][TH]XPA[/TH][TH]XP % [/TH][TH]FGM[/TH][TH]FGA[/TH][TH]FG % [/TH][TH]KR TD[/TH][/TR][TR][TD]{home_team['team']}[/TD][TD]{home_team['xpm']}[/TD][TD]{home_team['xpa']}[/TD][TD]{home_team['xp_percent']}[/TD][TD]{home_team['fgm']}[/TD][TD]{home_team['fga']}[/TD][TD]{home_team['fg_percent']}[/TD][TD]{home_team['kr_td']}[/TD][/TR][TR][TD]{away_team['team']}[/TD][TD]{away_team['xpm']}[/TD][TD]{away_team['xpa']}[/TD][TD]{away_team['xp_percent']}[/TD][TD]{away_team['fgm']}[/TD][TD]{away_team['fga']}[/TD][TD]{away_team['fg_percent']}[/TD][TD]{away_team['kr_td']}[/TD][/TR][/TABLE]\n\n[CENTER][B]Punting[/B][/CENTER]\n\n[TABLE][TR][TH]Team[/TH][TH]PUNTS[/TH][TH]PUNT YDS[/TH][TH]PUNT AVG[/TH][TH]RTN[/TH][TH]RTN YDS[/TH][TH]RTN AVG[/TH][TH]PR TD[/TH][/TR][TR][TD]{home_team['team']}[/TD][TD]{home_team['punts']}[/TD][TD]{home_team['punt_yds']}[/TD][TD]{home_team['punt_avg']}[/TD][TD]{home_team['rtn']}[/TD][TD]{home_team['rtn_yds']}[/TD][TD]{home_team['rtn_avg']}[/TD][TD]{home_team['pr_td']}[/TD][/TR][TR][TD]{away_team['team']}[/TD][TD]{away_team['punts']}[/TD][TD]{away_team['punt_yds']}[/TD][TD]{away_team['punt_avg']}[/TD][TD]{away_team['rtn']}[/TD][TD]{away_team['rtn_yds']}[/TD][TD]{away_team['rtn_avg']}[/TD][TD]{away_team['pr_td']}[/TD][/TR][/TABLE]\n\n[CENTER][B]Other[/B][/CENTER]\n\n[TABLE][TR][TH]Team[/TH][TH]SAF[/TH][TH]PEN[/TH][TH]PEN YDS[/TH][/TR][TR][TD]{home_team['team']}[/TD][TD]{home_team['saf']}[/TD][TD]{home_team['pen']}[/TD][TD]{home_team['pen_yds']}[/TD][/TR][TR][TD]{away_team['team']}[/TD][TD]{away_team['saf']}[/TD][TD]{away_team['pen']}[/TD][TD]{away_team['pen_yds']}[/TD][/TR][/TABLE]\n\nPlay-by-Play: "
print("##########################")
print("Home: ")
print(home_team)
print("\n##########################")
print("Away: ")
print(away_team)
app = "application/json"
key = "-MXtAHmOLG_1xDR2uLCicUnQSO711opM"
payload = {
    "Content-Type": "application/x-www-form-urlencoded",
    "XF-Api-Key": key,
    "XF-Api-User": "SFA"
}
params = {
    "node_id": 123,
    "title": f"Week 3, 1:00PM : {home_team['team']} vs {away_team['team']}",
    "message": template,
    "discussion_open": True,
    "sticky": False,
    "tags": ["Week3"]
}
# url = "https://www.simfba.com/index.php?api/forums/2021-season.171/threads/"
url2 = "https://www.simfba.com/index.php?api/threads/"


# res = requests.get(url2, headers=payload, params=params)
res = requests.post(url2, headers=payload, params=params)

print("RES SENT")
print(res.json())
print("============")
