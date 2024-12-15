import pytest
from oddsportal.tournament import Tournament
from unittest import mock

@pytest.fixture
def tournament():
    html = open('data/american-footbal/usa/nfl/nfl-without-next-matches.html').read()
    with mock.patch('oddsportal.tournament.get', return_value=html):    
        result = Tournament('/american-football/usa/nfl')
        yield result 

def test_next_matches_urls(tournament):
    expected = None
    result = tournament.next_matches_urls
    assert result == expected