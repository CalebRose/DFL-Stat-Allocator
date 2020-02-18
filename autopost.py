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
        offense['cmp_percent'] = float(
            offense['p_completions'] / offense['p_attempts'])
    # Rush Play
    elif(play in rush_plays):
        rush_play = True
        offense['rushing'] += r_yds
        if(was_accepted == 'False'):
            offense['r_att'] += 1
        offense['r_yds_att'] = float(offense['rushing']/offense['r_att'])
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
            offense['punt_avg'] = float(offense['punt_yds'] /
                                        offense['punts'])
            # Calculate Away Team Return Yards
            defense['rtn_yds'] += ret_yrds
            defense['rtn'] += 1
            defense['rtn_avg'] = float(defense['rtn_yds'] /
                                       defense['rtn'])

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
            offense['xp_percent'] = float(offense['xpm'] / offense['xpa'])
            offense['xp'] = False
        # Else, it's just a field goal for 3
        else:
            if(fg == 'True'):
                score_allocator(offense, iterator, 3)
                offense['fgm'] += 1
            offense['fga'] += 1
            offense['fg_percent'] = float(offense['fgm'] / offense['fga'])

    # Penalty Occurring
    if(penalty == 'True'):
        offense['pen'] += 1
        if(was_accepted == 'True'):
            offense['pen_yds'] += penalty_yards
    # Safety
    if(saf == 'True'):
        offense['saf'] += 1


with open("D:\Rubicon\AutoPost\SimFBA-Stat-Allocator\NYC@PP.csv") as file:
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
        elif(iterator > 6 and iterator not in gaps):
            # Home Team
            if(row[1] == home_team['team']):
                # Offense = Home Team; Defense = Away Team
                play_allocation(home_team, away_team, row, iterator)
            # If the team is the AWAY team
            elif(row[1] == away_team['team']):
                # Offense = Away Team; Defense = Home Team
                play_allocation(away_team, home_team, row, iterator)
        iterator += 1
        # print(row)

