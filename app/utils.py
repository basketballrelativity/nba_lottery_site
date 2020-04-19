"""
utils.py

Utility functions for routes.py
that helps populate objects
for display
"""

import ast

def get_teams_selected(request, lottery_info):
    """ get_teams_selected updates the teams
    selected by the user

    @param request (flask.request object): Object containing
        args attributes
    @param lottery_info (dict): Dictionary keyed by
        reverse standings order, with dictionary
        values containing 'name' and 'id' keys
        for the team

    Returns:

        - teams_selected (list): Teams previously
        selected by the user
    """

    teams_selected = []
    selections = ast.literal_eval(request.args['teams_selected'])
    for val in selections:
        team_name = selections[val].split(' ')[-1]
        if team_name != '':
            for x in range(len(lottery_info), 0, -1):
                if lottery_info[x]['name'] == team_name:
                    teams_selected.append(x)

    return teams_selected


def get_top_picks(teams_selected, lottery_info):
    """ This function fills in both teams known
    to be in the top 4 and their corresponding
    order

    @param teams_selected (list): List of key values for
        lottery_info that represent the reverse
        standings order. This list is filled
        in as teams are revealed
    @param lottery_info (dict): Dictionary keyed by
        reverse standings order, with dictionary
        values containing 'name' and 'id' keys
        for the team

    Returns:

        - top_pick_list (list): List of key values for
        lottery_info that correspond to the teams
        that are "skipped" as the back of the
        lottery is revealed. This means that team
        has a pick in the top 4
        - top_pick_order (list): List of key values for
        lottery_info that correspond to the teams
        that are revealed starting in the top 4
    """

    expected_team = len(lottery_info)
    team_count = len(lottery_info)

    top_pick_list = []
    top_pick_order = []
    for team in teams_selected:
        if team != expected_team:
            if len(top_pick_list) < 4 and team_count >= 5:
                top_pick_list.append(expected_team)
                expected_team -= 1
        if team_count < 5:
            top_pick_order.append(team)
        expected_team -= 1
        team_count -= 1

    return top_pick_list, top_pick_order


def update_teams(lottery_info, top_pick_list,
                 teams_selected, top_pick_order,
                 request):
    """ update_teams populates the proper list
    depending on the team selected

    @param lottery_info (dict): Dictionary keyed by
        reverse standings order, with dictionary
        values containing 'name' and 'id' keys
        for the team
    @param top_pick_list (list): List of key values for
        lottery_info that correspond to the teams
        that are "skipped" as the back of the
        lottery is revealed. This means that team
        has a pick in the top 4
    @param teams_selected (list): List of key values for
        lottery_info that represent the reverse
        standings order. This list is filled
        in as teams are revealed
    @param top_pick_order (list): List of key values for
        lottery_info that correspond to the teams
        that are revealed starting in the top 4
    @param request (flask.request object): Object containing
        method and form attributes

    Returns:

        - teams_selected (list): If the user selected a team,
        it is added to teams_selected
        - top_pick_list (list): If a team is "skipped" as the
        back of the lottery is revealed, it is added to
        top_pick_list
        - top_pick_order (list): Once the top 4 is known,
        a team is added to top_pick_order once it is
        revealed
        - current_slot (int): Integer corresponding to
        the current lottery slot, starting at 14 and
        diminishing by 1 as each team is revealed
    """
    current_slot = len(lottery_info) - len(teams_selected)
    if request.method == "POST" and request.form['teams'] is not None:
        expected_team = current_slot - len(top_pick_list)
        for x in lottery_info:
            if lottery_info[x]['name'] == request.form['teams']:
                # Add selected team to teams_selected
                teams_selected.append(x)
                if current_slot < 5:
                    # If the pick is within the top 4,
                    # update the top pick order list
                    top_pick_order.append(x)
                if x != expected_team:
                    # If the pick is "out of order",
                    # add the team that was skipped
                    # to the top 4 list
                    if len(top_pick_list) < 4:
                        for pos_team in range(len(lottery_info), x, -1):
                            if pos_team not in teams_selected and pos_team not in top_pick_list:
                                top_pick_list.append(pos_team)

        if current_slot == 5:
            top_pick_list = []
            for x in lottery_info:
                if x not in teams_selected:
                    top_pick_list.append(x)

    return teams_selected, top_pick_list, top_pick_order, current_slot


