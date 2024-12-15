from dataclasses import dataclass
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
import json
import datetime
from dateutil import parser
import logging
from pathlib import Path
from .team import Team
from .utils import get
from .data import bet_types
from .odds import average_odds

logger = logging.getLogger(__name__)

@dataclass
class Match():
    id: str
    event_id: str
    sport_id: int
    date: datetime.date
    home_team: Team
    away_team: Team
    event_stage: str
    _xhash: str = None

    @property
    def xhash(self):
        if not self._xhash:
            soup = BeautifulSoup(get(f'https://www.oddsportal.com{self.id}'), 'lxml')
            event_tag = soup.find('event')
            if event_tag:
                data = json.loads(event_tag.get(':data'))
                self._xhash = unquote(data.get('eventData').get('xhash'))
        return self._xhash
    
    @classmethod
    def from_url(cls, url):
        soup = BeautifulSoup(get(url), 'lxml')
        data = json.loads(soup.find('event')[':data'])
        id = str(Path(urlparse(url).path))
        event_id = data['eventData']['id']
        sport_id = data['eventData']['sportId']

        print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        # dateString = data['eventBody']['startDate'].replace("&nbsp;", " ").replace("Today, ", "").replace("Tomorrow, ", "")
        # print(dateString)
        start_date = data['eventBody']['startDate']
        if isinstance(start_date, int):
            timestamp_utc = datetime.datetime.utcfromtimestamp(start_date)
        else:
            start_date_str = BeautifulSoup(start_date, 'html.parser').get_text()
            start_date_str = start_date_str.replace('\xa0', ' ').replace('Today, ', '').replace('Tomorrow, ', '')
            timestamp_utc = parser.parse(start_date_str)

        print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")

        # timestamp_utc = parser.parse(dateString)
        timestamp_utc = timestamp_utc.replace(tzinfo=datetime.timezone.utc)
        local_timezone = datetime.timezone(datetime.timedelta(hours=-5))
        timestamp_local = timestamp_utc.astimezone(local_timezone)
        date = timestamp_local.date()
        home_team = data['eventData']['home']
        away_team = data['eventData']['away']
        if data['eventData']['isFinished']:
            event_stage = 'Finished'
        else:
            event_stage = 'Scheduled'
        _xhash = unquote(data['eventData']['xhash'])

        return cls(id = id, 
                   event_id = event_id, 
                   sport_id = sport_id, 
                   date = date, 
                   home_team = Team(home_team), 
                   away_team = Team(away_team), 
                   event_stage = event_stage, 
                   _xhash = _xhash)

    def get_odds_url(self, bet):
        prefix = 'https://www.oddsportal.com/feed/match-event/'
        url = f'{prefix}1-{self.sport_id}-{self.event_id}-{bet_types[bet[0]]["id"]}-{bet[1]}-{self.xhash}.dat'
        print('UUUUUUUUUURRRRRRRRRRRRRRLLLLLLLLLLLLLLLL :', url)
        return url

    def get_odds(self, bet):
        logger.info(f'Scraping bet type {bet} for {self.id}')

        url = self.get_odds_url(bet)
        result = get(url, xhr=True)
        if not result:
            result = None
            logger.warning(f'Error while scraping bet type {bet} for {self.id}')
        else:
            if "{'e':'404'}" in result:
                logger.error('404 Client Error: Not Found')
            print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
            # print(result)
            print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
            result = json.loads(result)
            result = result.get('d').get('oddsdata')
        return result

    def get_average_odds(self, bet):
        data = self.get_odds(bet)
        if not data:
            result = None
        elif not data.get('back'):
            result = None
        else:
            result = []
            for handicap in data['back'].keys():
                odds = data['back'][handicap]['odds']
                tmp = {'average_odds': average_odds(odds), 'handicap': data['back'][handicap]['handicapValue']}
                spread = abs(tmp['average_odds'][0]) - abs(tmp['average_odds'][1])
                tmp['spread'] = spread
                result.append(tmp)
            result = list(sorted(result, key = lambda x: x['spread']))
        if not result:
            logger.warning(f'No odds available for bet type {bet} for {self.id}')
        return result
    
    def handicap_with_tightest_spread(self, bet):
        try:
            data = self.get_average_odds(bet)
        except KeyError:
            logger.error(f'Error while calculating average odds for bet type {bet} for {self.id}')
            data = None
        except ValueError:
            logger.error(f'Error while calculating average odds for bet type {bet} for {self.id}')
            data = None
        if not data:
            result = None
        else:
            result = min(data, key=lambda x:abs(x['spread']-0))
        return result
