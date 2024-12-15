from oddsportal import Match, Team
import datetime
from unittest import mock
import pytest

@pytest.fixture()
def match():
    html = open('data/hockey/usa/nhl/los-angeles-kings-buffalo-sabres-UVhOii9p.html').read()
    with mock.patch('oddsportal.match.get', return_value=html):
        result = Match.from_url(url = 'https://www.oddsportal.com/hockey/usa/nhl-2022-2023/los-angeles-kings-buffalo-sabres-UVhOii9p')
        # result = Match.from_url(url = 'https://www.oddsportal.com/hockey/usa/nhl/los-angeles-kings-buffalo-sabres-UVhOii9p')
        yield result

def test_init_from_url(match):
    assert match.id == '/hockey/usa/nhl-2022-2023/los-angeles-kings-buffalo-sabres-UVhOii9p'
    assert match.event_id == 'UVhOii9p'
    assert match.sport_id == 4
    assert match.date == datetime.date(2023, 2, 13)
    assert match.home_team.name == 'Los Angeles Kings'
    assert match.away_team.name == 'Buffalo Sabres'
    assert match.event_stage == 'Scheduled'
