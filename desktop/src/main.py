"""NoteHub Desktop Application - Main Entry Point."""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QSettings

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import APP_NAME, APP_ORG, DEFAULT_BACKEND_URL, DARK_THEME, DEBUG
from logger import setup_logging, get_logger
from api.client import NoteHubClient
from ui.login_window import LoginWindow
from ui.main_window import MainWindow

# Setup logging
log_file = setup_logging()
logger = get_logger(__name__)


class NoteHubApp:
    """Main application controller."""
    
    def __init__(self):
        """Initialize application."""
        logger.info("Initializing NoteHub Desktop Application")
        logger.debug(f"Debug mode: {DEBUG}")
        logger.debug(f"Log file: {log_file}")
        
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(APP_NAME)
        self.app.setOrganizationName(APP_ORG)
        
        logger.debug("Qt Application created")
        
        # Apply dark theme
        self.app.setStyleSheet(DARK_THEME)
        logger.debug("Dark theme applied")
        
        # Settings
        self.settings = QSettings()
        
        # Get backend URL from settings or use default
        backend_url = self.settings.value("backend_url", DEFAULT_BACKEND_URL)
        logger.info(f"Backend URL: {backend_url}")
        
        # API Client
        self.client = NoteHubClient(backend_url)
        logger.debug("API client initialized")
        
        # Windows
        self.login_window = None
        self.main_window = None
        
        # Show login
        self.show_login()
    
    def show_login(self):
        """Show login window."""
        logger.info("Showing login window")
        self.login_window = LoginWindow(self.client)
        self.login_window.login_successful.connect(self.on_login_success)
        self.login_window.show()
        logger.debug("Login window displayed")
    
    def on_login_success(self, token: str):
        """
        Handle successful login.
        
        Args:
            token: Access token
        """
        logger.info(f"Login successful, token: {token[:20]}...")
        try:
            # Get current user info
            logger.debug("Fetching current user info")
            user = self.client.get_current_user()
            logger.info(f"User loaded: {user.username} (ID: {user.id})")
            
            # Close login window
            if self.login_window:
                self.login_window.close()
                logger.debug("Login window closed")
            
            # Show main window
            logger.info("Opening main window")
            self.main_window = MainWindow(self.client, user.username)
            self.main_window.show()
            logger.debug("Main window displayed")
            
        except Exception as e:
            logger.error(f"Failed to load user info: {e}", exc_info=True)
            QMessageBox.critical(
                self.login_window,
                "Error",
                f"Failed to load user info: {str(e)}"
            )
    
    def run(self) -> int:
        """
        Run the application.
        
        Returns:
            Exit code
        """
        logger.info("Starting Qt event loop")
        exit_code = self.app.exec()
        logger.info(f"Application exited with code: {exit_code}")
        return exit_code


def main():
    """Main entry point."""
    try:
        logger.info("=" * 80)
        logger.info("NoteHub Desktop Application Starting")
        logger.info("=" * 80)
        app = NoteHubApp()
        exit_code = app.run()
        logger.info("Application shutdown complete")
        sys.exit(exit_code)
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
