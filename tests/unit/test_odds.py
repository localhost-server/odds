import pytest
from oddsportal.data import bet_types, bet_scope, sport

def test_bet_types():
    assert bet_types['ah']['id'] == 5

def test_bet_scope():
    assert bet_scope['1'] == 'FT including OT'


def test_sport():
    assert sport['soccer'] == 1