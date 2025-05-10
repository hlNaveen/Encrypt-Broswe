# Encrypt Browser

A custom tabbed web browser built with Python and the PyQt6 framework, utilizing QtWebEngine for rendering web content. This project demonstrates various browser functionalities including tab management, navigation controls, user-configurable settings, and a security/privacy dialog.

## Features

* **Tabbed Browsing:**
    * Open multiple websites in different tabs.
    * Add new tabs.
    * Close tabs (individual tabs and closing the last tab exits the browser).
    * Tab titles update based on the loaded page.
* **Navigation:**
    * Back, Forward, Reload, Stop, and Home buttons.
    * Address bar for URL input and display.
* **User Interface:**
    * Custom Apple HIG-inspired theme with a light, clean aesthetic.
    * Integrated tab bar appearance at the top of the window.
    * Address bar positioned at the bottom of the window.
    * Splash screen on startup.
* **Settings & Preferences:**
    * **Preferences Dialog:** Allows setting a custom home page.
    * **Security & Privacy Dialog (Shield Icon):**
        * Toggle various content settings for the current tab (JavaScript, Local Storage, Plugins, DNS Prefetching, Hyperlink Auditing, WebGL, XSS Auditor, PDF Viewer, etc.).
        * Option to send a "Do Not Track" (DNT) header (requires Qt 6.2+).
        * Clear all cookies.
        * Clear HTTP cache.
        * Clear all browsing data (cookies, cache, visited links).
* **Developer Tools:**
    * "Inspect Element" button to open Chromium Developer Tools for the current tab, allowing detailed inspection of web content, network requests, console logs, etc.
* **Custom Web Page Handling:**
    * Pop-ups and links designed to open in new windows (`target="_blank"`) are opened in new tabs.
    * Basic permission handling for features like geolocation (prompts user).

## Project Structure

The project is organized into several Python files for better maintainability:

* `main.py`: The main entry point of the application. Handles application setup, splash screen, and instantiates the main browser window.
* `browser_window.py`: Contains the `WebBrowserWindow` class, which defines the main UI, toolbars, tab widget, and core browser logic.
* `web_engine_page.py`: Contains the `CustomWebEnginePage` class, responsible for handling page-specific behaviors like new window creation and feature permissions.
* `dialogs.py`: Contains the `SettingsDialog` (for preferences like home page) and `SecurityDialog` (for security/privacy settings).
* `ui_components.py`: Includes utility functions (e.g., `create_icon_from_svg`) and definitions for all SVG icons used in the UI.
* `constants.py`: Stores global constants, primarily the main QSS `STYLESHEET` for the application.

## Requirements

* Python 3.x (developed with Python 3.10+)
* PyQt6
* PyQt6-WebEngine

## Setup Instructions

1.  **Clone the repository (if applicable) or download all `.py` files into a single directory.**
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```
3.  **Install the required Python packages:**
    ```bash
    pip install PyQt6 PyQt6-WebEngine
    ```

## How to Run

Navigate to the directory containing the project files in your terminal and run:

```bash
python main.py


another version of this project's link down below. 

https://github.com/hlNaveen/webbrowserv2
