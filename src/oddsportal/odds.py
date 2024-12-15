from statistics import harmonic_mean

def to_american(odds):
    try:
        iter(odds)
    except TypeError:
        odds = [odds]
    result = [] 
    for odd in odds:
        if odd >= 2:
            result.append((odd - 1)*100)
        elif odd < 2:
            result.append(-100 / (odd - 1))
    return result

def to_decimal(odds):
    try:
        iter(odds)
    except TypeError:
        odds = [odds]
    result = [] 
    for odd in odds:
        if odd > 0:
            result.append((odd / 100) + 1)
        elif odd < 0:
            result.append((100 / abs(odd)) + 1)
    return result

def average_odds(odds):
    if isinstance(list(odds.values())[0], dict):
        odds = [[odd['0'], odd['1']] for odd in odds.values() if isinstance(odd, dict)]
    else:
        odds = [odd for odd in list(odds.values()) if len (odd) == 2]
    home, away = zip(*odds)
    home_average = harmonic_mean(home)
    away_average = harmonic_mean(away)
    return [home_average, away_average]

