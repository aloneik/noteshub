"""Login and Registration Window."""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QTabWidget,
    QFormLayout,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from api.client import NoteHubClient, APIError


class LoginWindow(QWidget):
    """Login and registration window."""
    
    # Signal emitted when login is successful
    login_successful = Signal(str)  # Emits access token
    
    def __init__(self, client: NoteHubClient):
        """
        Initialize login window.
        
        Args:
            client: API client instance
        """
        super().__init__()
        self.client = client
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("NoteHub - Login")
        self.setFixedSize(400, 350)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("NoteHub")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Your notes and plans, organized")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #888888; font-size: 12px;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        # Tab widget for Login/Register
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_login_tab(), "Login")
        self.tabs.addTab(self.create_register_tab(), "Register")
        layout.addWidget(self.tabs)
        
        self.setLayout(layout)
    
    def create_login_tab(self) -> QWidget:
        """Create login tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Form
        form = QFormLayout()
        form.setSpacing(10)
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        form.addRow("Username:", self.login_username)
        
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.returnPressed.connect(self.handle_login)
        form.addRow("Password:", self.login_password)
        
        layout.addLayout(form)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        login_btn.setMinimumHeight(40)
        layout.addWidget(login_btn)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_register_tab(self) -> QWidget:
        """Create registration tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Form
        form = QFormLayout()
        form.setSpacing(10)
        
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Choose a username")
        form.addRow("Username:", self.register_username)
        
        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText("Choose a password")
        self.register_password.setEchoMode(QLineEdit.Password)
        form.addRow("Password:", self.register_password)
        
        self.register_password_confirm = QLineEdit()
        self.register_password_confirm.setPlaceholderText("Confirm password")
        self.register_password_confirm.setEchoMode(QLineEdit.Password)
        self.register_password_confirm.returnPressed.connect(self.handle_register)
        form.addRow("Confirm:", self.register_password_confirm)
        
        layout.addLayout(form)
        
        # Register button
        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.handle_register)
        register_btn.setMinimumHeight(40)
        layout.addWidget(register_btn)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def handle_login(self):
        """Handle login button click."""
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Please enter both username and password."
            )
            return
        
        try:
            # Attempt login
            token = self.client.login(username, password)
            
            # Success - emit signal
            self.login_successful.emit(token)
            
        except APIError as e:
            QMessageBox.critical(
                self,
                "Login Failed",
                f"Failed to login: {e.message}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"An unexpected error occurred: {str(e)}"
            )
    
    def handle_register(self):
        """Handle registration button click."""
        username = self.register_username.text().strip()
        password = self.register_password.text()
        password_confirm = self.register_password_confirm.text()
        
        # Validation
        if not username or not password:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Please enter both username and password."
            )
            return
        
        if len(username) < 3:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Username must be at least 3 characters long."
            )
            return
        
        if len(password) < 6:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Password must be at least 6 characters long."
            )
            return
        
        if password != password_confirm:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Passwords do not match."
            )
            return
        
        try:
            # Attempt registration
            user = self.client.register(username, password)
            
            # Success - show message and switch to login tab
            QMessageBox.information(
                self,
                "Registration Successful",
                f"Welcome, {user.username}! Please login to continue."
            )
            
            # Switch to login tab and pre-fill username
            self.tabs.setCurrentIndex(0)
            self.login_username.setText(username)
            self.login_password.setFocus()
            
            # Clear registration fields
            self.register_username.clear()
            self.register_password.clear()
            self.register_password_confirm.clear()
            
        except APIError as e:
            QMessageBox.critical(
                self,
                "Registration Failed",
                f"Failed to register: {e.message}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"An unexpected error occurred: {str(e)}"
            )
