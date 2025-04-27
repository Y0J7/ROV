import unittest
from src.components.controls import Controls

class TestControls(unittest.TestCase):
    
    def setUp(self):
        self.controls = Controls()

    def test_button_press(self):
        self.controls.handle_button_press('forward')
        self.assertEqual(self.controls.current_state, 'moving_forward')

    def test_button_release(self):
        self.controls.handle_button_press('forward')
        self.controls.handle_button_release('forward')
        self.assertEqual(self.controls.current_state, 'stopped')

    def test_invalid_button_press(self):
        with self.assertRaises(ValueError):
            self.controls.handle_button_press('invalid')

if __name__ == '__main__':
    unittest.main()