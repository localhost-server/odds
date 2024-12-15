import pytest
from oddsportal.tournament import Tournament

def test_init_exists():
    nfl = Tournament('/american-football/usa/nfl')
    assert nfl.tournament == '/american-football/usa/nfl'
