# Import necessary date modules

from datetime import datetime
from datetime import timedelta


# Function to find the name of the higher ranked player in the match (higher ranked will have the lower winner_rank)

def find_player_1_name(winner_name, winner_rank, loser_name, loser_rank):
    if winner_rank < loser_rank:
        return winner_name
    else:
        return loser_name

# Function to find the rank of the higher ranked player in the match (higher ranked will have the lower winner_rank)

def find_player_1_rank(winner_rank, loser_rank):

    if winner_rank < loser_rank:
        return winner_rank
    else:
        return loser_rank

# Function to find the name of the lower ranked player in the match (lower ranked will have the higher winner_rank)

def find_player_2_name(winner_name, winner_rank, loser_name, loser_rank):

    if winner_rank > loser_rank:
        return winner_name
    else:
        return loser_name

# Function to find the rank of the lower ranked player in the match (lower ranked will have the higher winner_rank)

def find_player_2_rank(winner_rank, loser_rank):

    if winner_rank > loser_rank:
        return winner_rank
    else:
        return loser_rank

# Function for treating the result as an integer - 0 if higher ranked player won, 1 otherwise.

def result(winner_rank, loser_rank):

    if winner_rank< loser_rank:
        return 0
    else:
        return 1

# Function to give the odds of the higher ranked player

def find_player_1_odds(winner_odds, winner_rank, loser_odds, loser_rank):

    if winner_rank < loser_rank:
        return winner_odds
    else:
        return loser_odds

# Function to give the odds of the lower ranked player

def find_player_2_odds(winner_odds, winner_rank, loser_odds, loser_rank):

    if winner_rank > loser_rank:
        return winner_odds
    else:
        return loser_odds

# Function to allow assessment of performance over time frames (num_days is the number of days to be subtracting from the date)

def subtract_no_days(date_string, num_days):

    temp_date = (datetime.strptime(date_string, '%Y/%m/%d') - timedelta(days=num_days))
    return temp_date.strftime("%Y/%m/%d")

# Function to calculate winning percentages over different stats

def winning_percentage(player_id, data,  option='matches', current_date=None, surface='All', last_n_weeks=0):
    """
    :param option: Options: ['matches', 'total_matches', 'games', 'matches_5_sets', 'win_or_close_sets']
    :param last_n_weeks: find stats from the past n weeks
    :return: Returns the players stat for specified params.
    """
    data = data[data['Date'] < current_date]

    if surface!='All':
        data = data[data['Surface'] == surface]

    if last_n_weeks>0:
        last_date = subtract_no_days(current_date, (last_n_weeks * 7))
        data = data[data['Date'] >= last_date]

    if option == 'matches':
        wins = (data['Winner'] == player_id).sum()
        loses = (data['Loser'] == player_id).sum()

    elif option == 'total_matches':
        return (data['Winner'] == player_id).sum() + (data['Loser'] == player_id).sum()


    elif option == 'matches_5_sets':
        wins = ((data['Winner'] == player_id) & (data['best_of_5'] == 1)).sum()
        loses = ((data['Loser'] == player_id) & (data['best_of_5'] == 1)).sum()


    elif option == 'games':
        winner_sets_list = ['W1', 'W2', 'W3', 'W4', 'W5']
        loser_sets_list = ['L1', 'L2', 'L3', 'L4', 'L5']

        wins = data[data['Winner'] == player_id][winner_sets_list].values.sum() + data[data['Loser'] == player_id][loser_sets_list].values.sum()
        loses = data[data['Loser'] == player_id][winner_sets_list].values.sum() + data[data['Winner'] == player_id][loser_sets_list].values.sum()


    elif option == 'win_or_close_sets':

        wins = 0
        loses = 0

        data_3_sets = data[data['best_of_5'] == 0]
        data_5_sets = data[data['best_of_5'] == 1]

        for i in range(1, 4):
            wins = wins + ((data_3_sets['Winner'] == player_id) & (data_3_sets[('W' + str(i))] >= 5)).sum()
            wins = wins + ((data_3_sets['Loser'] == player_id) & (data_3_sets[('L' + str(i))] >= 5)).sum()
            loses = loses + ((data_3_sets['Winner'] == player_id) & (data_3_sets[('W' + str(i))] < 5)).sum()
            loses = loses + ((data_3_sets['Loser'] == player_id) & (data_3_sets[('L' + str(i))] < 5)).sum()

        for i in range(1, 6):
            wins = wins + ((data_5_sets['Winner'] == player_id) & (data_5_sets[('W' + str(i))] >= 5)).sum()
            wins = wins + ((data_5_sets['Loser'] == player_id) & (data_5_sets[('L' + str(i))] >= 5)).sum()
            loses = loses + ((data_5_sets['Winner'] == player_id) & (data_5_sets[('W' + str(i))] < 5)).sum()
            loses = loses + ((data_5_sets['Loser'] == player_id) & (data_5_sets[('L' + str(i))] < 5)).sum()

    total = wins + loses

    if total <2:
        win_percent = 0

    else:
        win_percent = wins / total
    return win_percent


