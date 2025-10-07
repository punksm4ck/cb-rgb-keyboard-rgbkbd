import unittest

class GUITests(unittest.TestCase):
    def test_rgbgui_exists(self):
        self.assertTrue(os.path.exists("rgbgui"), "rgbgui launcher missing")

if __name__ == "__main__":
    unittest.main()
