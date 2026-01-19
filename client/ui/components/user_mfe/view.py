from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QLineEdit, 
                               QSpinBox, QCheckBox, QLabel, QPushButton, QFormLayout)
from PySide6.QtCore import Signal

class UserSettingsView(QWidget):
    save_clicked = Signal(dict)

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        
        # --- Tab 1: Profile ---
        self.profile_tab = QWidget()
        self.profile_form = QFormLayout()
        
        self.username_input = QLineEdit()
        self.email_input = QLineEdit()
        
        self.profile_form.addRow("Username:", self.username_input)
        self.profile_form.addRow("Email:", self.email_input)
        self.profile_tab.setLayout(self.profile_form)
        
        # --- Tab 2: Preferences ---
        self.prefs_tab = QWidget()
        self.prefs_form = QFormLayout()
        
        self.address_input = QLineEdit()
        
        self.radius_input = QSpinBox()
        self.radius_input.setRange(1, 50)
        self.radius_input.setSuffix(" km")
        
        self.kosher_check = QCheckBox("Show Kosher results only")
        
        self.prefs_form.addRow("Default Address:", self.address_input)
        self.prefs_form.addRow("Search Radius:", self.radius_input)
        self.prefs_form.addRow(self.kosher_check)
        self.prefs_tab.setLayout(self.prefs_form)

        # Assemble Tabs
        self.tabs.addTab(self.profile_tab, "Profile")
        self.tabs.addTab(self.prefs_tab, "Preferences")
        
        # --- Save Button ---
        self.btn_save = QPushButton("Save Changes")
        self.btn_save.clicked.connect(self._on_save)

        self.main_layout.addWidget(self.tabs)
        self.main_layout.addWidget(self.btn_save)
        self.setLayout(self.main_layout)

    def _on_save(self):
        # Gather data into a plain dictionary
        data = {
            "username": self.username_input.text(),
            "email": self.email_input.text(),
            "address": self.address_input.text(),
            "radius": self.radius_input.value(),
            "kosher": self.kosher_check.isChecked()
        }
        self.save_clicked.emit(data)

    def load_data(self, username, email, address, radius, is_kosher):
        """Populate fields cleanly"""
        self.username_input.setText(username)
        self.email_input.setText(email or "")
        self.address_input.setText(address)
        self.radius_input.setValue(radius)
        self.kosher_check.setChecked(is_kosher)
