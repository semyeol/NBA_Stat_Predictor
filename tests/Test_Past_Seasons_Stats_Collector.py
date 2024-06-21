import sys
sys.path.insert(0, '/Users/sem/SWA/Application of SWA/NBA_Stat_Predictor')

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import pandas as pd
from src.app.utils.Past_Seasons_Stats_Collector import get_past_seasons_stats

class TestGetPastSeasonsStats(unittest.TestCase):
    @patch('requests.get')
    @patch('pandas.read_html')
    def test_get_past_seasons_stats(self, mock_read_html, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<div id="div_per_game">mocked response text</div>'
        mock_get.return_value = mock_response

        mock_df = pd.DataFrame({
                                'Season': ['2021-22', '2022-23', '2023-24'], 
                                'Tm': ['LAL', 'LAL', 'LAL'],
                                'Player Name': ['player_name', 'player_name', 'player_name']
                                })
        
        mock_read_html.return_value = [mock_df]

        result = get_past_seasons_stats('player_name')

        mock_get.assert_called_once_with('https://www.basketball-reference.com/players/n/namepl01.html')
        call_args = mock_read_html.call_args
        called_with_stringio = call_args[0][0]
        self.assertIsInstance(called_with_stringio, StringIO)
        self.assertEqual(called_with_stringio.getvalue(), '<div id="div_per_game">mocked response text</div>')
        self.assertTrue(result.equals(mock_df))

if __name__ == '__main__':
    unittest.main()
