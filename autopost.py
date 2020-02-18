# Extract CSVs and Post results to games forum
# Imports
import requests
from csv import reader
from csv import DictReader
# Reader - lets you iterate
# DictReader

template = "[CENTER][SIZE = 6]Team 1 (0-0) vs Team 2 (0-0)[/SIZE]\n[SIZE = 3]Stadium - - Location[/SIZE][/CENTER]\n\n[TABLE]\n[TR]\n[TH]Team[/TH]\n[TH]Q1[/TH]\n[TH]Q2[/TH]\n[TH]Q3[/TH]\n[TH]Q4[/TH]\n[TH]Final[/TH]\n[/TR]\n[TR]\n[TD]TEAM 1[/TD]\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n[/TR]\n[TR]\n[TD]TEAM 2[/TD]\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n[/TR]\n[/TABLE]\n[CENTER]\n[B][U][SIZE = 6]Match Stats[/SIZE][/U]\n\nPassing[/B][/CENTER]\n\n[TABLE]\n[TR]\n[TH][CENTER]Team[/CENTER][/TH]\n\n[TH]CMP[/TH]\n[TH]ATT[/TH]\n[TH]CMP % [/TH]\n[TH]YDS[/TH]\n[TH]TD[/TH]\n[TH]INT[/TH]\n[TH]SK[/TH]\n[/TR]\n[TR]\n[TD]TEAM 1[/TD]\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n[/TR]\n[TR]\n[TD]TEAM 2[/TD]\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n[/TR]\n[/TABLE]\n\n[CENTER][B]Rushing[/B][/CENTER]\n\n[TABLE]\n[TR]\n[TH]Team[/TH]\n[TH]ATT[/TH]\n[TH]YDS[/TH]\n[TH]YDS/ATT[/TH]\n[TH]TD[/TH]\n[TH]FUM[/TH]\n[TH]LOST[/TH]\n[/TR]\n[TR]\n[TD]TEAM 1[/TD]\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n[/TR]\n[TR]\n[TD]TEAM 2[/TD]\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n[/TR]\n[/TABLE]\n\n[CENTER][B]Kicking[/B][/CENTER]\n\n[TABLE]\n[TR]\n[TH]Team[/TH]\n[TH]XPM[/TH]\n[TH]XPA[/TH]\n[TH]XP % [/TH]\n[TH]FGM[/TH]\n[TH]FGA[/TH]\n[TH]FG % [/TH]\n[TH]KR TD[/TH]\n[/TR]\n[TR]\n[TD]TEAM 1[/TD]\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n[/TR]\n[TR]\n[TD]TEAM 2[/TD]\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n[/TR]\n[/TABLE]\n\n[CENTER][B]Punting[/B][/CENTER]\n\n[TABLE]\n[TR]\n[TH]Team[/TH]\n[TH]PUNTS[/TH]\n[TH]PUNT YDS[/TH]\n[TH]PUNT AVG[/TH]\n[TH]RTN[/TH]\n[TH]RTN YDS[/TH]\n[TH]RTN AVG[/TH]\n[TH]PR TD[/TH]\n[/TR]\n[TR]\n[TD]TEAM 1[/TD]\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n[/TR]\n[TR]\n[TD]TEAM 2[/TD]\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n[/TR]\n[/TABLE]\n\n[CENTER][B]Other[/B][/CENTER]\n\n[TABLE]\n[TR]\n[TH]Team[/TH]\n[TH]SAF[/TH]\n[TH]PEN[/TH]\n[TH]PEN YDS[/TH]\n[/TR]\n[TR]\n[TD]TEAM 1[/TD]\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n[/TR]\n[TR]\n[TD]TEAM 2[/TD]\n[TD][/TD]\n\n[TD][/TD]\n\n[TD][/TD]\n[/TR]\n[/TABLE]\n\nPlay-by-Play: "
home_team = {
    "team": "",
    "score": 0,
    "passing": 0,
    "p_attempts": 0,
    "p_completions": 0,
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

# with open("./NYC@PP.csv") as file:
#     csv_reader = DictReader(file)
#     for row in csv_reader:
#         print(row)

# Function to allocate points by quarter


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
    elif(play in rush_plays):
        print(play)
        rush_play = True
        offense['rushing'] += r_yds
        if(was_accepted == 'False'):
            offense['r_att'] += 1
        offense['r_yds_att'] = float(offense['rushing']/offense['r_att'])
        if(fum == 'True'):
            offense['fum'] += 1
            if(turnover == 'True'):
                offense['lost'] += 1

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
    if(saf == 'True'):
        offense['saf'] += 1


with open("") as file:
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

print("Home: " + home_team)
print("Away: " + away_team)


# res = requests.get(
#     "https://www.simfba.com/index.php?threads/4-00pm-games.624", headers={"Accept": "application/json"})
# print("RES\n\n")
# print(res)
# print("============\n\n")
# res2 = requests.get("https://pokeapi.co/api/v2/pokemon/ditto/",
#                     headers={"Accept": "application/json"})
# print(res2.json())
