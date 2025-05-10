# dialogs.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QDialogButtonBox,
    QLineEdit, QCheckBox, QMessageBox, QGroupBox
)
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings, QWebEnginePage
from PyQt6.QtCore import Qt

class SettingsDialog(QDialog): # For general browser preferences
    """Dialog for general browser preferences like home page."""
    def __init__(self, current_home_page: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preferences")
        self.setMinimumWidth(380)


        layout = QVBoxLayout(self)
        
        home_page_group = QGroupBox("General")
        home_page_layout = QVBoxLayout(home_page_group)
        home_page_label = QLabel("Home Page URL:")
        home_page_layout.addWidget(home_page_label)
        self.home_page_input = QLineEdit(current_home_page)
        self.home_page_input.setPlaceholderText("Enter URL (e.g., https://www.example.com)")
        home_page_layout.addWidget(self.home_page_input)
        layout.addWidget(home_page_group)

        layout.addStretch(1) # Push buttons to the bottom

        # Standard OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        if ok_button: # Ensure the button exists
            ok_button.setDefault(True)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def get_home_page(self) -> str:
        """Returns the entered home page URL."""
        return self.home_page_input.text().strip()

class SecurityDialog(QDialog): # For security and privacy settings
    """Dialog for managing security and privacy settings."""
    def __init__(self, browser_view: QWebEngineView, profile: QWebEngineProfile, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Security & Privacy")
        self.setMinimumWidth(480) 
        # self.setStyleSheet(parent.styleSheet() if parent else "") # Inherit main window style

        self.browser_view = browser_view
        self.profile = profile
        # Get page settings if a valid page exists in the view
        self.page_settings = None
        if self.browser_view and self.browser_view.page():
            self.page_settings = self.browser_view.page().settings()

        main_layout = QVBoxLayout(self)

        # --- Content Settings Group ---
        content_group = QGroupBox("Content Settings (Current Tab)")
        content_layout = QVBoxLayout(content_group)
        
        info_label = QLabel("Note: Some settings may require a page reload to take full effect.")
        info_label.setObjectName("InfoLabel") 
        content_layout.addWidget(info_label)

        self.checkboxes = {} 

        if self.page_settings:
  
            settings_map = {
                QWebEngineSettings.WebAttribute.JavascriptEnabled: ("Enable JavaScript", True, "Allows websites to run scripts."),
                QWebEngineSettings.WebAttribute.LocalStorageEnabled: ("Enable Local Storage", True, "Allows websites to store data locally."),
                QWebEngineSettings.WebAttribute.PluginsEnabled: ("Enable Plugins (e.g., PDF viewer)", True, "Allows browser plugins to run."),
                QWebEngineSettings.WebAttribute.DnsPrefetchEnabled: ("Enable DNS Prefetching", False, "May improve page load times but can reveal browsing habits to DNS servers."),
                QWebEngineSettings.WebAttribute.HyperlinkAuditingEnabled: ("Enable Hyperlink Auditing (<a ping>)", False, "Allows sites to track clicks on links."),
                QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled: ("Enable Smooth Scrolling", True, "Enables smooth scrolling animations."),
                QWebEngineSettings.WebAttribute.ErrorPageEnabled: ("Show Custom Error Pages", True, "Shows browser-specific error pages instead of server errors."),
                QWebEngineSettings.WebAttribute.FullScreenSupportEnabled: ("Allow Fullscreen Requests", True, "Allows sites to request fullscreen mode."),
                QWebEngineSettings.WebAttribute.ScreenCaptureEnabled: ("Allow Screen Capture", False, "Allows sites to capture screen content (use with caution)."),
                QWebEngineSettings.WebAttribute.WebGLEnabled: ("Enable WebGL", False, "Allows 3D graphics. Disabling can reduce fingerprinting and resource usage."), 
                QWebEngineSettings.WebAttribute.XSSAuditingEnabled: ("Enable XSS Auditor (if available)", False, "Attempt to prevent cross-site scripting attacks (effectiveness varies, often deprecated)."),
                QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls: ("Allow Local Files to Access Remote Content", False, "Security risk: Local files (file://) accessing internet resources."),
                QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls: ("Allow Local Files to Access Other Local Files", False, "Security risk: Local files accessing other local files via file:// URLs."),
                QWebEngineSettings.WebAttribute.PdfViewerEnabled: ("Enable Built-in PDF Viewer", True, "Uses the browser's internal PDF viewer.")
            }

            for attr, (text, default_checked, *tooltip_parts) in settings_map.items():
                checkbox = QCheckBox(text)
                current_value = self.page_settings.testAttribute(attr)
                checkbox.setChecked(current_value if isinstance(current_value, bool) else default_checked)
                
                if tooltip_parts: checkbox.setToolTip(tooltip_parts[0])
                self.checkboxes[attr] = checkbox 
                content_layout.addWidget(checkbox)
        else:
            content_layout.addWidget(QLabel("No active page to configure content settings for."))
        main_layout.addWidget(content_group)

        # --- Profile Settings Group ---
        profile_group = QGroupBox("Browser Profile Settings (Global)")
        profile_layout = QVBoxLayout(profile_group)

        self.dnt_checkbox = QCheckBox("Send 'Do Not Track' (DNT) Header")
        
        self.has_set_http_header = hasattr(self.profile, 'setHttpHeader') # Check if method exists
        if not self.has_set_http_header:
            self.dnt_checkbox.setEnabled(False)
            self.dnt_checkbox.setToolTip("This feature (DNT header modification) requires Qt 6.2 or newer.")
        else:
            self.dnt_checkbox.setToolTip("Asks websites not to track you. Compliance is voluntary.")
            # We cannot reliably get the current DNT header value. Assume off unless user checks it.
            self.dnt_checkbox.setChecked(False) 

        profile_layout.addWidget(self.dnt_checkbox)
        main_layout.addWidget(profile_group)

        # --- Privacy Actions Group ---
        actions_group = QGroupBox("Privacy Actions (Browser-wide)")
        actions_layout = QVBoxLayout(actions_group)

        clear_cookies_button = QPushButton("Clear All Cookies")
        clear_cookies_button.setObjectName("ClearDataButton")
        clear_cookies_button.setToolTip("Deletes all cookies stored by the browser.")
        clear_cookies_button.clicked.connect(self.clear_all_cookies)
        actions_layout.addWidget(clear_cookies_button)
        
        clear_cache_button = QPushButton("Clear HTTP Cache")
        clear_cache_button.setObjectName("ClearDataButton")
        clear_cache_button.setToolTip("Deletes cached web content like images and scripts.")
        clear_cache_button.clicked.connect(self.clear_http_cache)
        actions_layout.addWidget(clear_cache_button)

        clear_all_data_button = QPushButton("Clear All Browsing Data")
        clear_all_data_button.setObjectName("ClearDataButton")
        clear_all_data_button.setToolTip("Clears cookies, cache, visited links, and other browsing data.")
        clear_all_data_button.clicked.connect(self.clear_all_browsing_data)
        actions_layout.addWidget(clear_all_data_button)
        
        main_layout.addWidget(actions_group)
        main_layout.addStretch(1) 

        # --- Dialog Buttons ---
        button_box = QDialogButtonBox()
        apply_button = button_box.addButton("Apply & Close", QDialogButtonBox.ButtonRole.AcceptRole)
        close_button = button_box.addButton("Close", QDialogButtonBox.ButtonRole.RejectRole)
        
        apply_button.setDefault(True)
        button_box.accepted.connect(self.apply_all_settings) 
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

    def apply_all_settings(self):
        settings_changed_count = 0
        if self.page_settings:
            for attr, checkbox in self.checkboxes.items():
                current_val = self.page_settings.testAttribute(attr) 
                new_val = checkbox.isChecked()
                if current_val != new_val: 
                    self.page_settings.setAttribute(attr, new_val)
                    settings_changed_count +=1
        
        if self.has_set_http_header and self.dnt_checkbox.isEnabled():

            if self.dnt_checkbox.isChecked():
                self.profile.setHttpHeader(b"DNT", b"1") 
                print("DNT header set to 1 for the profile.")
            else:

                self.profile.setHttpHeader(b"DNT", b"0") 
                print("DNT header set to 0 for the profile.")
            settings_changed_count +=1 # Count DNT change as a setting change

        if settings_changed_count > 0:
            QMessageBox.information(self, "Settings Applied", 
                                   f"{settings_changed_count} setting(s) have been applied.\nSome content settings may require a page reload to take full effect.")
        else:
            QMessageBox.information(self, "Settings", "No settings were changed.")
        self.accept() 

    def clear_all_cookies(self):
        reply = QMessageBox.question(self, "Confirm Clear Cookies",
                                     "Are you sure you want to delete all cookies?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if self.profile:
                self.profile.cookieStore().deleteAllCookies()
                QMessageBox.information(self, "Cookies Cleared", "All cookies have been cleared.")

    def clear_http_cache(self):
        reply = QMessageBox.question(self, "Confirm Clear Cache",
                                     "Are you sure you want to clear the HTTP cache?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if self.profile:
                self.profile.clearHttpCache()
                QMessageBox.information(self, "Cache Cleared", "HTTP cache has been cleared.")
            
    def clear_all_browsing_data(self):
        reply = QMessageBox.question(self, "Confirm Clear All Browsing Data",
                                     "This will clear cookies, HTTP cache, and visited links history. This action cannot be undone. Are you sure?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if self.profile:
                self.profile.clearAllVisitedLinks() 
                self.profile.clearHttpCache()
                self.profile.cookieStore().deleteAllCookies()
                QMessageBox.information(self, "Browsing Data Cleared", 
                                        "Cookies, HTTP cache, and visited links history have been cleared.")

