import itertools
import numpy as np
import pandas as pd

LOTTERY_INFO = {1: {'name': 'Pistons', 'id': '1610612765'},
                2: {'name': 'Rockets', 'id': '1610612745'},
                3: {'name': 'Spurs', 'id': '1610612759'},
                4: {'name': 'Hornets', 'id': '1610612766'},
                5: {'name': 'Trailblazers', 'id': '1610612757'},
                6: {'name': 'Magic', 'id': '1610612753'},
                7: {'name': 'Pacers', 'id': '1610612754'},
                8: {'name': 'Wizards', 'id': '1610612764'},
                9: {'name': 'Jazz', 'id': '1610612762'},
                10: {'name': 'Mavericks', 'id': '1610612742'},
                11: {'name': 'Bulls', 'id': '1610612741'},
                12: {'name': 'Thunder', 'id': '1610612760'},
                13: {'name': 'Raptors', 'id': '1610612761'},
                14: {'name': 'Pelicans', 'id': '1610612740'}}

LOTTO_CHANCES = {1: 140, 2: 140, 3: 140,
                 4: 125, 5: 105, 6: 90, 7: 75,
                 8: 60, 9: 45, 10: 30, 11: 20, 12: 15,
                 13: 10, 14: 5}
TOP_PICKS = 4


def calculate_pick_probabilities(lotto_combos, top_picks,
                                 teams_selected, top_pick_list,
                                 top_pick_order):
    """ calculate_pick_probabilities dynamically calculates the probability of each
    team receiving picks 1-14 in the NBA Lottery.

    @param lotto_combos (dict): Dictionary keyed by team
        lottery order with values corresponding to each team's
        lottery chances
    @param top_picks (int): Integer indicating the number of
        picks that are selected via the lottery. The rest of the
        picks are slotted in reverse order of team record
    @param teams_selected (list): List containing the team lottery
        order of teams already revealed in the lottery and not in
        the top_picks number of picks
    @param top_pick_list (list): List containing the team lottery
        order of teams already revealed to be in the top_picks number
        of picks
    @param top_pick_order (list): List containing the order of the
        top picks as they are revealed

    Returns:

        prob_dict (dict): Dictionoary keyed by team lottery order
            with a list containing the probability of the team
            receiving each draft pick
    """

    prob_dict = {}
    total_teams = len(lotto_combos)
    total_combos = 0
    for num in lotto_combos:
        if num not in teams_selected:  # Only adding teams that have not been revealed
            total_combos += lotto_combos[num]

    team_list = list(lotto_combos.keys())
    for team in range(1, total_teams + 1):
        prob_list = [0] * total_teams # Initializing the list of pick probabilities                      
        if team in teams_selected and team not in top_pick_order:
            fall_spot = 0
            for top_pick in top_pick_list:
                if top_pick > team:
                    fall_spot += 1
            prob_list[team - 1 + fall_spot] = 1 # If a team has been revealed, we know with certainty the pick number
        elif team in top_pick_order:
            count = 0
            for team_here in top_pick_order:
                if team_here == team:
                    prob_list[top_picks - count - 1] = 1
                count += 1
        else:
            pick_order = list(itertools.permutations(team_list,
                                                     top_picks - len(top_pick_order)))
            prob_fall = [0] * (top_picks + 1)

            # If a team has not been revealed, we loop through all possible permutations of the
            # first four picks and find the probability of each permutation occurring
            for order in pick_order:
                balls_remaining = total_combos
                other_teams_probability = 1
                top_pick_probability = 1

                # If a team has been revealed to be in the top number of picks, only permutations
                # containing that team are valid. top_pick_ind ensures that only these permutations
                # are evaluated
                top_pick_ind = 1
                for top_pick in top_pick_list:
                    if top_pick in order or top_pick in teams_selected:
                        top_pick_ind *= 1
                    else:
                        top_pick_ind *= 0

                if top_pick_ind:
                    fall_spots = 0
                    pick_ind = 0
                    count = 0
                    for pick in order:
                        if pick in teams_selected:
                            # If a pick has already been revealed to be outside of the
                            # top picks, this permutation is invalid
                            other_teams_probability = 0
                            top_pick_probability = 0
                            break

                        if team in order:
                            # If team is in this permutation of top picks, evaluate the probability
                            # of the permutation occurring AND track the pick number with the pick_count
                            # index.
                            if pick == team:
                                pick_count = count
                            other_teams_probability = 0
                            shot_prob = lotto_combos[pick]/float(balls_remaining)

                            balls_remaining = balls_remaining - lotto_combos[pick]
                            top_pick_probability *= shot_prob
                            pick_ind = 1
                            count += 1
                        else:
                            # If team is not in this permutation, track the number of teams higher
                            # than the current team that are in the permutation. This gives the number
                            # of spots that the team falls in the lottery. Again, track the probability
                            # of this permutation occurring AND track the pick number with the fall_spots
                            # index
                            pick_ind = 0
                            if pick > team:
                                fall_spots += 1

                            shot_prob = lotto_combos[pick]/float(balls_remaining)

                            balls_remaining = balls_remaining - lotto_combos[pick]

                            count += 1

                            other_teams_probability *= shot_prob

                    # If pick_ind == 0, the team does not pick in the top_picks in this permutation
                    # If pick_ind == 1, the team does pick in the top_picks in this permutation
                    if pick_ind == 0:
                        prob_fall[fall_spots] += \
                            other_teams_probability
                    else:
                        prob_list[pick_count] += \
                            top_pick_probability

            # This loop fills in the corresponding "fall" spot with the appropriate probability
            for spot in range(team - 1, team + top_picks - len(top_pick_order)):
                if spot <= total_teams - 1 and spot > top_picks - 1:
                    prob_list[spot] = prob_fall[spot - team + 1]

        prob_list = [0 if sum(prob_list) == 0 else x/sum(prob_list) for x in prob_list]
        prob_dict[team] = [round(100*x, 1) for x in prob_list]

    return prob_dict