# Function to return head to head stats between the two players

def winning_percent_h2h(player_name, opponent_name, data, option='matches', current_date=None, surface='All', last_n_weeks=0):

    data = data[data['Date'] < current_date]

    if surface != 'All':
        data = data[data['Surface'] == surface]

    if last_n_weeks>0:
        last_date = subtract_no_days(current_date, (last_n_weeks * 7))
        data = data[data['Date'] >= last_date]

    if option == 'matches':
        wins = ((data['Winner'] == player_name) & (data['Loser'] == opponent_name)).sum()
        loses = ((data['Winner'] == opponent_name) & (data['Loser'] == player_name)).sum()

    elif option == 'games':
        winner_sets_list = ['W1', 'W2', 'W3', 'W4', 'W5']
        loser_sets_list = ['L1', 'L2', 'L3', 'L4', 'L5']

        wins = data[(data['Winner'] == player_name) & (data['Loser'] == opponent_name)][winner_sets_list].values.sum() + \
               data[(data['Winner'] == opponent_name) & (data['Loser'] == player_name)][loser_sets_list].values.sum()

        loses = data[(data['Winner'] == opponent_name) & (data['Loser'] == player_name)][winner_sets_list].values.sum() + \
                data[(data['Winner'] == player_name) & (data['Loser'] == opponent_name)][loser_sets_list].values.sum()

    total = wins + loses

    if total == 0:
        win_percent = 0

    else:
        win_percent = wins / total
    return win_percent

