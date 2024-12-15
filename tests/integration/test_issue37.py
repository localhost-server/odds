from oddsportal import Match

def test_init_from_url(caplog):    
    match = Match.from_url(url = 'https://www.oddsportal.com/baseball/usa/mlb-2018/san-diego-padres-philadelphia-phillies-OtK4wHIb')
    match.handicap_with_tightest_spread(('over-under', 1))
    assert 'Error while calculating average odds for bet type' in caplog.text
