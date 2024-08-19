import os
import datetime as dt
import unittest
from rumorz.client import RumorzClient, RumorzAPIException
from rumorz.enums import Lookback, ScreenerValues, EntityType

rumorz = RumorzClient(api_key=os.environ['RUMORZ_API_KEY'],
                      api_url='http://0.0.0.0:80')


class TestRumorz(unittest.TestCase):

    def test_valid_screener_chg_lookback_request(self):
        person_screener = rumorz.graph.get_screener(
            lookback=Lookback.THREE_MONTHS,
            entity_type=EntityType.PERSON
        )
        self.assertTrue(len(person_screener['data']) > 0)

    def test_valid_screener_abs_timestamp_request(self):
        to_timestamp, from_timestamp = dt.datetime.utcnow().isoformat(), (dt.datetime.utcnow() - dt.timedelta(days=14)).isoformat()
        person_screener = rumorz.graph.get_screener(
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
            entity_type=EntityType.PERSON
        )
        self.assertTrue(len(person_screener) > 0)

    def test_invalid_screener_abs_timestamp_request(self):
        from_timestamp, to_timestamp = (dt.datetime.utcnow() - dt.timedelta(days=7)).isoformat(), dt.datetime.utcnow().isoformat()
        try:
            person_screener = rumorz.graph.get_screener(
                from_timestamp=5.2,
                to_timestamp=to_timestamp,
                entity_type=EntityType.PERSON
            )
            print(person_screener)
        except Exception as e:
            self.assertTrue(isinstance(e, RumorzAPIException))


    def test_posts(self):
        posts = rumorz.graph.get_posts(
            type=EntityType.FINANCIAL_ASSET,
            name="Bitcoin",
            symbol="BTC",
            lookback=Lookback.ONE_WEEK,
            page=2,
        )
        self.assertTrue(len(posts) > 0)


    def test_time_series(self):
        timeseries = rumorz.graph.get_time_series(
            type=EntityType.FINANCIAL_ASSET,
            name="Bitcoin",
            symbol="BTC",
            lookback=Lookback.ONE_WEEK,
            page=1,
        )
        self.assertTrue(len(timeseries) > 0)