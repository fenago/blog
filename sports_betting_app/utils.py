import pandas as pd
import pickle
from fuzzywuzzy import process, fuzz
from sympy import symbols, Eq, solve



def read_dataframes(path_1, path_2):
    df_bwin = pickle.load(open(path_1,'rb'))
    df_bwin = df_bwin.replace(r'', '0\n0', regex=True)
    df_bwin = df_bwin.replace(r'^\d+\.\d+$', '0\n0', regex=True)

    df_betfair = pickle.load(open(path_2,'rb'))
    df_betfair = df_betfair.replace(r'', '0\n0', regex=True)
    df_betfair = df_betfair.replace(r'^\d+\.\d+$', '0\n0', regex=True)
    return df_bwin, df_betfair


def clean_and_combine_dataframes(df_bwin, df_betfair):  
    teams_2 = df_betfair['Teams'].tolist()
    df_bwin[['Teams_matched_betfair', 'Score_betfair']] = df_bwin['Teams'].apply(lambda x:process.extractOne(x, teams_2, scorer=fuzz.token_set_ratio)).apply(pd.Series)
    df_surebet_bwin_betfair = pd.merge(df_bwin, df_betfair, left_on='Teams_matched_betfair', right_on='Teams')
    df_surebet_bwin_betfair = df_surebet_bwin_betfair[df_surebet_bwin_betfair['Score_betfair'] > 65]
    df_surebet_bwin_betfair = df_surebet_bwin_betfair[['Teams_x', 'btts_x', 'Teams_y', 'btts_y']]
    return df_surebet_bwin_betfair


def find_surebet(frame):
    frame[['btts_x_1', 'btts_x_2']] = frame['btts_x'].apply(lambda x: x.split('\n')).apply(pd.Series).astype(float)
    frame[['btts_y_1', 'btts_y_2']] = frame['btts_y'].apply(lambda x: [x.split('\n')[0], x.split()[-1]]).apply(pd.Series).astype(float)
    frame['sure_btts1'] = (1 / frame['btts_x_1']) + (1 / frame['btts_y_2'])
    frame['sure_btts2'] = (1 / frame['btts_x_2']) + (1 / frame['btts_y_1'])
    frame = frame[['Teams_x', 'btts_x', 'Teams_y', 'btts_y', 'sure_btts1', 'sure_btts2']]
    frame = frame[(frame['sure_btts1'] < 1) | (frame['sure_btts2'] < 1)]
    frame.reset_index(drop=True, inplace=True)
    surebet = { 
        'Bwin-Betfair': frame
    }
    return surebet


def beat_bookies(odds1, odds2, total_stake):
    x, y = symbols('x y')
    eq1 = Eq(x + y - total_stake, 0) # total_stake = x + y
    eq2 = Eq((odds2*y) - odds1*x, 0) # odds1*x = odds2*y
    stakes = solve((eq1,eq2), (x, y))
    total_investment = stakes[x] + stakes[y]
    profit1 = odds1*stakes[x] - total_stake
    profit2 = odds2*stakes[y] - total_stake
    benefit1 = f'{profit1 / total_investment * 100:.2f}%'
    benefit2 = f'{profit2 / total_investment * 100:.2f}%'
    dict_gabmling = {'Odds1':odds1, 'Odds2':odds2, 'Stake1':f'${stakes[x]:.0f}', 'Stake2':f'${stakes[y]:.0f}', 'Profit1':f'${profit1:.2f}', 'Profit2':f'${profit2:.2f}',
                    'Benefit1': benefit1, 'Benefit2': benefit2}
    return dict_gabmling


def calculate_surebets(surebet, total_stake):
    surebets = []
    for frame in surebet:
        if len(surebet[frame]) >= 1:
            for i, value in enumerate(surebet[frame]['sure_btts1']):
                
                if value < 1:
                    odds1 = float(surebet[frame].at[i, 'btts_x'].split('\n')[0])
                    odds2 = float(surebet[frame].at[i, 'btts_y'].split('\n')[1])
                    
                    teams = surebet[frame].at[i, 'Teams_x'].split('\n')
                    dict_bet = beat_bookies(odds1, odds2, total_stake)

                    new_surebet = {
                        'Teams': '-'.join(teams),
                        'Odds1': dict_bet['Odds1'],
                        'Odds2': dict_bet['Odds2'],
                        'Stake1': dict_bet['Stake1'],
                        'Stake2': dict_bet['Stake2'],
                        'Profit1': dict_bet['Profit1'],
                        'Profit2': dict_bet['Profit2'],
                        'Benefit1': dict_bet['Benefit1'],
                        'Benefit2': dict_bet['Benefit2']
                    }
                    surebets.append(new_surebet)
                    
            for i, value in enumerate(surebet[frame]['sure_btts2']):
                
                if value < 1:
                    odds1 = float(surebet[frame].at[i, 'btts_x'].split('\n')[1])
                    odds2 = float(surebet[frame].at[i, 'btts_y'].split('\n')[0])
                    
                    teams = surebet[frame].at[i, 'Teams_x'].split('\n')
                    dict_bet = beat_bookies(odds1, odds2, total_stake)
                    
                    new_surebet = {
                        'Teams': '-'.join(teams),
                        'Odds1': dict_bet['Odds1'],
                        'Odds2': dict_bet['Odds2'],
                        'Stake1': dict_bet['Stake1'],
                        'Stake2': dict_bet['Stake2'],
                        'Profit1': dict_bet['Profit1'],
                        'Profit2': dict_bet['Profit2'],
                        'Benefit1': dict_bet['Benefit1'],
                        'Benefit2': dict_bet['Benefit2']
                    }
                    surebets.append(new_surebet)
    return surebets    