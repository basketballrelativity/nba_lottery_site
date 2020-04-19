#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 08:43:34 2018

@author: patrickmcfarlane

test_utils.py

This function contains the tests for
functions in the utils.py file
"""

LOTTERY_INFO = {1: {'name': 'Warriors', 'id': '1610612744'},
                2: {'name': 'Cavaliers', 'id': '1610612739'},
                3: {'name': 'Timberwolves', 'id': '1610612750'},
                4: {'name': 'Hawks', 'id': '1610612737'},
                5: {'name': 'Pistons', 'id': '1610612765'},
                6: {'name': 'Knicks', 'id': '1610612752'},
                7: {'name': 'Bulls', 'id': '1610612741'},
                8: {'name': 'Hornets', 'id': '1610612766'},
                9: {'name': 'Wizards', 'id': '1610612764'},
                10: {'name': 'Suns', 'id': '1610612756'},
                11: {'name': 'Spurs', 'id': '1610612759'},
                12: {'name': 'Kings', 'id': '1610612766'},
                13: {'name': 'Pelicans', 'id': '1610612740'},
                14: {'name': 'Trailblazers', 'id': '1610612757'}}

from app import utils


class Request(object):
        pass


def test_get_teams_selected():
    """ This function tests
    get_teams_selected in app.utils.py
    """

    test_teams_1 = "{14: '14. ', 13: '13. ', 12: '12. ', \
                     11: '11. ', 10: '10. ', 9: '9. ', \
                     8: '8. ', 7: '7. ', 6: '6. ', \
                     5: '5. ', 4: '4. ', 3: '3. ', \
                     2: '2. ', 1: '1. '}"
    test_teams_2 = "{14: '14. Trailblazers', 13: '13. Pelicans', \
                     12: '12. Kings', \
                     11: '11. ', 10: '10. ', 9: '9. ', \
                     8: '8. ', 7: '7. ', 6: '6. ', \
                     5: '5. ', 4: '4. ', 3: '3. ', \
                     2: '2. ', 1: '1. '}"
    test_teams_3 = "{14: '14. Trailblazers', 13: '13. Pelicans', \
                     12: '12. Kings', \
                     11: '11. Spurs', 10: '10. Wizards', 9: '9. Bulls', \
                     8: '8. Knicks', 7: '7. Hawks', 6: '6. Timberwolves', \
                     5: '5. Cavaliers', 4: '4. Warriors', 3: '3. Suns', \
                     2: '2. Pistons', 1: '1. Hornets'}"

    request = Request()
    request.args = {}
    request.args['teams_selected'] = test_teams_1
    teams_selected_1 = utils.get_teams_selected(request, LOTTERY_INFO)

    request.args['teams_selected'] = test_teams_2
    teams_selected_2 = utils.get_teams_selected(request, LOTTERY_INFO)

    request.args['teams_selected'] = test_teams_3
    teams_selected_3 = utils.get_teams_selected(request, LOTTERY_INFO)

    assert teams_selected_1 == []
    assert teams_selected_2 == [14, 13, 12]
    assert teams_selected_3 == [14, 13, 12, 11, 9,
                                7, 6, 4, 3, 2, 1,
                                10, 5, 8]


def test_get_top_picks():
    """ This function tests
    get_top_picks in app.utils.py
    """

    teams_selected_1 = []
    teams_selected_2 = [14, 13, 12]
    teams_selected_3 = [14, 13, 12, 11, 9,
                        7, 6, 4, 3, 2, 1,
                        10, 5, 8]

    top_pick_list, top_pick_order = \
        utils.get_top_picks(teams_selected_1, LOTTERY_INFO)

    assert top_pick_list == []
    assert top_pick_order == []

    top_pick_list, top_pick_order = \
        utils.get_top_picks(teams_selected_2, LOTTERY_INFO)

    assert top_pick_list == []
    assert top_pick_order == []

    top_pick_list, top_pick_order = \
        utils.get_top_picks(teams_selected_3, LOTTERY_INFO)

    assert top_pick_list == [10, 8, 5]
    assert top_pick_order == [1, 10, 5, 8]


def test_update_teams():
    """ This function tests update_teams
    in app.utils.py
    """

    teams_selected_1 = []
    teams_selected_2 = [14, 13, 11]
    teams_selected_3 = [14, 13, 12, 10, 9,
                        8, 6, 5, 4, 3, 11]

    top_pick_list_1 = []
    top_pick_list_2 = [12]
    top_pick_list_3 = [11, 7]

    top_pick_order_1 = []
    top_pick_order_2 = []
    top_pick_order_3 = [11]

    request = Request()
    request.method = "POST"
    request.form = {}
    request.form['teams'] = 'Trailblazers'

    teams_selected, top_pick_list, top_pick_order, current_slot = \
        utils.update_teams(LOTTERY_INFO, top_pick_list_1,
                           teams_selected_1, top_pick_order_1,
                           request)

    assert teams_selected == [14]
    assert top_pick_list == []
    assert top_pick_order == []
    assert current_slot == 14

    request.form['teams'] = 'Wizards'

    teams_selected, top_pick_list, top_pick_order, current_slot = \
        utils.update_teams(LOTTERY_INFO, top_pick_list_2,
                           teams_selected_2, top_pick_order_2,
                           request)

    assert teams_selected == [14, 13, 11, 9]
    assert top_pick_list == [12, 10]
    assert top_pick_order == []
    assert current_slot == 11

    request.form['teams'] = 'Cavaliers'

    teams_selected, top_pick_list, top_pick_order, current_slot = \
        utils.update_teams(LOTTERY_INFO, top_pick_list_3,
                           teams_selected_3, top_pick_order_3,
                           request)

    assert teams_selected == [14, 13, 12, 10, 9,
                              8, 6, 5, 4, 3, 11, 2]
    assert top_pick_list == [11, 7]
    assert top_pick_order == [11, 2]
    assert current_slot == 3


def test_fast_forward():
    """ This function tests fast_forward
    in app.utils.py
    """

    teams_selected_1 = [14, 13, 11, 9, 8, 6, 5, 3]
    teams_selected_2 = [10]
    teams_selected_3 = [14, 13, 8]

    top_pick_list_1 = [12, 10, 7, 4]
    top_pick_list_2 = [14, 13, 12, 11]
    top_pick_list_3 = [12, 11, 10, 9]

    current_slot_1 = 7
    current_slot_2 = 14
    current_slot_3 = 12

    teams_selected, current_slot = \
        utils.fast_forward(LOTTERY_INFO,
                           top_pick_list_1,
                           teams_selected_1,
                           current_slot_1)

    assert teams_selected == [14, 13, 11, 9, 8,
                              6, 5, 3, 2, 1]
    assert current_slot == 5

    teams_selected, current_slot = \
        utils.fast_forward(LOTTERY_INFO,
                           top_pick_list_2,
                           teams_selected_2,
                           current_slot_2)

    assert teams_selected == [10, 9, 8, 7, 6,
                              5, 4, 3, 2, 1]
    assert current_slot == 5

    teams_selected, current_slot = \
        utils.fast_forward(LOTTERY_INFO,
                           top_pick_list_3,
                           teams_selected_3,
                           current_slot_3)

    assert teams_selected == [14, 13, 8, 7, 6,
                              5, 4, 3, 2, 1]
    assert current_slot == 5


def test_populate_dropdown():
    """ This function tests
    populate_dropdown in app.utils.py
    """

    teams_selected_1 = []
    teams_selected_2 = [14, 13, 11]
    teams_selected_3 = [14, 13, 12, 10, 9,
                        8, 6, 5, 4, 3, 11]
    teams_selected_4 = [14, 13, 12, 10, 9,
                        8, 6, 5, 4, 3, 11, 7, 2]

    top_pick_list_1 = []
    top_pick_list_2 = [12]
    top_pick_list_3 = [11, 7]
    top_pick_list_4 = [11, 7]

    top_pick_order_1 = []
    top_pick_order_2 = []
    top_pick_order_3 = [11]
    top_pick_order_4 = [11, 7, 2]

    current_slot_1 = 14
    current_slot_2 = 12
    current_slot_3 = 3
    current_slot_4 = 1

    teams, teams_selected, top_pick_order = \
        utils.populate_dropdown(LOTTERY_INFO, top_pick_list_1,
                                teams_selected_1, top_pick_order_1,
                                current_slot_1)

    assert teams == ['Trailblazers', 'Pelicans', 'Kings',
                     'Spurs', 'Suns', None]
    assert teams_selected == []
    assert top_pick_order == []

    teams, teams_selected, top_pick_order = \
        utils.populate_dropdown(LOTTERY_INFO, top_pick_list_2,
                                teams_selected_2, top_pick_order_2,
                                current_slot_2)

    assert teams == ['Suns', 'Wizards', 'Hornets',
                     'Bulls', None]
    assert teams_selected == [14, 13, 11]
    assert top_pick_order == []

    teams, teams_selected, top_pick_order = \
        utils.populate_dropdown(LOTTERY_INFO, top_pick_list_3,
                                teams_selected_3, top_pick_order_3,
                                current_slot_3)

    assert teams == ['Bulls', 'Cavaliers', 'Warriors', None]
    assert teams_selected == [14, 13, 12, 10, 9,
                              8, 6, 5, 4, 3, 11]
    assert top_pick_order == [11]

    teams, teams_selected, top_pick_order = \
        utils.populate_dropdown(LOTTERY_INFO, top_pick_list_4,
                                teams_selected_4, top_pick_order_4,
                                current_slot_4)

    assert teams == [None]
    assert teams_selected == [14, 13, 12, 10, 9,
                              8, 6, 5, 4, 3, 11,
                              7, 2, 1]
    assert top_pick_order == [11, 7, 2, 1]


def test_draft_order():
    """ This function tests
    draft_order in app.utils.py
    """

    teams_selected_1 = []
    teams_selected_2 = [14, 13, 11]
    teams_selected_3 = [14, 13, 12, 10, 9,
                        8, 6, 5, 4, 3, 11]
    teams_selected_4 = [14, 13, 12, 10, 9,
                        8, 6, 5, 4, 3, 11, 7, 2]

    selections = utils.draft_order(LOTTERY_INFO,
                                   teams_selected_1)

    assert selections == {14: '14. ', 13: '13. ',
                          12: '12. ', 11: '11. ',
                          10: '10. ', 9: '9. ',
                          8: '8. ', 7: '7. ',
                          6: '6. ', 5: '5. ', 4: '4. ',
                          3: '3. ', 2: '2. ', 1: '1. '}

    selections = utils.draft_order(LOTTERY_INFO,
                                   teams_selected_2)

    assert selections[14] == '14. Trailblazers'
    assert selections[13] == '13. Pelicans'
    assert selections[12] == '12. Spurs'

    selections = utils.draft_order(LOTTERY_INFO,
                                   teams_selected_3)

    assert selections[14] == '14. Trailblazers'
    assert selections[9] == '9. Hornets'
    assert selections[4] == '4. Spurs'

    selections = utils.draft_order(LOTTERY_INFO,
                                   teams_selected_4)

    assert selections[4] == '4. Spurs'
    assert selections[3] == '3. Bulls'
    assert selections[2] == '2. Cavaliers'