def fast_forward(lottery_info, top_pick_list,
                 teams_selected, current_slot):
    """ fast_forward automatically advances the site
    to the top 4 if all 4 teams are known

    @param lottery_info (dict): Dictionary keyed by
        reverse standings order, with dictionary
        values containing 'name' and 'id' keys
        for the team
    @param top_pick_list (list): List of key values for
        lottery_info that correspond to the teams
        that are "skipped" as the back of the
        lottery is revealed. This means that team
        has a pick in the top 4
    @param teams_selected (list): List of key values for
        lottery_info that represent the reverse
        standings order. This list is filled
        in as teams are revealed
    @param current_slot (int): Integer corresponding to
        the current lottery slot, starting at 14 and
        diminishing by 1 as each team is revealed

    Returns:

        - teams_selected (list): If a team is not in the top 4,
        it is added to teams_selected
        - current_slot (int): Current slot is advanced to 5
    """

    current_slot = 5
    for x in range(len(lottery_info), 0, -1):
        if x not in teams_selected and x not in top_pick_list:
            teams_selected.append(x)

    return teams_selected, current_slot


def populate_dropdown(lottery_info, top_pick_list,
                      teams_selected,
                      top_pick_order, current_slot):
    """ populate_dropdown returns a list of teams
    to be displayed in the site dropdown. Only teams
    that are eligible to be revealed can be selected

    @param lottery_info (dict): Dictionary keyed by
        reverse standings order, with dictionary
        values containing 'name' and 'id' keys
        for the team
    @param top_pick_list (list): List of key values for
        lottery_info that correspond to the teams
        that are "skipped" as the back of the
        lottery is revealed. This means that team
        has a pick in the top 4
    @param teams_selected (list): List of key values for
        lottery_info that represent the reverse
        standings order. This list is filled
        in as teams are revealed
    @param top_pick_order (list): List of key values for
        lottery_info that correspond to the teams
        that are revealed starting in the top 4
    @param current_slot (int): Integer corresponding to
        the current lottery slot, starting at 14 and
        diminishing by 1 as each team is revealed

    Returns:

        - teams (list): List of team names to be
            displayed in the site dropdown
        - teams_selected (list): If one team remains,
            we know it's got the number 1 pick! It is
            added to teams_selected
        - top_pick_order (list): The same team is
            added to top_pick_order
    """
    teams = []
    for x in range(len(lottery_info), 0, -1):
        if x not in teams_selected:
            if x not in top_pick_list or current_slot <= 5:
                if current_slot > 5:
                    if len(teams) < 5 - len(top_pick_list):
                        teams.append(lottery_info[x]['name'])
                else:
                    teams.append(lottery_info[x]['name'])

    if len(teams) == 1:
        for x in lottery_info:
            if x not in teams_selected:
                teams_selected.append(x)
                top_pick_order.append(x)
        teams = []

    teams.append(None)

    return teams, teams_selected, top_pick_order


def draft_order(lottery_info, teams_selected):
    """ draft_order populates a list of revealed
    teams so far

    @param lottery_info (dict): Dictionary keyed by
        reverse standings order, with dictionary
        values containing 'name' and 'id' keys
        for the team
    @param teams_selected (list): List of key values for
        lottery_info that represent the reverse
        standings order. This list is filled
        in as teams are revealed

    Returns:

        - selections (list): Returns a list
            of team names prefixed with draft
            pick number
    """

    selections = {}
    init = len(lottery_info)
    for selection in teams_selected:
        selections[init] = str(init) + \
            '. ' + \
            lottery_info[selection]['name']
        init -= 1
    while init > 0:
        selections[init] = str(init) + '. '
        init -= 1

    return selections