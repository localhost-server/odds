import pytest
from oddsportal.team import Team
from oddsportal.tournament import Tournament
from oddsportal.match import Match
import datetime
import json
from unittest import mock

@pytest.fixture
def tournament():
    return_value = json.loads(open('data/all_matches_api_data.json').read())
    with mock.patch('oddsportal.tournament.Tournament.all_matches_api_data', return_value=return_value):
        result = Tournament('/american-football/usa/nfl')
        yield result 

def test_all_matches(tournament):
    expected = Match(id='/american-football/usa/nfl-2019-2020/kansas-city-chiefs-san-francisco-49ers-QNLis8yO/', 
                     event_id='QNLis8yO', 
                     sport_id=5, 
                     date=datetime.date(2020, 2, 2), 
                     home_team=Team(name='Kansas City Chiefs'), 
                     away_team=Team(name='San Francisco 49ers'),
                     event_stage = 'Finished')
    result = list(tournament.all_matches('2019/2020'))[0]
    assert result == expected