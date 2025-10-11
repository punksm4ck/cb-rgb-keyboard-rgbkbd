import sys
import logging

class ApplicationLauncher:
    """ApplicationLauncher class"""

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        print('✅ Logging initialized')

def main() -> int:
    """main method"""
    launcher = ApplicationLauncher()
    launcher.setup_logging()
    print('✅ GUI launched successfully!')
if __name__ == '__main__':
    sys.exit(main())