def update_odds(teams_selected,
                top_pick_list,
                top_pick_order):
    """ update_odds calculates draft
    lottery probabilities and populates
    them in a DataFrame

    @param teams_selected (list): List of key values for
        LOTTERY_INFO that represent the reverse
        standings order. This list is filled
        in as teams are revealed
    @param top_pick_list (list): List of key values for
        lottery_info that correspond to the teams
        that are "skipped" as the back of the
        lottery is revealed. This means that team
        has a pick in the top 4
    @param top_pick_order (list): List of key values for
        lottery_info that correspond to the teams
        that are revealed starting in the top 4

    Returns:

        - lotto_df (DataFrame): DataFrame containing
            the lottery odds for each team
    """

    prob_dict = calculate_pick_probabilities(LOTTO_CHANCES,
                                             TOP_PICKS,
                                             teams_selected,
                                             top_pick_list,
                                             top_pick_order)

    lotto_df = pd.DataFrame(prob_dict)

    # Coding in the pick conversions that trigger should a certain order be pulled
    lotto_df.columns = ["Knicks" if (x == 10 and (prob_dict[x][10] == 100
                                                        or prob_dict[x][11] == 100
                                                        or prob_dict[x][12] == 100
                                                        or prob_dict[x][13] == 100))
                        else "Magic" if (x == 11 and (prob_dict[x][4] == 100
                                                        or prob_dict[x][5] == 100
                                                        or prob_dict[x][6] == 100
                                                        or prob_dict[x][7] == 100
                                                        or prob_dict[x][8] == 100
                                                        or prob_dict[x][9] == 100
                                                        or prob_dict[x][10] == 100
                                                        or prob_dict[x][11] == 100
                                                        or prob_dict[x][12] == 100
                                                        or prob_dict[x][13] == 100))
                        else LOTTERY_INFO[x]['name']
                        for x in LOTTERY_INFO]
    lotto_df = lotto_df.T
    lotto_df.columns = list(range(1, len(LOTTO_CHANCES) + 1))
    lotto_df = lotto_df.sort_values([1, 2, 3, 4],
                                    ascending=[False, False, False, False])

    for col in lotto_df.columns:
        lotto_df[col] = ['%s' % float('%.3g' % x) if x not in [0, 100]
                         else '100' if x == 100
                         else '0' for x in lotto_df[col]]

    return lotto_df
