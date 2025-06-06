# browser_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QLineEdit, QToolBar, QStatusBar,
    QWidget, QSizePolicy, QTabWidget, QTabBar, QMessageBox
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PyQt6.QtCore import QUrl, QSize, Qt
from PyQt6.QtGui import QAction

# Import from our other modules
from constants import STYLESHEET
from ui_components import (
    create_icon_from_svg, BACK_ICON_SVG, FORWARD_ICON_SVG, RELOAD_ICON_SVG,
    HOME_ICON_SVG, STOP_ICON_SVG, SETTINGS_ICON_SVG, NEW_TAB_ICON_SVG,
    SHIELD_ICON_SVG, INSPECT_ICON_SVG 
    # CLOSE_TAB_ICON_SVG is not used here directly, tabs use default close buttons
)
from dialogs import SettingsDialog, SecurityDialog
from web_engine_page import CustomWebEnginePage


class WebBrowserWindow(QMainWindow):
    """Main window for the tabbed web browser."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Browser") 
        self.setGeometry(100, 100, 1024, 768) # Default size
        self.setStyleSheet(STYLESHEET) 

        self.default_url = QUrl("https://www.google.com") 

        self.profile = QWebEngineProfile("SecureUserProfile", self) 


        self.address_bar = QLineEdit() 
        self.address_bar.setObjectName("AddressBar") 
        self.address_bar.setStatusTip("Enter web address and press Enter")
        self.address_bar.returnPressed.connect(self.load_url_from_address_bar)

        self.setup_toolbars() 

        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True) 
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.current_tab_changed)
        
        self.setCentralWidget(self.tab_widget) 
        
        self.add_new_tab(self.default_url) 

        self.setStatusBar(QStatusBar(self))
        self.current_tab_changed(0)

    def create_browser_view(self) -> QWebEngineView:
        """Creates a new QWebEngineView with a CustomWebEnginePage and default settings."""
        browser_view = QWebEngineView()
        page_settings = browser_view.settings() 

        page_settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, False)
        page_settings.setAttribute(QWebEngineSettings.WebAttribute.HyperlinkAuditingEnabled, False)
        page_settings.setAttribute(QWebEngineSettings.WebAttribute.ScreenCaptureEnabled, False) 
        page_settings.setAttribute(QWebEngineSettings.WebAttribute.XSSAuditingEnabled, False) 
        page_settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False) 

        custom_page = CustomWebEnginePage(self.profile, self, browser_view) 
        browser_view.setPage(custom_page)

        browser_view.urlChanged.connect(lambda qurl, bv=browser_view: self.update_url_in_address_bar(qurl, bv))
        browser_view.loadFinished.connect(lambda success, bv=browser_view: self.on_load_finished(success, bv))
        browser_view.loadStarted.connect(lambda bv=browser_view: self.on_load_started(bv))
        browser_view.loadProgress.connect(lambda progress, bv=browser_view: self.on_load_progress(progress, bv))
        browser_view.titleChanged.connect(lambda title, bv=browser_view: self.update_tab_title(title, bv))
        return browser_view

    def add_new_tab(self, url: QUrl = None, make_current: bool = True) -> QWebEngineView:
        """Adds a new tab with a web browser view."""
        if url is None:
            url = self.default_url
        
        browser_view = self.create_browser_view()
        
        idx = self.tab_widget.addTab(browser_view, "New Tab") 
        self.tab_widget.setTabToolTip(idx, "Loading...") 
        
        browser_view.setUrl(url) L

        if make_current:
            self.tab_widget.setCurrentIndex(idx)
        
        self.update_navigation_buttons_state() 
        return browser_view

    def close_tab(self, index: int):
        """Closes the tab at the given index."""
        if index < 0 or index >= self.tab_widget.count(): 
            return

        browser_view_to_close = self.tab_widget.widget(index)
        if isinstance(browser_view_to_close, QWebEngineView):

            try:
                browser_view_to_close.urlChanged.disconnect()
                browser_view_to_close.loadFinished.disconnect()
                browser_view_to_close.loadStarted.disconnect()
                browser_view_to_close.loadProgress.disconnect()
                browser_view_to_close.titleChanged.disconnect()
            except TypeError: 
                pass
            browser_view_to_close.stop() 
            browser_view_to_close.setPage(None)
            browser_view_to_close.deleteLater() 
        
        self.tab_widget.removeTab(index)
        
        if self.tab_widget.count() == 0:

            self.close() 

    def current_tab_changed(self, index: int):
        """Updates UI elements when the current tab changes."""
        browser_view = self.current_browser_view()
        if browser_view:
            self.update_url_in_address_bar(browser_view.url(), browser_view)
            self.update_tab_title(browser_view.title(), browser_view) 

            if browser_view.isLoading():
                self.on_load_started(browser_view)
            else:
                self.on_load_finished(True, browser_view) 
        else:

            self.address_bar.setText("")
            self.setWindowTitle("Web Browser")
            self.statusBar().clearMessage()
        self.update_navigation_buttons_state()


    def current_browser_view(self) -> QWebEngineView | None:
        """Returns the QWebEngineView of the currently active tab."""
        if self.tab_widget.count() > 0:
            current_widget = self.tab_widget.currentWidget()
     
            if isinstance(current_widget, QWebEngineView):
                return current_widget
        return None

    def setup_toolbars(self): 
        """Sets up the top navigation toolbar and the bottom address bar toolbar."""
   
        self.top_toolbar = QToolBar("TopNavigation")
        self.top_toolbar.setObjectName("TopToolBar") 
        self.top_toolbar.setIconSize(QSize(16, 16)) 
        self.top_toolbar.setMovable(False); self.top_toolbar.setFloatable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.top_toolbar) 


        actions_config = [
            (BACK_ICON_SVG, "Back", lambda: self.current_browser_view().back() if self.current_browser_view() else None, "back_button", "Go to previous page"),
            (FORWARD_ICON_SVG, "Forward", lambda: self.current_browser_view().forward() if self.current_browser_view() else None, "forward_button", "Go to next page"),
            (RELOAD_ICON_SVG, "Reload", lambda: self.current_browser_view().reload() if self.current_browser_view() else None, "reload_button", "Reload current page"),
            (STOP_ICON_SVG, "Stop", lambda: self.current_browser_view().stop() if self.current_browser_view() else None, "stop_button", "Stop loading current page", True), 
            (HOME_ICON_SVG, "Home", self.navigate_home, "home_button", f"Go to home page ({self.default_url.toString()})"),
            (NEW_TAB_ICON_SVG, "New Tab", lambda: self.add_new_tab(make_current=True), "new_tab_button", "Open a new tab"),
            (INSPECT_ICON_SVG, "Inspect Element", self.open_inspector, "inspect_button", "Open Developer Tools")
        ]

        for icon_svg, text, callback, attr_name, tooltip, *disabled_state in actions_config:
            action = QAction(create_icon_from_svg(icon_svg), text, self)
            action.setStatusTip(tooltip)
            action.triggered.connect(callback)
            setattr(self, attr_name, action) 
            self.top_toolbar.addAction(action)
            if disabled_state and disabled_state[0]:
                action.setEnabled(False)
        
        
        top_spacer = QWidget()
        top_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.top_toolbar.addWidget(top_spacer) 

        
        self.shield_button = QAction(create_icon_from_svg(SHIELD_ICON_SVG), "Security & Privacy", self)
        self.shield_button.setStatusTip("Open Security & Privacy settings for current tab")
        self.shield_button.triggered.connect(self.open_security_dialog)
        self.top_toolbar.addAction(self.shield_button)

        
        self.settings_button = QAction(create_icon_from_svg(SETTINGS_ICON_SVG), "Preferences", self)
        self.settings_button.setStatusTip("Open browser preferences")
        self.settings_button.triggered.connect(self.open_settings_dialog)
        self.top_toolbar.addAction(self.settings_button)

        
        self.bottom_toolbar = QToolBar("BottomAddressBar")
        self.bottom_toolbar.setObjectName("BottomToolBar") 
        self.bottom_toolbar.setMovable(False); self.bottom_toolbar.setFloatable(False)
        self.bottom_toolbar.addWidget(self.address_bar) 
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.bottom_toolbar) 

    def open_inspector(self):
        """Opens the Web Inspector (Developer Tools) for the current tab."""
        current_view = self.current_browser_view()
        if current_view and current_view.page():
           
            current_view.page().triggerAction(QWebEnginePage.WebAction.InspectElement)
        else: 
            self.statusBar().showMessage("No active page to inspect.", 3000)

    def open_settings_dialog(self):
        """Opens the general preferences dialog."""
        dialog = SettingsDialog(self.default_url.toString(), self)
        if dialog.exec(): 
            new_home_page_str = dialog.get_home_page()
            if new_home_page_str:
                
                if not (new_home_page_str.startswith("http://") or new_home_page_str.startswith("https://")):
                    new_home_page_str = "https://" + new_home_page_str
                
                self.default_url = QUrl(new_home_page_str)
                
                if hasattr(self, 'home_button'):
                    self.home_button.setStatusTip(f"Go to home page ({self.default_url.toString()})")
                print(f"Default Home page updated to: {self.default_url.toString()}")
            else:
                 QMessageBox.warning(self, "Settings Error", "Home page URL cannot be empty.")


    def open_security_dialog(self):
        """Opens the security and privacy settings dialog for the current tab."""
        current_view = self.current_browser_view()
        if current_view:
            dialog = SecurityDialog(current_view, self.profile, self)
            dialog.exec() 
        else: 
            self.statusBar().showMessage("No active tab for security settings.", 3000)

    def navigate_home(self):
        """Navigates the current tab to the default home page."""
        if current_view := self.current_browser_view(): 
            current_view.setUrl(self.default_url)

    def load_url_from_address_bar(self):
        """Loads the URL entered in the address bar into the current tab."""
        if current_view := self.current_browser_view():
            url_text = self.address_bar.text()
            if not (url_text.startswith(("http://", "https://", "file://")) or "://" in url_text):
                url_text = "https://" + url_text 
            current_view.setUrl(QUrl(url_text))

    def update_url_in_address_bar(self, q_url: QUrl, sender_view: QWebEngineView):
        """Updates the address bar if the URL change is from the current tab."""
        if self.current_browser_view() == sender_view:
            self.address_bar.setText(q_url.toString())
            self.address_bar.setCursorPosition(0) 

    def update_tab_title(self, title: str, sender_view: QWebEngineView):
        """Updates the tab text and main window title if the sender is the current tab."""
        idx = self.tab_widget.indexOf(sender_view)
        if idx != -1: 
            host = sender_view.url().host()
            tab_display_title = title if title else host if host else "Loading..."
            if len(tab_display_title) > 20: 
                tab_display_title = tab_display_title[:17] + "..."
            self.tab_widget.setTabText(idx, tab_display_title)
            self.tab_widget.setTabToolTip(idx, title if title else sender_view.url().toString()) 

        if self.current_browser_view() == sender_view:
            
            main_title = title if title else sender_view.url().host()
            if main_title and len(main_title) < 60: 
                self.setWindowTitle(f"{main_title}")
            elif sender_view.url().host():
                 self.setWindowTitle(sender_view.url().host())
            else:
                self.setWindowTitle("Web Browser")

    def on_load_started(self, sender_view: QWebEngineView):
        """Handles actions when a page starts loading in a tab."""
        if self.current_browser_view() == sender_view:
            self.statusBar().showMessage("Loading...")
            if hasattr(self, 'stop_button'): self.stop_button.setEnabled(True)
            
            idx = self.tab_widget.indexOf(sender_view)
            if idx != -1: 
                 current_tab_text = self.tab_widget.tabText(idx)
         
                 if not sender_view.title() and current_tab_text != "Loading...":
                    self.tab_widget.setTabText(idx, "Loading...")


    def on_load_progress(self, progress: int, sender_view: QWebEngineView):
        """Handles page load progress updates for the current tab."""
        if self.current_browser_view() == sender_view:
            self.statusBar().showMessage(f"Loading... {progress}%")

    def on_load_finished(self, success: bool, sender_view: QWebEngineView):
        """Handles actions when a page finishes loading in a tab."""
      
        if self.tab_widget.indexOf(sender_view) != -1 : 
            if self.current_browser_view() == sender_view or self.tab_widget.currentWidget() is None :
                if hasattr(self, 'stop_button'): self.stop_button.setEnabled(False)
                if success:
                    self.statusBar().showMessage("Load Complete", 3000)
                else:
                    current_url = sender_view.url().toString()
                    self.statusBar().showMessage(f"Failed to load: {current_url.split('?')[0]}", 5000) 
           
            self.update_tab_title(sender_view.title(), sender_view) 
        self.update_navigation_buttons_state() 


    def update_navigation_buttons_state(self):
        """Updates the enabled state of back and forward buttons based on current tab's history."""
        current_view = self.current_browser_view()
        if current_view and current_view.history():
            if hasattr(self, 'back_button'): self.back_button.setEnabled(current_view.history().canGoBack())
            if hasattr(self, 'forward_button'): self.forward_button.setEnabled(current_view.history().canGoForward())
        else:
            if hasattr(self, 'back_button'): self.back_button.setEnabled(False)
            if hasattr(self, 'forward_button'): self.forward_button.setEnabled(False)
        

        if not current_view or (current_view and not current_view.isLoading()):
             if hasattr(self, 'stop_button'): self.stop_button.setEnabled(False)