template = f"[CENTER][SIZE=6]{home_team['team']} (0-0) vs{away_team['team']} (0-0)[/SIZE][SIZE=3]{stadium} - - {location}[/SIZE][/CENTER][TABLE][TR][TH]Team[/TH][TH]Q1[/TH][TH]Q2[/TH][TH]Q3[/TH][TH]Q4[/TH][TH]Final[/TH][/TR][TR][TD]{home_team['team']}[/TD][TD]{home_team['q1_score']}[/TD][TD]{home_team['q2_score']}[/TD][TD]{home_team['q3_score']}[/TD][TD]{home_team['q4_score']}[/TD][TD]{home_team['score']}[/TD][/TR][TR][TD]{away_team['team']}[/TD][TD]{away_team['q1_score']}[/TD][TD]{away_team['q2_score']}[/TD][TD]{away_team['q3_score']}[/TD][TD]{away_team['q4_score']}[/TD][TD]{away_team['score']}[/TD][/TR][/TABLE][CENTER][B][U][SIZE = 6]Match Stats[/SIZE][/U]Passing[/B][/CENTER][TABLE][TR][TH][CENTER]Team[/CENTER][/TH][TH]CMP[/TH][TH]ATT[/TH][TH]CMP % [/TH][TH]YDS[/TH][TH]TD[/TH][TH]INT[/TH][TH]SK[/TH][/TR][TR][TD]{home_team['team']}[/TD][TD]{home_team['p_completions']}[/TD][TD]{home_team['p_attempts']}[/TD][TD]{home_team['cmp_percent']}[/TD][TD]{home_team['passing']}[/TD][TD]{home_team['p_td']}[/TD][TD]{home_team['int']}[/TD][TD]{home_team['sck']}[/TD][/TR][TR][TD]{away_team['team']}[/TD][TD]{away_team['p_completions']}[/TD][TD]{away_team['p_attempts']}[/TD][TD]{away_team['cmp_percent']}[/TD][TD]{away_team['passing']}[/TD][TD]{away_team['p_td']}[/TD][TD]{away_team['int']}[/TD][TD]{away_team['sck']}[/TD][/TR][/TABLE][CENTER][B]Rushing[/B][/CENTER][TABLE][TR][TH]Team[/TH][TH]ATT[/TH][TH]YDS[/TH][TH]YDS/ATT[/TH][TH]TD[/TH][TH]FUM[/TH][TH]LOST[/TH][/TR][TR][TD]{home_team['team']}[/TD][TD]{home_team['r_att']}[/TD][TD]{home_team['rushing']}[/TD][TD]{home_team['r_yds_att']}[/TD][TD]{home_team['r_td']}[/TD][TD]{home_team['fum']}[/TD][TD]{home_team['lost']}[/TD][/TR][TR][TD]{away_team['team']}[/TD][TD]{away_team['r_att']}[/TD][TD]{away_team['rushing']}[/TD][TD]{away_team['r_yds_att']}[/TD][TD]{away_team['r_td']}[/TD][TD]{away_team['fum']}[/TD][TD]{away_team['lost']}[/TD][/TR][/TABLE][CENTER][B]Kicking[/B][/CENTER][TABLE][TR][TH]Team[/TH][TH]XPM[/TH][TH]XPA[/TH][TH]XP % [/TH][TH]FGM[/TH][TH]FGA[/TH][TH]FG % [/TH][TH]KR TD[/TH][/TR][TR][TD]{home_team['team']}[/TD][TD]{home_team['xpm']}[/TD][TD]{home_team['xpa']}[/TD][TD]{home_team['xp_percent']}[/TD][TD]{home_team['fgm']}[/TD][TD]{home_team['fga']}[/TD][TD]{home_team['fg_percent']}[/TD][TD]{home_team['kr_td']}[/TD][/TR][TR][TD]{away_team['team']}[/TD][TD]{away_team['xpm']}[/TD][TD]{away_team['xpa']}[/TD][TD]{away_team['xp_percent']}[/TD][TD]{away_team['fgm']}[/TD][TD]{away_team['fga']}[/TD][TD]{away_team['fg_percent']}[/TD][TD]{away_team['kr_td']}[/TD][/TR][/TABLE][CENTER][B]Punting[/B][/CENTER][TABLE][TR][TH]Team[/TH][TH]PUNTS[/TH][TH]PUNT YDS[/TH][TH]PUNT AVG[/TH][TH]RTN[/TH][TH]RTN YDS[/TH][TH]RTN AVG[/TH][TH]PR TD[/TH][/TR][TR][TD]{home_team['team']}[/TD][TD]{home_team['punts']}[/TD][TD]{home_team['punt_yds']}[/TD][TD]{home_team['punt_avg']}[/TD][TD]{home_team['rtn']}[/TD][TD]{home_team['rtn_yds']}[/TD][TD]{home_team['rtn_avg']}[/TD][TD]{home_team['pr_td']}[/TD][/TR][TR][TD]{away_team['team']}[/TD][TD]{away_team['punts']}[/TD][TD]{away_team['punt_yds']}[/TD][TD]{away_team['punt_avg']}[/TD][TD]{away_team['rtn']}[/TD][TD]{away_team['rtn_yds']}[/TD][TD]{away_team['rtn_avg']}[/TD][TD]{away_team['pr_td']}[/TD][/TR][/TABLE][CENTER][B]Other[/B][/CENTER][TABLE][TR][TH]Team[/TH][TH]SAF[/TH][TH]PEN[/TH][TH]PEN YDS[/TH][/TR][TR][TD]{home_team['team']}[/TD][TD]{home_team['saf']}[/TD][TD]{home_team['pen']}[/TD][TD]{home_team['pen_yds']}[/TD][/TR][TR][TD]{away_team['team']}[/TD][TD]{away_team['saf']}[/TD][TD]{away_team['pen']}[/TD][TD]{away_team['pen_yds']}[/TD][/TR][/TABLE]Play-by-Play: "
# print("Home: " + home_team)
# print("Away: " + away_team)
app = "application/json"
key = "-MXtAHmOLG_1xDR2uLCicUnQSO711opM"
payload = {
    "Content-Type": "application/x-www-form-urlencoded",
    "XF-Api-Key": key,
    "XF-Api-User": "SFA"
}
params = {
    "node_id": 123,
    "title": "Test3",
    "message": template,
    "discussion_open": True,
    "sticky": False,
    "tags": ["SeattleWins"]
}
url = "https://www.simfba.com/index.php?api/forums/2021-season.171/threads/"
url2 = "https://www.simfba.com/index.php?api/threads/"


# res = requests.get(url2, headers=payload, params=params)
res = requests.post(url2, headers=payload, params=params)

print("RES")
print(res.json())
print("============")
