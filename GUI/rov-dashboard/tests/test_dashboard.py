import unittest
from src.components.dashboard import Dashboard

class TestDashboard(unittest.TestCase):
    
    def setUp(self):
        self.dashboard = Dashboard()

    def test_render_initial_state(self):
        # Test that the dashboard renders the initial state correctly
        self.dashboard.render()
        self.assertTrue(self.dashboard.is_rendered)

    def test_update_display_with_telemetry(self):
        # Test that the dashboard updates correctly with telemetry data
        telemetry_data = {'speed': 5, 'depth': 10}
        self.dashboard.update_display(telemetry_data)
        self.assertEqual(self.dashboard.current_speed, 5)
        self.assertEqual(self.dashboard.current_depth, 10)

if __name__ == '__main__':
    unittest.main()