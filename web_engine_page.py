# web_engine_page.py
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PyQt6.QtWidgets import QMessageBox # For permission dialogs
from PyQt6.QtCore import QUrl, Qt # Added Qt for GlobalColor

# Forward declaration for type hinting if WebBrowserWindow is in another file
if False: # This block is not executed, for type hinting only
    from browser_window import WebBrowserWindow


class CustomWebEnginePage(QWebEnginePage):
    """
    Custom QWebEnginePage to handle new window requests (e.g., target="_blank")
    and feature permissions.
    """
    # Added browser_view_parent to __init__ to avoid issues with self.view() being None initially
    # when the page is created before being set on a view.
    def __init__(self, profile: QWebEngineProfile, main_window_ref: 'WebBrowserWindow', browser_view_parent: 'QWebEngineView'): # type: ignore
        super().__init__(profile, browser_view_parent) # Parent is the QWebEngineView hosting this page
        self.main_window_ref = main_window_ref # Reference to the main WebBrowserWindow
        self.featurePermissionRequested.connect(self.handle_feature_permission)
        self.setBackgroundColor(Qt.GlobalColor.white) # Ensure new pages have a white background

    def createWindow(self, _type: QWebEnginePage.WebWindowType) -> QWebEnginePage | None:
        """
        Handles requests from web content to create a new window.
        (e.g., target="_blank" links or window.open()).
        This implementation creates a new tab in the main browser window.
        """
        # For pop-ups or target="_blank", open in a new tab in our main window
        if _type in [QWebEnginePage.WebWindowType.WebBrowserTab, 
                       QWebEnginePage.WebWindowType.WebBrowserWindow, 
                       QWebEnginePage.WebWindowType.WebDialog]: # Treat dialogs as tabs too for simplicity
            
            # Call the add_new_tab method of the main window instance
            new_view = self.main_window_ref.add_new_tab(make_current=True) # Add and switch to new tab
            return new_view.page() # Return the QWebEnginePage of the new tab
        
        # For other types, or if no main window reference, block by returning None
        return None 

    def handle_feature_permission(self, url: QUrl, feature: QWebEnginePage.Feature):
        """
        Handles requests from web pages for specific features like geolocation, media access, etc.
        """
        permission_policy = QWebEnginePage.PermissionPolicy.PermissionDeniedByUser # Default to deny
        feature_name = feature.name if hasattr(feature, 'name') else str(feature) # Get feature name as string
        
        # Example: Auto-grant some less sensitive features
        if feature in [QWebEnginePage.Feature.MouseLock, QWebEnginePage.Feature.FullScreen]:
            permission_policy = QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
            print(f"Auto-granting permission for {feature_name} to {url.host()}")
        elif feature == QWebEnginePage.Feature.Geolocation:
            # For sensitive permissions, prompt the user
            reply = QMessageBox.question(self.view().window(), "Location Permission", # Use self.view().window() to get parent QMainWindow
                                         f"Allow {url.host()} to access your location?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                permission_policy = QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
        # Add more specific permission handling for other features as needed (e.g., MediaAudioCapture, MediaVideoCapture)
        # else:
        #     print(f"Permission for {feature_name} by {url.host()} - currently auto-denied (would prompt).")
        
        self.setFeaturePermission(url, feature, permission_policy)
