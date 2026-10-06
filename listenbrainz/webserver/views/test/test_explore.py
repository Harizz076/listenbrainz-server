import datetime
from unittest import mock
from unittest.mock import patch

from listenbrainz.tests.integration import IntegrationTestCase


class ExploreViewsTestCase(IntegrationTestCase):

    def test_hue_sound(self):
        resp = self.client.get(self.custom_url_for('explore.index', path="huesound"))
        self.assert200(resp)

    def test_similar_users(self):
        resp = self.client.get(self.custom_url_for('explore.index', path="similar-users"))
        self.assert200(resp)

    def test_fresh_releases(self):
        resp = self.client.get(self.custom_url_for('explore.index', path="fresh-releases"))
        self.assert200(resp)

    @patch('listenbrainz.db.fresh_releases.get_sitewide_fresh_releases', side_effect=[([], 0), ([], 0), ([], 0)])
    def test_fresh_releases_api(self, mock_fresh):
        resp = self.client.get(self.custom_url_for('explore_api_v1.get_fresh_releases'))
        self.assert200(resp)
        mock_fresh.assert_called_with(mock.ANY, datetime.date.today(), 14, 'release_date', True, True)

        resp = self.client.get(self.custom_url_for('explore_api_v1.get_fresh_releases', release_date="2022-01-01", days=5))
        self.assert200(resp)
        mock_fresh.assert_called_with(mock.ANY, datetime.date(year=2022, month=1, day=1), 5, 'release_date', True, True)

        resp = self.client.get(self.custom_url_for('explore_api_v1.get_fresh_releases', sort="artist_credit_name", past=False))
        self.assert200(resp)
        mock_fresh.assert_called_with(mock.ANY, datetime.date.today(), 14, 'artist_credit_name', False, True)

    @patch('listenbrainz.db.fresh_releases.couchdb.fetch_all_data')
    def test_fresh_releases_api_uses_cached_data_without_mb_database(self, mock_fetch_all_data):
        today = datetime.date.today()
        mock_fetch_all_data.return_value = [{
            "releases": [{
                "release_date": today.isoformat(),
                "release_mbid": "25f0d2c0-2c42-4f33-a1e0-081084a1a012",
                "release_name": "Local Release",
                "artist_credit_name": "Local Artist",
                "artist_mbids": ["b1bfbb6e-2a7f-4a04-b7f9-b0e37cc693e2"],
                "release_group_mbid": "fc3b2f15-6b16-4be0-a7f4-611762b8ea83",
                "release_group_primary_type": "Album",
                "release_group_secondary_type": None,
                "release_tags": ["electronic"],
                "listen_count": 12,
                "caa_id": None,
                "caa_release_mbid": None,
            }]
        }]

        resp = self.client.get(
            self.custom_url_for('explore_api_v1.get_fresh_releases', days=1)
        )

        self.assert200(resp)
        self.assertEqual(resp.json["payload"]["total_count"], 1)
        self.assertEqual(
            resp.json["payload"]["releases"][0]["release_name"],
            "Local Release"
        )
        mock_fetch_all_data.assert_called_once_with("fresh_releases")

    def test_lb_radio(self):
        resp = self.client.get(self.custom_url_for('explore.index', path="lb-radio"))
        self.assert200(resp)
