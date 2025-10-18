"""Main application window."""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QTextEdit,
    QLineEdit,
    QLabel,
    QMessageBox,
    QSplitter,
    QFrame,
    QScrollArea,
    QDateEdit,
    QCheckBox,
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

from api.client import NoteHubClient, APIError
from models import Note, NoteWithPlans, Plan


class MainWindow(QMainWindow):
    """Main application window with notes and plans."""
    
    def __init__(self, client: NoteHubClient, username: str):
        """
        Initialize main window.
        
        Args:
            client: API client with active session
            username: Current user's username
        """
        super().__init__()
        self.client = client
        self.username = username
        self.current_note: NoteWithPlans | None = None
        self.notes: list[Note] = []
        
        self.setup_ui()
        self.load_notes()
    
    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle(f"NoteHub - {self.username}")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left sidebar (notes list)
        sidebar = self.create_sidebar()
        
        # Right panel (note editor)
        editor_panel = self.create_editor_panel()
        
        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(sidebar)
        splitter.addWidget(editor_panel)
        splitter.setSizes([300, 900])
        
        main_layout.addWidget(splitter)
        central.setLayout(main_layout)
        
        # Status bar
        self.statusBar().showMessage(f"Logged in as {self.username}")
    
    def create_sidebar(self) -> QWidget:
        """Create left sidebar with notes list."""
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setMaximumWidth(350)
        sidebar.setMinimumWidth(250)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Header
        header = QLabel("📝 My Notes")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # New note button
        new_note_btn = QPushButton("+ New Note")
        new_note_btn.clicked.connect(self.create_new_note)
        new_note_btn.setMinimumHeight(35)
        layout.addWidget(new_note_btn)
        
        # Notes list
        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.on_note_selected)
        layout.addWidget(self.notes_list)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_notes)
        layout.addWidget(refresh_btn)
        
        sidebar.setLayout(layout)
        return sidebar
    
    def create_editor_panel(self) -> QWidget:
        """Create right panel with note editor and plans."""
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Note title
        title_layout = QHBoxLayout()
        self.note_title = QLineEdit()
        self.note_title.setPlaceholderText("Note title...")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.note_title.setFont(title_font)
        self.note_title.setMinimumHeight(45)
        title_layout.addWidget(self.note_title)
        
        # Save button
        self.save_btn = QPushButton("💾 Save")
        self.save_btn.clicked.connect(self.save_note)
        self.save_btn.setMinimumWidth(100)
        self.save_btn.setMinimumHeight(45)
        self.save_btn.setEnabled(False)
        title_layout.addWidget(self.save_btn)
        
        # Delete button
        self.delete_btn = QPushButton("🗑️ Delete")
        self.delete_btn.clicked.connect(self.delete_note)
        self.delete_btn.setMinimumWidth(100)
        self.delete_btn.setMinimumHeight(45)
        self.delete_btn.setEnabled(False)
        self.delete_btn.setStyleSheet("background-color: #d32f2f;")
        title_layout.addWidget(self.delete_btn)
        
        layout.addLayout(title_layout)
        
        # Note content
        self.note_content = QTextEdit()
        self.note_content.setPlaceholderText("Write your note content here...")
        layout.addWidget(self.note_content, stretch=2)
        
        # Plans section
        plans_label = QLabel("📅 Daily Plans")
        plans_label_font = QFont()
        plans_label_font.setPointSize(12)
        plans_label_font.setBold(True)
        plans_label.setFont(plans_label_font)
        layout.addWidget(plans_label)
        
        # Plans list
        self.plans_widget = QWidget()
        self.plans_layout = QVBoxLayout()
        self.plans_layout.setSpacing(10)
        self.plans_widget.setLayout(self.plans_layout)
        
        scroll = QScrollArea()
        scroll.setWidget(self.plans_widget)
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(200)
        scroll.setMaximumHeight(300)
        layout.addWidget(scroll, stretch=1)
        
        # Add plan button
        self.add_plan_btn = QPushButton("+ Add Plan")
        self.add_plan_btn.clicked.connect(self.add_plan)
        self.add_plan_btn.setEnabled(False)
        layout.addWidget(self.add_plan_btn)
        
        # Placeholder
        self.placeholder = QLabel("← Select a note or create a new one")
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.placeholder.setStyleSheet("color: #888888; font-size: 16px;")
        layout.addWidget(self.placeholder, stretch=3)
        
        panel.setLayout(layout)
        return panel
    
    def load_notes(self):
        """Load all notes from backend."""
        try:
            self.notes = self.client.get_notes()
            self.update_notes_list()
            self.statusBar().showMessage(f"Loaded {len(self.notes)} notes", 3000)
        except APIError as e:
            QMessageBox.critical(self, "Error", f"Failed to load notes: {e.message}")
    
    def update_notes_list(self):
        """Update the notes list widget."""
        self.notes_list.clear()
        
        for note in sorted(self.notes, key=lambda n: n.updated_at, reverse=True):
            item = QListWidgetItem(note.title)
            item.setData(Qt.UserRole, note.id)
            self.notes_list.addItem(item)
    
    def on_note_selected(self, item: QListWidgetItem):
        """Handle note selection."""
        note_id = item.data(Qt.UserRole)
        self.load_note(note_id)
    
    def load_note(self, note_id: int):
        """Load a specific note with plans."""
        try:
            self.current_note = self.client.get_note(note_id)
            self.display_note()
        except APIError as e:
            QMessageBox.critical(self, "Error", f"Failed to load note: {e.message}")
    
    def display_note(self):
        """Display current note in editor."""
        if not self.current_note:
            return
        
        # Hide placeholder
        self.placeholder.hide()
        
        # Show editor controls
        self.note_title.setEnabled(True)
        self.note_content.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)
        self.add_plan_btn.setEnabled(True)
        
        # Set content
        self.note_title.setText(self.current_note.title)
        self.note_content.setText(self.current_note.content)
        
        # Display plans
        self.display_plans()
    
    def display_plans(self):
        """Display plans for current note."""
        # Clear existing plans
        while self.plans_layout.count():
            item = self.plans_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.current_note or not self.current_note.plans:
            no_plans = QLabel("No plans yet. Click 'Add Plan' to create one.")
            no_plans.setStyleSheet("color: #888888; padding: 20px;")
            no_plans.setAlignment(Qt.AlignCenter)
            self.plans_layout.addWidget(no_plans)
            return
        
        # Sort plans by creation date
        sorted_plans = sorted(self.current_note.plans, key=lambda p: p.created_at, reverse=True)
        
        for plan in sorted_plans:
            plan_widget = self.create_plan_widget(plan)
            self.plans_layout.addWidget(plan_widget)
    
    def create_plan_widget(self, plan: Plan) -> QWidget:
        """Create a widget for displaying a plan."""
        widget = QFrame()
        widget.setFrameShape(QFrame.StyledPanel)
        widget.setStyleSheet("background-color: #3c3c3c; border-radius: 4px; padding: 8px;")
        
        layout = QHBoxLayout()
        
        # Checkbox for completion
        checkbox = QCheckBox()
        checkbox.setChecked(plan.is_done)
        checkbox.stateChanged.connect(lambda: self.toggle_plan_completed(plan.id, checkbox.isChecked()))
        layout.addWidget(checkbox)
        
        # Title
        title_label = QLabel(plan.title)
        if plan.is_done:
            title_label.setStyleSheet("text-decoration: line-through; color: #888888;")
        layout.addWidget(title_label, stretch=1)
        
        # Delete button
        delete_btn = QPushButton("🗑️")
        delete_btn.setMaximumWidth(40)
        delete_btn.setStyleSheet("background-color: #d32f2f;")
        delete_btn.clicked.connect(lambda: self.delete_plan(plan.id))
        layout.addWidget(delete_btn)
        
        widget.setLayout(layout)
        return widget
    
    def create_new_note(self):
        """Create a new note."""
        try:
            note = self.client.create_note("Untitled Note", "")
            self.notes.append(note)
            self.update_notes_list()
            self.load_note(note.id)
            self.statusBar().showMessage("New note created", 3000)
            
            # Focus title for editing
            self.note_title.setFocus()
            self.note_title.selectAll()
            
        except APIError as e:
            QMessageBox.critical(self, "Error", f"Failed to create note: {e.message}")
    
    def save_note(self):
        """Save current note."""
        if not self.current_note:
            return
        
        title = self.note_title.text().strip()
        content = self.note_content.toPlainText()
        
        if not title:
            QMessageBox.warning(self, "Validation Error", "Note title cannot be empty")
            return
        
        try:
            updated = self.client.update_note(self.current_note.id, title, content)
            
            # Update in list
            for i, note in enumerate(self.notes):
                if note.id == updated.id:
                    self.notes[i] = updated
                    break
            
            self.update_notes_list()
            self.statusBar().showMessage("Note saved", 3000)
            
        except APIError as e:
            QMessageBox.critical(self, "Error", f"Failed to save note: {e.message}")
    
    def delete_note(self):
        """Delete current note."""
        if not self.current_note:
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{self.current_note.title}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        try:
            self.client.delete_note(self.current_note.id)
            
            # Remove from list
            self.notes = [n for n in self.notes if n.id != self.current_note.id]
            self.update_notes_list()
            
            # Clear editor
            self.current_note = None
            self.note_title.clear()
            self.note_content.clear()
            self.note_title.setEnabled(False)
            self.note_content.setEnabled(False)
            self.save_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
            self.add_plan_btn.setEnabled(False)
            self.placeholder.show()
            
            while self.plans_layout.count():
                item = self.plans_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            self.statusBar().showMessage("Note deleted", 3000)
            
        except APIError as e:
            QMessageBox.critical(self, "Error", f"Failed to delete note: {e.message}")
    
    def add_plan(self):
        """Add a new plan to current note."""
        if not self.current_note:
            return
        
        # Simple dialog for plan creation
        from PySide6.QtWidgets import QDialog, QFormLayout, QDialogButtonBox, QTextEdit as QTextEditDialog
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Plan")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        form = QFormLayout()
        
        title_edit = QTextEditDialog()
        title_edit.setPlaceholderText("Plan title...")
        title_edit.setMaximumHeight(100)
        form.addRow("Title:", title_edit)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.Accepted:
            title = title_edit.toPlainText().strip()
            
            if not title:
                QMessageBox.warning(self, "Validation Error", "Plan title cannot be empty")
                return
            
            try:
                plan = self.client.create_plan(self.current_note.id, title)
                self.current_note.plans.append(plan)
                self.display_plans()
                self.statusBar().showMessage("Plan added", 3000)
                
            except APIError as e:
                QMessageBox.critical(self, "Error", f"Failed to add plan: {e.message}")
    
    def toggle_plan_completed(self, plan_id: int, completed: bool):
        """Toggle plan completion status."""
        if not self.current_note:
            return
        
        try:
            updated_plan = self.client.update_plan(
                self.current_note.id,
                plan_id,
                is_done=completed  # Changed from completed to is_done
            )
            
            # Update in current note
            for i, plan in enumerate(self.current_note.plans):
                if plan.id == plan_id:
                    self.current_note.plans[i] = updated_plan
                    break
            
            self.display_plans()
            self.statusBar().showMessage("Plan updated", 2000)
            
        except APIError as e:
            QMessageBox.critical(self, "Error", f"Failed to update plan: {e.message}")
    
    def delete_plan(self, plan_id: int):
        """Delete a plan."""
        if not self.current_note:
            return
        
        try:
            self.client.delete_plan(self.current_note.id, plan_id)
            
            # Remove from current note
            self.current_note.plans = [p for p in self.current_note.plans if p.id != plan_id]
            self.display_plans()
            self.statusBar().showMessage("Plan deleted", 3000)
            
        except APIError as e:
            QMessageBox.critical(self, "Error", f"Failed to delete plan: {e.message}")
