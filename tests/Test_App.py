import unittest
from src.app.app import app  

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_predict_stats_route(self):
        test_cases = [
            {'player_name': 'LeBron James', 'team_name': 'LAC'},
            {'player_name': 'kyrie irving', 'team_name': 'BOS'},
            {'player_name': 'tYrese HaliburTon', 'team_name': 'MIL'},
            {'player_name': 'lamelo Ball', 'team_name': 'SAC'},
            {'player_name': 'Derrick White', 'team_name': 'MIN'},
            {'player_name': 'Precious Achiuwa', 'team_name': 'TOR'},
            {'player_name': 'Mikal Bridges', 'team_name': 'POR'},
        ]

        for test_case in test_cases:
            response = self.client.post('/predict_stats', data=test_case)
            self.assertEqual(response.status_code, 200)
        

if __name__ == '__main__':
    unittest.main()