# Function to create a data frame with player features for each match (in df_with_features the player_1 will be the higher ranked player, df is the raw dataframe)
def add_features(df_with_features, df):

   
    # Player Career Stats All Surfaces
   
    print('Loading Player Career Stats on All Surfaces')

    df_with_features.loc[:, 'player_1_match_win_percent'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='matches', current_date=row['Date'], last_n_weeks=0),
        axis=1)
    df_with_features.loc[:, 'player_2_match_win_percent'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='matches', current_date=row['Date'], last_n_weeks=0),
        axis=1)

    df_with_features.loc[:, 'player_1_games_win_percent'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='games', current_date=row['Date'], last_n_weeks=0),
        axis=1)
    df_with_features.loc[:, 'player_2_games_win_percent'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='games', current_date=row['Date'], last_n_weeks=0),
        axis=1)

    df_with_features.loc[:, 'player_1_5_sets_match_win_percent'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='matches_5_sets', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)
    df_with_features.loc[:, 'player_2_5_sets_match_win_percent'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='matches_5_sets', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)

    df_with_features.loc[:, 'player_1_close_sets_percent'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='win_or_close_sets', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)
    df_with_features.loc[:, 'player_2_close_sets_percent'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='win_or_close_sets', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)

   
    # Player Career Stats on Hard Court
   

    print('Loading Player Career Stats on Hard Courts')

    df_with_features.loc[:, 'player_1_match_win_percent_hard'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='matches', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)
    df_with_features.loc[:, 'player_2_match_win_percent_hard'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='matches', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)

    df_with_features.loc[:, 'player_1_games_win_percent_hard'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='games', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)
    df_with_features.loc[:, 'player_2_games_win_percent_hard'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='games', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)

    df_with_features.loc[:, 'player_1_5_sets_match_win_percent_hard'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='matches_5_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)
    df_with_features.loc[:, 'player_2_5_sets_match_win_percent_hard'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='matches_5_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)

    df_with_features.loc[:, 'player_1_close_sets_percent_hard'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='win_or_close_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)
    df_with_features.loc[:, 'player_2_close_sets_percent_hard'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='win_or_close_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)

   
    # Player Career Stats All Surface Last 60 Weeks (chose more than a year as covid meant long shutdown)
   

    print('Loading Player Career Stats on All Surfaces in the Last 60 Weeks')

    df_with_features.loc[:, 'player_1_match_win_percent_60'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='matches', current_date=row['Date'], last_n_weeks=60),
        axis=1)
    df_with_features.loc[:, 'player_2_match_win_percent_60'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='matches', current_date=row['Date'], last_n_weeks=60),
        axis=1)

    df_with_features.loc[:, 'player_1_games_win_percent_60'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='games', current_date=row['Date'], last_n_weeks=60),
        axis=1)
    df_with_features.loc[:, 'player_2_games_win_percent_60'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='games', current_date=row['Date'], last_n_weeks=60),
        axis=1)

    df_with_features.loc[:, 'player_1_5_sets_match_win_percent_60'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='matches_5_sets', current_date=row['Date'],
                                       last_n_weeks=60), axis=1)
    df_with_features.loc[:, 'player_2_5_sets_match_win_percent_60'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='matches_5_sets', current_date=row['Date'],
                                       last_n_weeks=60), axis=1)

    df_with_features.loc[:, 'player_1_close_sets_percent_60'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='win_or_close_sets', current_date=row['Date'],
                                       last_n_weeks=60), axis=1)
    df_with_features.loc[:, 'player_2_close_sets_percent_60'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='win_or_close_sets', current_date=row['Date'],
                                       last_n_weeks=60), axis=1)

    
   
    # Player Career Stats on Hard Court Last 100 Weeks (chose 100 as ATP rankings is on pause for 22 months ~96 weeks and rounded up to 100)
   

    print('Loading Player Career Stats on Hard Court in the last 100 Weeks')

    df_with_features.loc[:, 'player_1_match_win_percent_hard_100'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='matches', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=100), axis=1)
    df_with_features.loc[:, 'player_2_match_win_percent_hard_100'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='matches', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=100), axis=1)

    df_with_features.loc[:, 'player_1_games_win_percent_hard_100'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='games', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=100), axis=1)
    df_with_features.loc[:, 'player_2_games_win_percent_hard_100'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='games', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=100), axis=1)

    df_with_features.loc[:, 'player_1_5_sets_match_win_percent_hard_100'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='matches_5_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=100), axis=1)
    df_with_features.loc[:, 'player_2_5_sets_match_win_percent_hard_100'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='matches_5_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=100), axis=1)

    df_with_features.loc[:, 'player_1_close_sets_percent_hard_100'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_1'], df, option='win_or_close_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=100), axis=1)
    df_with_features.loc[:, 'player_2_close_sets_percent_hard_100'] = df_with_features.apply(
        lambda row: winning_percentage(row['player_2'], df, option='win_or_close_sets', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=100), axis=1)

   
    # Player Head to Head Career Stats All Surface
   

    print('Loading Player H2H Career Stats on All Surfaces')

    df_with_features.loc[:, 'player_1_match_win_percent_h2h'] = df_with_features.apply(
        lambda row: winning_percent_h2h(row['player_1'], row['player_2'], df, option='matches', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)
    df_with_features.loc[:, 'player_2_match_win_percent_h2h'] = df_with_features.apply(
        lambda row: winning_percent_h2h(row['player_2'], row['player_1'], df, option='matches', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)

    df_with_features.loc[:, 'player_1_games_win_percent_h2h'] = df_with_features.apply(
        lambda row: winning_percent_h2h(row['player_1'], row['player_2'], df, option='games', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)
    df_with_features.loc[:, 'player_2_games_win_percent_h2h'] = df_with_features.apply(
        lambda row: winning_percent_h2h(row['player_2'], row['player_1'], df, option='games', current_date=row['Date'],
                                       last_n_weeks=0), axis=1)

    
    # Player Head to Head Career Stats On Hard Court
   

    print('Loading Player H2H Career Stats On Hard Court')

    df_with_features.loc[:, 'player_1_match_win_percent_hard_h2h'] = df_with_features.apply(
        lambda row: winning_percent_h2h(row['player_1'], row['player_2'], df, option='matches', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)
    df_with_features.loc[:, 'player_2_match_win_percent_hard_h2h'] = df_with_features.apply(
        lambda row: winning_percent_h2h(row['player_2'], row['player_1'], df, option='matches', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)

    df_with_features.loc[:, 'player_1_games_win_percent_hard_h2h'] = df_with_features.apply(
        lambda row: winning_percent_h2h(row['player_1'], row['player_2'], df, option='games', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)
    df_with_features.loc[:, 'player_2_games_win_percent_hard_h2h'] = df_with_features.apply(
        lambda row: winning_percent_h2h(row['player_2'], row['player_1'], df, option='games', current_date=row['Date'],
                                       surface=row['Surface'], last_n_weeks=0), axis=1)

   
    # Difference between the players stats
   

    print('Loading variables for difference in player stats')

    df_with_features.loc[:, 'diff_match_win_percent'] = df_with_features['player_1_match_win_percent'] - df_with_features[
        'player_2_match_win_percent']
    df_with_features.loc[:, 'diff_games_win_percent'] = df_with_features['player_1_games_win_percent'] - df_with_features[
        'player_2_games_win_percent']
    df_with_features.loc[:, 'diff_5_sets_match_win_percent'] = df_with_features['player_1_5_sets_match_win_percent'] - df_with_features[
        'player_2_5_sets_match_win_percent']
    df_with_features.loc[:, 'diff_close_sets_percent'] = df_with_features['player_1_close_sets_percent'] - df_with_features[
        'player_2_close_sets_percent']

    df_with_features.loc[:, 'diff_match_win_percent_hard'] = df_with_features['player_1_match_win_percent_hard'] - df_with_features[
        'player_2_match_win_percent_hard']
    df_with_features.loc[:, 'diff_games_win_percent_hard'] = df_with_features['player_1_games_win_percent_hard'] - df_with_features[
        'player_2_games_win_percent_hard']
    df_with_features.loc[:, 'diff_5_sets_match_win_percent_hard'] = df_with_features['player_1_5_sets_match_win_percent_hard'] - \
                                                               df_with_features['player_2_5_sets_match_win_percent_hard']
    df_with_features.loc[:, 'diff_close_sets_percent_hard'] = df_with_features['player_1_close_sets_percent_hard'] - \
                                                          df_with_features['player_2_close_sets_percent_hard']

    df_with_features.loc[:, 'diff_match_win_percent_60'] = df_with_features['player_1_match_win_percent_60'] - \
                                                            df_with_features['player_2_match_win_percent_60']
    df_with_features.loc[:, 'diff_games_win_percent_60'] = df_with_features['player_1_games_win_percent_60'] - \
                                                            df_with_features['player_2_games_win_percent_60']
    df_with_features.loc[:, 'diff_5_sets_match_win_percent_60'] = df_with_features['player_1_5_sets_match_win_percent_60'] - \
                                                            df_with_features['player_2_5_sets_match_win_percent_60']
    df_with_features.loc[:, 'diff_close_sets_percent_60'] = df_with_features['player_1_close_sets_percent_60'] - df_with_features[
        'player_2_close_sets_percent_60']

    df_with_features.loc[:, 'diff_match_win_percent_hard_100'] = df_with_features['player_1_match_win_percent_hard_100'] - \
                                                            df_with_features['player_2_match_win_percent_hard_100']
    df_with_features.loc[:, 'diff_games_win_percent_hard_100'] = df_with_features['player_1_games_win_percent_hard_100'] - \
                                                            df_with_features['player_2_games_win_percent_hard_100']
    df_with_features.loc[:, 'diff_5_sets_match_win_percent_hard_100'] = df_with_features[
                                                                      'player_1_5_sets_match_win_percent_hard_100'] - \
                                                                  df_with_features[
                                                                      'player_2_5_sets_match_win_percent_hard_100']
    df_with_features.loc[:, 'diff_close_sets_percent_hard_100'] = df_with_features['player_1_close_sets_percent_hard_100'] - \
                                                             df_with_features['player_2_close_sets_percent_hard_100']

    df_with_features.loc[:, 'diff_match_win_percent_h2h'] = df_with_features['player_1_match_win_percent_h2h'] - df_with_features[
        'player_2_match_win_percent_h2h']
    df_with_features.loc[:, 'diff_games_win_percent_h2h'] = df_with_features['player_1_games_win_percent_h2h'] - df_with_features[
        'player_2_games_win_percent_h2h']

    df_with_features.loc[:, 'diff_match_win_percent_hard_h2h'] = df_with_features['player_1_match_win_percent_hard_h2h'] - \
                                                            df_with_features['player_2_match_win_percent_hard_h2h']
    df_with_features.loc[:, 'diff_games_win_percent_hard_h2h'] = df_with_features['player_1_games_win_percent_hard_h2h'] - \
                                                            df_with_features['player_2_games_win_percent_hard_h2h']

    return df_with_features