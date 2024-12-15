from oddsportal import Match, Team
import datetime
from unittest import mock
import pytest

@pytest.fixture()
def match():
    html = open('data/hockey/usa/nhl/montreal-canadiens-chicago-blackhawks-Klu8tbue.html').read()
    with mock.patch('oddsportal.match.get', return_value=html):
        result = Match.from_url(url = 'https://www.oddsportal.com/hockeyl/usanhll/montreal-canadiens-chicago-blackhawks-Klu8tbue')
        yield result

def test_init_from_url(match):
    assert match.id == '/hockeyl/usanhll/montreal-canadiens-chicago-blackhawks-Klu8tbue'
    assert match.event_id == 'Klu8tbue'
    assert match.sport_id == 4
    assert match.date == datetime.date(2023, 2, 14)
    assert match.home_team.name == 'Montreal Canadiens'
    assert match.away_team.name == 'Chicago Blackhawks'
    assert match.event_stage == 'Scheduled'
