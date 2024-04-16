import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLineEdit, QToolBar, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QCheckBox, QFileDialog
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://www.google.com'))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        self.setupNavigationBar()
        self.profile = QWebEngineProfile.defaultProfile()

        # Connect downloadRequested signal to custom slot
        self.browser.page().profile().downloadRequested.connect(self.downloadRequested)

    def setupNavigationBar(self):
        navbar = QToolBar('Navigation')
        navbar.setIconSize(QSize(16, 16))
        self.addToolBar(navbar)

        actions = [
            ("Back", self.browser.back),
            ("Forward", self.browser.forward),
            ("Reload", self.browser.reload),
            ("Settings", self.openSettings)
        ]

        for text, action in actions:
            btn = QAction(text, self)
            btn.triggered.connect(action)
            navbar.addAction(btn)

        self.urlBar = QLineEdit()
        self.urlBar.returnPressed.connect(self.navigate)
        navbar.addWidget(self.urlBar)
        self.browser.urlChanged.connect(self.updateUrl)

    def navigate(self):
        url = self.urlBar.text()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        self.browser.setUrl(QUrl(url))

    def updateUrl(self, q):
        self.urlBar.setText(q.toString())

    def openSettings(self):
        dialog = SettingsDialog(self.profile, self)
        dialog.exec_()

    def downloadRequested(self, download):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)", options=options)
        if fileName:
            download.setPath(fileName)
            download.accept()

class SettingsDialog(QDialog):
    def __init__(self, profile, parent=None):
        super().__init__(parent)
        self.profile = profile
        self.setWindowTitle('Settings')
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)

        homepageLabel = QLabel('Homepage URL:')
        self.homepageEdit = QLineEdit()
        self.homepageEdit.setText(self.profile.httpUserAgent())
        layout.addWidget(homepageLabel)
        layout.addWidget(self.homepageEdit)

        clearDataLabel = QLabel('Clear Browsing Data:')
        self.historyCheckbox = QCheckBox('History')
        self.cookiesCheckbox = QCheckBox('Cookies')
        self.cacheCheckbox = QCheckBox('Cache')
        layout.addWidget(clearDataLabel)
        layout.addWidget(self.historyCheckbox)
        layout.addWidget(self.cookiesCheckbox)
        layout.addWidget(self.cacheCheckbox)

        saveButton = QPushButton('Save')
        saveButton.clicked.connect(self.saveSettings)
        closeButton = QPushButton('Close')
        closeButton.clicked.connect(self.close)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(saveButton)
        buttonsLayout.addWidget(closeButton)
        layout.addLayout(buttonsLayout)

        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
            }
            QLineEdit, QCheckBox {
                background-color: #fff;
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def saveSettings(self):
        homepageUrl = self.homepageEdit.text()
        self.profile.setHttpUserAgent(homepageUrl)

        if self.historyCheckbox.isChecked():
            self.profile.clearHistory()
        if self.cookiesCheckbox.isChecked():
            self.profile.cookieStore().deleteAllCookies()
        if self.cacheCheckbox.isChecked():
            self.profile.clearHttpCache()

        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setApplicationName('My Browser')
    window = Browser()
    sys.exit(app.exec_())
