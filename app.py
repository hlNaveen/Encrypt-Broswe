import sys
import os
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QColor, QFont, QPainter, QFontMetrics, QIcon # Added QIcon for app icon

# Import the main window class from our new module
from browser_window import WebBrowserWindow
from ui_components import APP_ICON_SVG # For application icon

def main():
    """Main function to set up and run the browser application."""

    # --- Environment and Application Attribute Setup ---
    # These should be set BEFORE QApplication is instantiated.
    # Attempt to force software rendering for ANGLE (used by Qt on Windows for OpenGL)
    os.environ["QT_ANGLE_PLATFORM"] = "warp" 
    # Fallback to disable GPU for QtWebEngine's underlying Chromium if issues persist
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu" 
    # For better rendering on some systems, especially with software rendering
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseSoftwareOpenGL, True)

    app = QApplication(sys.argv)
    app.setApplicationName("Python Web Browser")
    app.setOrganizationName("GeminiCodeLabs")
    
    # Set Application Icon
    # Create a QIcon from SVG content (assuming create_icon_from_svg is in ui_components)
    # For the app icon, it's better to use a QPixmap directly if create_icon_from_svg is not yet available
    # or ensure ui_components is imported correctly.
    # For simplicity, we'll assume APP_ICON_SVG is defined and create_icon_from_svg handles it.
    # If create_icon_from_svg is in ui_components, it needs to be imported.
    # Let's create a simple one here for the app icon for now.
    try:
        from ui_components import create_icon_from_svg # Assuming it's there
        app_icon = create_icon_from_svg(APP_ICON_SVG, size=64) # Larger size for app icon
        app.setWindowIcon(app_icon)
    except ImportError:
        print("Warning: ui_components or create_icon_from_svg not found for app icon.")
    except Exception as e:
        print(f"Error setting application icon: {e}")


    # --- Splash Screen Creation ---
    primary_screen = app.primaryScreen()
    if primary_screen:
        screen_geometry = primary_screen.geometry()
        splash_width = min(500, screen_geometry.width() - 100) # Adjusted size
        splash_height = min(300, screen_geometry.height() - 100)
    else: 
        splash_width = 500
        splash_height = 300

    splash_pixmap = QPixmap(splash_width, splash_height)
    splash_pixmap.fill(QColor("#e8f0fe")) 

    painter = QPainter(splash_pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(QColor("#005ecb"))

    main_font = QFont("Arial", 20, QFont.Weight.Bold) # Adjusted font size
    painter.setFont(main_font)
    main_text = "Python Browser"
    font_metrics_main = QFontMetrics(main_font)
    
    # Calculate bounding rect for the main text to center it properly
    # Using QRect for text drawing to handle alignment better
    main_text_bounding_rect = font_metrics_main.boundingRect(QRect(0,0,splash_width - 20, splash_height // 2), Qt.AlignmentFlag.AlignCenter, main_text)
    
    subtitle_font = QFont("Arial", 12, QFont.Weight.Normal) # Adjusted font size
    painter.setFont(subtitle_font)
    subtitle_text = "Initializing, please wait..."
    font_metrics_sub = QFontMetrics(subtitle_font)
    subtitle_bounding_rect = font_metrics_sub.boundingRect(QRect(0,0,splash_width - 20, splash_height // 2), Qt.AlignmentFlag.AlignCenter, subtitle_text)

    total_text_height = main_text_bounding_rect.height() + subtitle_bounding_rect.height() + 15 # 15px spacing
    
    main_text_y_offset = (splash_height - total_text_height) // 2
    
    painter.setFont(main_font) # Reset for main text
    main_text_draw_rect = QRect( (splash_width - main_text_bounding_rect.width()) // 2 , 
                                 main_text_y_offset, 
                                 main_text_bounding_rect.width(), 
                                 main_text_bounding_rect.height() )
    painter.drawText(main_text_draw_rect, Qt.AlignmentFlag.AlignCenter, main_text)
    
    subtitle_y_offset = main_text_y_offset + main_text_bounding_rect.height() + 15
    painter.setFont(subtitle_font) # Reset for subtitle
    subtitle_draw_rect = QRect( (splash_width - subtitle_bounding_rect.width()) // 2,
                                subtitle_y_offset,
                                subtitle_bounding_rect.width(),
                                subtitle_bounding_rect.height())
    painter.drawText(subtitle_draw_rect, Qt.AlignmentFlag.AlignCenter, subtitle_text)
    painter.end()

    splash = QSplashScreen(splash_pixmap)
    splash.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    splash.show()
    app.processEvents() 
    
    # --- Main Window Creation and Startup ---
    main_window = WebBrowserWindow() 

    # Use QTimer for a controlled delay before showing the main window
    # This makes the splash screen visible for a minimum duration
    SPLASH_DURATION_MS = 2500 # 2.5 seconds
    QTimer.singleShot(SPLASH_DURATION_MS, lambda: (main_window.show(), splash.finish(main_window)))

    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("Browser closed by user (KeyboardInterrupt).")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred in main: {e}")
        import traceback
        traceback.print_exc() 
        sys.exit(1)

if __name__ == "__main__":
    main()
