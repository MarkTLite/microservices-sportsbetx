from unittest.mock import patch, call
from sportsbetx.db import get_db

@patch('builtins.print')
def test_request_close_db(mocked_print,app): # test closing of db for each request.
    with app.app_context():
        get_db('postgresql')

    # ensure the list of prints called during a particular request has closed db.    
    assert call('closed db connection') in mocked_print.mock_calls 

def test_create_success(client):
    response = client.post('/odds/create', json={
    "league":"Premier League",
    "home_team":"Manchester United",
    "away_team":"Arsenal",
    "home_team_win_odds": 1,
    "away_team_win_odds": 2,
    "draw_odds": 5, 
    "game_date":"12/10/2022"
    })
    assert response.status_code == 200
    assert response.data == b'{"message":"Odds created"}\n'
