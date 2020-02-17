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
    "xpm": 0,
    "xpa": 0,
    "xp_percent": 0,
    "fgm": 0,
    "fga": 0,
    "fg_percent": 0,
    "kr_td": 0,
    "punts": 0,
    "p_yds": 0,
    "p_avg": 0,
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
    "score": "",
    "passing": "",
    "p_attempts": "",
    "p_completions": "",
    "p_TD": "",
    "int": "",
    "sck": "",
    "rushing": "",
    "r_att": "",
    "r_yds_att": "",
    "r_td": "",
    "fum": "",
    "lost": "",
    "xpm": "",
    "xpa": "",
    "xp_percent": "",
    "fgm": "",
    "fga": "",
    "fg_percent": "",
    "kr_td": "",
    "punts": "",
    "p_yds": "",
    "p_avg": "",
    "rtn": "",
    "rtn_yds": "",
    "rtn_avg": "",
    "pr_td": "",
    "saf": "",
    "pen": "",
    "pen_yds": "",
    "q1_score": "",
    "q2_score": "",
    "q3_score": "",
    "q4_score": ""
}

stadium = ""
location = ""
iterator = 0
gaps = (7, 42, 43, 79, 80, 81, 82, 118, 119)
pass_plays = ('Slants', 'Flood', 'Scissors', 'Play Action',
              'Screen Pass', 'Max Protect', 'Streaks')
rush_plays = ('Blast', 'Power', 'Draw', 'Sweep', 'Option')

# with open("./NYC@PP.csv") as file:
#     csv_reader = DictReader(file)
#     for row in csv_reader:
#         print(row)

with open("./NYC@PP.csv") as file:
    csv_reader = reader(file)
    for row in csv_reader:
        if(row[0] == 'Home Team:'):
            home_team['team'] = row[1]
            home_team['score'] = row[2]
        elif(row[0] == 'Away Team:'):
            away_team['team'] = row[1]
            away_team['score'] = row[2]
        elif(iterator > 6 and iterator not in gaps):
            play = row[2]
            pass_play = False
            rush_play = False
            kickoff = row[4]
            p_yds = row[8]
            incomplete = row[9]
            r_yds = row[10]
            k_yards = row[11]
            punt_yards = row[12]
            ret_yrds = row[13]
            sack = row[14]
            fg = row[15]
            td = row[16]
            xp = False
            saf = row[17]
            inter = row[18]
            fum = row[19]
            turnover = row[20]
            minor_injury = row[21]
            major_injury = row[22]
            injury = row[23]
            penalty = row[24]
            penalty_type = row[25]
            penalty_yards = row[26]
            was_accepted = row[27]
            # Home Team
            if(row[1] == home_team['team']):
                # # Calculate stats # #
                # Passing
                if(play in pass_plays):
                    pass_play = True
                    home_team['passing'] += p_yds
                    if(incomplete == 'FALSE'):
                        home_team['p_completions'] += 1
                    if(sack == 'TRUE'):
                        home_team['sck'] += 1
                    else:
                        home_team['p_attempts'] += 1
                    if(inter == 'TRUE'):
                        home_team['int'] += 1

                # Rushing
                elif(play in rush_plays):
                    rush_play = True
                    home_team['rushing'] += r_yds
                    home_team['r_att'] += 1
                    home_team['r_yds_att'] = home_team['rushing'] / \
                        home_team['r_att']
                    if(fum == 'TRUE'):
                        home_team['fum'] += 1
                        if(turnover == 'TRUE'):
                            home_team['lost'] += 1

                elif(play == 'Kickoff' or play == 'Punt'):
                    if(play == 'Kickoff'):
                        home_team['kickoff_yds'] += k_yards
                    elif(play == 'Punt'):
                        home_team['punts'] += 1
                        home_team['p_yds'] += punt_yards
                        home_team['p_avg'] = home_team['p_yds'] / \
                            home_team['punts']
                    # Calculate Away Team Return Yards
                    away_team['rtn_yds'] += ret_yrds
                    away_team['rtn'] += 1
                    away_team['rtn_avg'] = away_team['rtn_yds'] / \
                        away_team['rtn']
                # Touchdown Made
                if(td == 'TRUE'):
                    if(pass_play == True):
                        home_team['p_td'] += 1
                    elif(rush_play == True):
                        home_team['r_td'] += 1
                    if(iterator < 42):
                        home_team['q1_score'] += 6
                    elif(iterator < 79):
                        home_team['q2_score'] += 6
                    elif(iterator < 118):
                        home_team['q3_score'] += 6
                    else:
                        home_team['q4_score'] += 6
                    xp = True
                if(play == 'Field Goal'):
                    if(xp == True):
                        if(fg == 'TRUE'):
                            home_team['q1_score'] += 1
                            home_team['xpm'] += 1
                        home_team['xpa'] += 1
                        xp = False
                    else:
                        if(fg == 'TRUE'):
                            home_team['q1_score'] += 3
                            home_team['fgm'] += 1
                        home_team['fga'] += 1

                if(penalty == 'TRUE'):
                    home_team['pen'] += 1
                    if(was_accepted == 'TRUE'):
                        home_team['pen_yds'] += penalty_yards
            elif(row[1] == away_team['team']):
                if(play in pass_plays):
                    pass_play = True
                    away_team['passing'] += p_yds
                    if(incomplete == 'FALSE'):
                        away_team['p_completions'] += 1
                    if(sack == 'TRUE'):
                        away_team['sck'] += 1
                    else:
                        away_team['p_attempts'] += 1
                    if(inter == 'TRUE'):
                        away_team['int'] += 1

                # Rushing
                elif(play in rush_plays):
                    rush_play = True
                    away_team['rushing'] += r_yds
                    away_team['r_att'] += 1
                    away_team['r_yds_att'] = away_team['rushing'] / \
                        away_team['r_att']
                    if(fum == 'TRUE'):
                        away_team['fum'] += 1
                        if(turnover == 'TRUE'):
                            away_team['lost'] += 1

                elif(play == 'Kickoff' or play == 'Punt'):
                    if(play == 'Kickoff'):
                        away_team['kickoff_yds'] += k_yards
                    elif(play == 'Punt'):
                        away_team['punts'] += 1
                        away_team['p_yds'] += punt_yards
                        away_team['p_avg'] = away_team['p_yds'] / \
                            home_team['punts']
                    # Calculate Away Team Return Yards
                    home_team['rtn_yds'] += ret_yrds
                    home_team['rtn'] += 1
                    home_team['rtn_avg'] = home_team['rtn_yds'] / \
                        home_team['rtn']
                # Touchdown Made
                if(td == 'TRUE'):
                    if(pass_play == True):
                        away_team['p_td'] += 1
                    elif(rush_play == True):
                        away_team['r_td'] += 1
                    if(iterator < 42):
                        away_team['q1_score'] += 6
                    elif(iterator < 79):
                        away_team['q2_score'] += 6
                    elif(iterator < 118):
                        away_team['q3_score'] += 6
                    else:
                        away_team['q4_score'] += 6
                    xp = True
                if(play == 'Field Goal'):
                    if(xp == True):
                        if(fg == 'TRUE'):
                            away_team['q1_score'] += 1
                            away_team['xpm'] += 1
                        away_team['xpa'] += 1
                        xp = False
                    else:
                        if(fg == 'TRUE'):
                            away_team['q1_score'] += 3
                            away_team['fgm'] += 1
                        away_team['fga'] += 1

                if(penalty == 'TRUE'):
                    away_team['pen'] += 1
                    if(was_accepted == 'TRUE'):
                        away_team['pen_yds'] += penalty_yards
                # Away Team
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
