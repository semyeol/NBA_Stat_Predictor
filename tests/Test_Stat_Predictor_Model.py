import sys
sys.path.insert(0, '/Users/sem/SWA/Application of SWA/NBA_Stat_Predictor')

import unittest
import pandas as pd
from app.model.Stat_Predictor_Model import predict_points
from app.model.Stat_Predictor_Model import predict_assists
from app.model.Stat_Predictor_Model import predict_rebounds

class TestPredictPoints(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'PTS_weighted': [10, 20, 30, 40, 50],
            'AST_weighted': [5, 10, 15, 20, 25],
            'TRB_weighted': [3, 6, 9, 12, 15],
            'Player Name': ['Player1', 'Player2', 'Player3', 'Player4', 'Player5'],
            'GmSc': [10, 20, 30, 30, 30],
            'TOV_df2': [0, 1, 2, 3, 4]
        })

    def test_predict_points(self):
        result = predict_points(self.df)
        self.assertIsInstance(result, (int, float))

    def test_predict_assists(self):
        result = predict_assists(self.df)
        self.assertIsInstance(result, (int, float))

    def test_predict_rebounds(self):
        result = predict_rebounds(self.df)
        self.assertIsInstance(result, (int, float))

if __name__ == '__main__':
    unittest.main()