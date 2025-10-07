import unittest, os

class PluginTests(unittest.TestCase):
    def test_plugin_load(self):
        for f in os.listdir("plugins"):
            if f.endswith(".py"):
                try:
                    __import__(f[:-3])
                except Exception as e:
                    self.fail(f"Plugin {f} failed to load: {e}")

if __name__ == "__main__":
    unittest.main()
