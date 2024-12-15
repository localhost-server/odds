import pytest
from oddsportal.team import Team

def test_init():
    home = Team(name = 'Minnesota Vikings')
    away = Team(name = 'Minnesota Vikings')
    assert home.name == 'Minnesota Vikings'
    assert home == away

