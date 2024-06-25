import sys
sys.path.insert(0, '/Users/sem/SWA/Application of SWA/NBA_Stat_Predictor')

import unittest
from unittest.mock import patch, MagicMock, call
import pandas as pd
from app.utils.Against_Opponent_Stats_Collector import get_against_opp_stats

class TestGetAgainstOppStats(unittest.TestCase):
    @patch('requests.get')
    @patch('pandas.read_html')
    def test_get_against_opp_stats(self, mock_read_html, mock_get):
        mock_response1 = MagicMock()
        mock_response1.status_code = 200
        mock_response1.text = '<div id="div_pgl_basic">mocked response text</div>'
        
        mock_response2 = MagicMock()
        mock_response2.status_code = 200
        mock_response2.text = '<div id="div_pgl_basic">mocked response text</div>'

        mock_response3 = MagicMock()
        mock_response3.status_code = 200
        mock_response3.text = '<div id="div_pgl_basic">mocked response text</div>'

        mock_get.side_effect = [mock_response1, mock_response2, mock_response3]

        mock_df1 = pd.DataFrame({
                                'GS': ['1', '1', '1'],
                                'Opp': ['LAC', 'LAC', 'LAC'],
                                'Player Name': ['player_name', 'player_name', 'player_name']
                                })
        
        mock_df2 = pd.DataFrame({
                                'GS': ['1', '1', '1'],
                                'Opp': ['LAC', 'LAC', 'LAC'],
                                'Player Name': ['player_name', 'player_name', 'player_name']
                                })
        
        mock_df3 = pd.DataFrame({
                                'GS': ['1', '1', '1'],
                                'Opp': ['LAC', 'LAC', 'LAC'],
                                'Player Name': ['player_name', 'player_name', 'player_name']
                                })
        
        mock_read_html.side_effect = [[mock_df1], [mock_df2], [mock_df3]]

        result = get_against_opp_stats('player_name', 'LAC')

        calls = [call('https://www.basketball-reference.com/players/n/namepl01/gamelog/2024'),
                 call('https://www.basketball-reference.com/players/n/namepl01/gamelog/2023'),
                 call('https://www.basketball-reference.com/players/n/namepl01/gamelog/2022')]
        mock_get.assert_has_calls(calls, any_order=True)
        self.assertTrue(result.equals(pd.concat([mock_df1, mock_df2, mock_df3])))

if __name__ == '__main__':
    unittest.main()


        
    