import logging
from flask import render_template, request
from app.lottery_odds import update_odds, LOTTERY_INFO
import app.utils as utils
from app import app

# TESTS
@app.route('/',  methods=['POST', 'GET'])
def show_tables(teams_selected=''):
    """ This function creates the updated
    lottery odds table as teams are revealed.
    Although no variables are explicitly provided
    to this main function, the following describes
    global variables and form data used

    teams_selected (list): List of key values for
        LOTTERY_INFO that represent the reverse
        standings order. This list is filled
        in as teams are revealed. This gets
        overwritten with the request arguments
        of teams already selected
    top_pick_list (list): List of key values for
        LOTTERY_INFO that correspond to the teams
        that are "skipped" as the back of the
        lottery is revealed. This means that team
        has a pick in the top 4
    top_pick_order (list): List of key values for
        LOTTERY_INFO that correspond to the teams
        that are revealed starting in the top 4
    LOTTERY_INFO (dict): Dictionary keyed by
        reverse standings order, with dictionary
        values containing 'name' and 'id' keys
        for the team
    """

    if request.method == 'POST':
        teams_selected = \
            utils.get_teams_selected(request, LOTTERY_INFO)
    else:
        teams_selected = []

    current_slot = len(LOTTERY_INFO) - len(teams_selected)

    top_pick_list, top_pick_order = \
        utils.get_top_picks(teams_selected, LOTTERY_INFO)

    # Update the teams selected and those in the top 4
    if request.method == "POST" and request.form['teams'] is not None:
        teams_selected, top_pick_list, top_pick_order, current_slot = \
            utils.update_teams(LOTTERY_INFO, top_pick_list,
                               teams_selected, top_pick_order,
                               request)

    # If we know the top 4 teams already, we can fast forward
    # the draft lottery
    if current_slot < 14:
        if len(top_pick_list) == 4 and current_slot >= 5:
            teams_selected, current_slot = \
                utils.fast_forward(LOTTERY_INFO, top_pick_list,
                                   teams_selected, current_slot)


    # Populate the dropdown list in teams with teams
    # available to be selected
    teams, teams_selected, top_pick_order = \
        utils.populate_dropdown(LOTTERY_INFO,
                                top_pick_list,
                                teams_selected,
                                top_pick_order,
                                current_slot)

    
    # Update the draft order display
    selections = utils.draft_order(LOTTERY_INFO,
                                   teams_selected)

    logging.warning(str(teams_selected))
    logging.warning(str(top_pick_list))
    logging.warning(str(top_pick_order))
    # Calculate updated odds
    lotto_df = update_odds(teams_selected,
                           top_pick_list,
                           top_pick_order)

    return render_template('tables.html',
                            table=lotto_df.to_html(classes='data'),
                            teams=teams,
                            selections=selections)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
