import pytest
from oddsportal.tournament import Tournament
from unittest import mock

@pytest.fixture
def tournament():
    html = open('data/american-footbal/usa/xfl/results.html').read()
    json = open('data/ajax-sport-country-tournament-archive_/5-4xTlzXUJ-1-0.json').read()
    with (
        mock.patch('oddsportal.tournament.Tournament.season_results_html', return_value=html),
        mock.patch('oddsportal.tournament.get', return_value=json)
    ):
        result = Tournament('/american-football/usa/xfl')
        yield result 

def test_all_matches_api_urls_without_odds(tournament):
    expected = None
    result = tournament.all_matches_api_urls('2023')
    print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    assert result == expected