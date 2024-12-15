from oddsportal import Match, Team
import datetime
from unittest import mock
import pytest

@pytest.fixture()
def match():
    html = open('data/american-footbal/usa/nfl/new-orleans-saints-minnesota-vikings-E3C0Iu6A.html').read()
    with mock.patch('oddsportal.match.get', return_value=html):
        result = Match.from_url(url = 'https://www.oddsportal.com/american-football/usa/nfl/new-orleans-saints-minnesota-vikings-E3C0Iu6A')
        yield result

def test_init():
    match = Match(id = '/american-football/usa/nfl/new-orleans-saints-minnesota-vikings-E3C0Iu6A',
                  event_id = 'E3C0Iu6A',
                  sport_id = 5,
                  date = datetime.date(2022, 10, 2),
                  home_team = Team(name = 'New Orleans Saints'),
                  away_team = Team(name = 'Minnesota Vikings'),
                  event_stage = 'Finished')
    assert match.id == '/american-football/usa/nfl/new-orleans-saints-minnesota-vikings-E3C0Iu6A'

def test_init_from_url(match):
    assert match.id == '/american-football/usa/nfl/new-orleans-saints-minnesota-vikings-E3C0Iu6A'
    assert match.event_id == 'E3C0Iu6A'
    assert match.sport_id == 5
    assert match.date == datetime.date(2022, 10, 2)
    assert match.home_team.name == 'New Orleans Saints'
    assert match.away_team.name == 'Minnesota Vikings'
    assert match.event_stage == 'Finished'

def test_get_odds_url(match):
    assert match.get_odds_url(('ah', 1)) == 'https://www.oddsportal.com/feed/match-event/1-5-E3C0Iu6A-5-1-yja2d.dat'
    assert match.get_odds_url(('ah', 3)) == 'https://www.oddsportal.com/feed/match-event/1-5-E3C0Iu6A-5-3-yja2d.dat'
    assert match.get_odds_url(('over-under', 1)) == 'https://www.oddsportal.com/feed/match-event/1-5-E3C0Iu6A-2-1-yja2d.dat'
    assert match.get_odds_url(('over-under', 3)) == 'https://www.oddsportal.com/feed/match-event/1-5-E3C0Iu6A-2-3-yja2d.dat'
    