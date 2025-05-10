from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PyQt6.QtWidgets import QMessageBox 
from PyQt6.QtCore import QUrl, Qt 


if False: 
    from browser_window import WebBrowserWindow


class CustomWebEnginePage(QWebEnginePage):
    """
    Custom QWebEnginePage to handle new window requests (e.g., target="_blank")
    and feature permissions.
    """

    def __init__(self, profile: QWebEngineProfile, main_window_ref: 'WebBrowserWindow', browser_view_parent: 'QWebEngineView'): # type: ignore
        super().__init__(profile, browser_view_parent)
        self.main_window_ref = main_window_ref 
        self.featurePermissionRequested.connect(self.handle_feature_permission)
        self.setBackgroundColor(Qt.GlobalColor.white) 

    def createWindow(self, _type: QWebEnginePage.WebWindowType) -> QWebEnginePage | None:
        """
        Handles requests from web content to create a new window.
        (e.g., target="_blank" links or window.open()).
        This implementation creates a new tab in the main browser window.
        """
  
        if _type in [QWebEnginePage.WebWindowType.WebBrowserTab, 
                       QWebEnginePage.WebWindowType.WebBrowserWindow, 
                       QWebEnginePage.WebWindowType.WebDialog]: 
            
 
            new_view = self.main_window_ref.add_new_tab(make_current=True) 
            return new_view.page() # Return the QWebEnginePage of the new tab
        
   
        return None 

    def handle_feature_permission(self, url: QUrl, feature: QWebEnginePage.Feature):
        """
        Handles requests from web pages for specific features like geolocation, media access, etc.
        """
        permission_policy = QWebEnginePage.PermissionPolicy.PermissionDeniedByUser # Default to deny
        feature_name = feature.name if hasattr(feature, 'name') else str(feature) 
        

        if feature in [QWebEnginePage.Feature.MouseLock, QWebEnginePage.Feature.FullScreen]:
            permission_policy = QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
            print(f"Auto-granting permission for {feature_name} to {url.host()}")
        elif feature == QWebEnginePage.Feature.Geolocation:

            reply = QMessageBox.question(self.view().window(), "Location Permission",
                                         f"Allow {url.host()} to access your location?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                permission_policy = QWebEnginePage.PermissionPolicy.PermissionGrantedByUser

        
        self.setFeaturePermission(url, feature, permission_policy)
