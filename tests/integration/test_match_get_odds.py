from oddsportal import Match
import json

def test_get_odds_ah_1():
    with open('data/feed/match-event/1-5-E3C0Iu6A-5-1.json') as fs:
        data = json.load(fs)
        expected = data['d']['oddsdata']
    match = Match.from_url(url = 'https://www.oddsportal.com/american-football/usa/nfl/new-orleans-saints-minnesota-vikings-E3C0Iu6A')
    extracted = match.get_odds(('ah', 1))
    assert extracted['back'].keys()  == expected['back'].keys()

def test_get_odds_ah_3():
    with open('data/feed/match-event/1-5-E3C0Iu6A-5-3.json') as fs:
        data = json.load(fs)
        expected = data['d']['oddsdata']
    match = Match.from_url(url = 'https://www.oddsportal.com/american-football/usa/nfl/new-orleans-saints-minnesota-vikings-E3C0Iu6A')
    extracted = match.get_odds(('ah', 3))
    assert extracted['back'].keys()  == expected['back'].keys()

def test_get_odds_1x2_11():
    with open('data/feed/match-event/1-5-E3C0Iu6A-1-11.json') as fs:
        data = json.load(fs)
        expected = data['d']['oddsdata']
    match = Match.from_url(url = 'https://www.oddsportal.com/american-football/usa/nfl/new-orleans-saints-minnesota-vikings-E3C0Iu6A')
    extracted = match.get_odds(('1x2', 11))
    assert extracted['back'].keys()  == expected['back'].keys()

def test_get_odds_over_under_1():
    with open('data/feed/match-event/1-5-E3C0Iu6A-2-1.json') as fs:
        data = json.load(fs)
        expected = data['d']['oddsdata']
    match = Match.from_url(url = 'https://www.oddsportal.com/american-football/usa/nfl/new-orleans-saints-minnesota-vikings-E3C0Iu6A')
    extracted = match.get_odds(('over-under', 1))
    assert extracted['back'].keys()  == expected['back'].keys()

def test_get_odds_over_under_2():
    with open('data/feed/match-event/1-5-E3C0Iu6A-2-3.json') as fs:
        data = json.load(fs)
        expected = data['d']['oddsdata']
    match = Match.from_url(url = 'https://www.oddsportal.com/american-football/usa/nfl/new-orleans-saints-minnesota-vikings-E3C0Iu6A')
    extracted = match.get_odds(('over-under', 3))
    assert extracted['back'].keys()  == expected['back'].keys()

def test_get_odds_home_away_1():
    with open('data/feed/match-event/1-5-E3C0Iu6A-3-1.json') as fs:
        data = json.load(fs)
        expected = data['d']['oddsdata']
    match = Match.from_url(url = 'https://www.oddsportal.com/american-football/usa/nfl/new-orleans-saints-minnesota-vikings-E3C0Iu6A')
    extracted = match.get_odds(('home-away', 1))
    assert extracted['back'].keys()  == expected['back'].keys()
