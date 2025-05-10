
STYLESHEET = """
QMainWindow { 
    background-color: #e8e8e8; /* Unified header color for the entire window background */
}

QToolBar#TopToolBar {
    background-color: #e8e8e8; /* Match QMainWindow for unified header */
    border: none; 
    padding: 2px 5px 0px 5px; /* No bottom padding, to merge with QTabBar */
    spacing: 3px; 
    min-height: 26px; 
}

QTabWidget {
    border: none; /* Remove QTabWidget's own border */
    background-color: transparent; /* Make QTabWidget itself transparent */
}

QTabWidget::pane { 
    border-top: 1px solid #b0b0b0; /* Separator line below the unified header (tabs) */
    background-color: #f6f6f6; /* Main content background */
}

QTabBar { 
    background-color: #e8e8e8; /* Match TopToolBar and QMainWindow */
    border: none; /* No border for QTabBar itself */
    qproperty-drawBase: 0; 
    margin: 0px; 
    padding: 0px 5px 0px 5px; /* No bottom padding for QTabBar */
}

QTabBar::tab {
    background-color: #dcdcdc; 
    color: #4c4c4c;
    border: 1px solid #c0c0c0; 
    border-bottom: none; /* Non-selected tabs don't have a distinct bottom border here */
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    padding: 5px 10px; 
    margin-right: 1px; 
    margin-left: 1px;
    margin-top: 3px; /* Creates a small space above non-selected tabs */
    min-width: 80px; 
    max-width: 160px; 
    font-size: 12px;
}

QTabBar::tab:selected {
    background-color: #f6f6f6; /* Match pane background */
    color: #2c2c2c; 
    border-top: 1px solid #b0b0b0; /* Match pane's top border color */
    border-left: 1px solid #b0b0b0;
    border-right: 1px solid #b0b0b0;
    border-bottom-color: #f6f6f6; /* Make bottom border same as pane to "connect" */
    margin-top: 0px; /* Selected tab is flush with the top of QTabBar area */
    margin-bottom: -1px; /* Crucial: Pulls selected tab down to cover QTabBar's bottom border line */
    padding-top: 6px; 
    padding-bottom: 6px; 
}

QTabBar::tab:hover:!selected {
    background-color: #d0d0d0;
}

QTabBar::tab:first { margin-left: 0; }
QTabBar::tab:last { margin-right: 0; }
QTabBar::tab:only-one { margin: 0; }

QTabBar::close-button { 
    margin: 2px; padding: 1px; border-radius: 3px; 
}
QTabBar::close-button:hover { background-color: #c0c0c0; }


/* Bottom Toolbar and Address Bar */
QToolBar#BottomToolBar { 
    background-color: #f0f0f0; border-top: 1px solid #d0d0d0; 
    padding: 3px 8px; spacing: 6px; min-height: 28px; 
}
QLineEdit#AddressBar {
    background-color: #ffffff; color: #222222; border: 1px solid #c6c6c6; 
    border-radius: 6px; padding: 4px 10px; font-size: 13px; min-height: 22px; 
}
QLineEdit#AddressBar:focus { border: 1px solid #007aff; }

/* Status Bar */
QStatusBar {
    background-color: #f0f0f0; color: #4c4c4c; font-size: 11px; 
    padding: 2px 0px; border-top: 1px solid #d0d0d0; min-height: 18px; 
}
QStatusBar::item { border: none; }

/* Web View */
QWebEngineView { border: none; background-color: #ffffff; }


/* Dialog Styling (remains largely the same) */
QDialog { background-color: #f6f6f6; border: 1px solid #c0c0c0; }
QDialog QLabel { font-size: 13px; color: #333333; margin-bottom: 3px;}
QDialog QLabel#DialogSectionLabel { font-weight: bold; margin-top: 10px; margin-bottom: 6px; }
QDialog QLabel#InfoLabel { font-size: 11px; color: #555555; margin-top: 2px; margin-bottom: 8px; font-style: italic; }
QDialog QGroupBox { 
    font-size: 13px; font-weight: bold; color: #333333; 
    border: 1px solid #c6c6c6; border-radius: 5px; 
    margin-top: 10px; padding: 10px 5px 5px 5px;
}
QDialog QGroupBox::title {
    subcontrol-origin: margin; subcontrol-position: top left;
    padding: 0 3px; left: 7px; 
}
QDialog QLineEdit {
    background-color: #ffffff; color: #222222; border: 1px solid #c6c6c6;
    border-radius: 5px; padding: 6px 8px; font-size: 13px; min-height: 26px;
}
QDialog QLineEdit:focus { border: 1px solid #007aff; }
QDialog QCheckBox { 
    font-size: 13px; color: #333333; spacing: 5px; 
    margin-top: 4px; margin-bottom: 4px; padding-left: 3px;
}
QDialog QCheckBox::indicator { width: 15px; height: 15px; }
QDialog QCheckBox::indicator:unchecked {
    border: 1px solid #999999; border-radius: 3px; background-color: white;
}
QDialog QCheckBox::indicator:checked {
    background-color: #007aff; border: 1px solid #007aff; border-radius: 3px;
}
QDialog QCheckBox::indicator:disabled {
    border: 1px solid #c0c0c0; background-color: #e0e0e0;
}
QDialog QPushButton {
    background-color: #ffffff; border: 1px solid #c6c6c6; border-radius: 5px;
    padding: 6px 12px; font-size: 13px; color: #333333; min-height: 26px;
}
QDialog QPushButton:hover { background-color: #f0f0f0; }
QDialog QPushButton:pressed { background-color: #e0e0e0; }
QDialog QPushButton#ClearDataButton { 
    background-color: #ffebee; border-color: #ffcdd2;
}
QDialog QPushButton#ClearDataButton:hover { background-color: #ffcdd2; }
QDialog QPushButton:default {
    background-color: #007aff; color: white; border: 1px solid #007aff;
}
QDialog QPushButton:default:hover { background-color: #005ecb; }

/* Splash Screen Styling */
QSplashScreen {
    border: 2px solid #007aff; background-color: #e8f0fe; 
}
QSplashScreen QLabel { color: #005ecb; font-size: 20px; padding: 10px; }
"""
