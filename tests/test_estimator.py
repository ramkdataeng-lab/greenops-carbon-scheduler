import unittest
from estimator import estimate_query_carbon

class TestEstimator(unittest.TestCase):
    def test_estimate_basic(self):
        result = estimate_query_carbon('Large', 300, 'us-east-1')
        self.assertEqual(result['warehouse_size'], 'Large')
        self.assertEqual(result['duration_seconds'], 300)
        self.assertEqual(result['region'], 'us-east-1')
        # Credits per hour for Large is 8
        # Watts per credit is 200
        # Power kW = (8 * 200) / 1000 = 1.6
        # Time hours = 300 / 3600 = 0.0833
        # Grid intensity us-east-1 = 380
        # PUE = 1.1
        # Emission = 1.6 * 0.0833 * 1.1 * 380 = 55.72
        self.assertAlmostEqual(result['estimated_emissions_gCO2'], 55.73, places=1)

    def test_regional_difference(self):
        virginia = estimate_query_carbon('Small', 3600, 'us-east-1')
        oregon = estimate_query_carbon('Small', 3600, 'us-west-2')
        self.assertLess(oregon['estimated_emissions_gCO2'], virginia['estimated_emissions_gCO2'])

if __name__ == '__main__':
    unittest.main()
