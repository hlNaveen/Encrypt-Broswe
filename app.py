import sys
import os
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QColor, QFont, QPainter, QFontMetrics, QIcon


from browser_window import WebBrowserWindow
from ui_components import APP_ICON_SVG 

def main():
    """Main function to set up and run the browser application."""

    # Environment and Application Attribute Setup

    os.environ["QT_ANGLE_PLATFORM"] = "warp" 

    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu" 

    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseSoftwareOpenGL, True)

    app = QApplication(sys.argv)
    app.setApplicationName("Encrypt Browser")
    app.setOrganizationName("NaviCodeLabs")
    
    try:
        from ui_components import create_icon_from_svg 
        app_icon = create_icon_from_svg(APP_ICON_SVG, size=64) 
        app.setWindowIcon(app_icon)
    except ImportError:
        print("Warning: ui_components or create_icon_from_svg not found for app icon.")
    except Exception as e:
        print(f"Error setting application icon: {e}")


    # Splash Screen Creation
    primary_screen = app.primaryScreen()
    if primary_screen:
        screen_geometry = primary_screen.geometry()
        splash_width = min(500, screen_geometry.width() - 100) 
        splash_height = min(300, screen_geometry.height() - 100)
    else: 
        splash_width = 500
        splash_height = 300

    splash_pixmap = QPixmap(splash_width, splash_height)
    splash_pixmap.fill(QColor("#e8f0fe")) 

    painter = QPainter(splash_pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(QColor("#005ecb"))

    main_font = QFont("Arial", 20, QFont.Weight.Bold) 
    painter.setFont(main_font)
    main_text = "Encrypt Browser"
    font_metrics_main = QFontMetrics(main_font)
    
    
    main_text_bounding_rect = font_metrics_main.boundingRect(QRect(0,0,splash_width - 20, splash_height // 2), Qt.AlignmentFlag.AlignCenter, main_text)
    
    subtitle_font = QFont("Arial", 12, QFont.Weight.Normal) 
    painter.setFont(subtitle_font)
    subtitle_text = "Initializing, please wait..."
    font_metrics_sub = QFontMetrics(subtitle_font)
    subtitle_bounding_rect = font_metrics_sub.boundingRect(QRect(0,0,splash_width - 20, splash_height // 2), Qt.AlignmentFlag.AlignCenter, subtitle_text)

    total_text_height = main_text_bounding_rect.height() + subtitle_bounding_rect.height() + 15 
    
    main_text_y_offset = (splash_height - total_text_height) // 2
    
    painter.setFont(main_font) 
    main_text_draw_rect = QRect( (splash_width - main_text_bounding_rect.width()) // 2 , 
                                 main_text_y_offset, 
                                 main_text_bounding_rect.width(), 
                                 main_text_bounding_rect.height() )
    painter.drawText(main_text_draw_rect, Qt.AlignmentFlag.AlignCenter, main_text)
    
    subtitle_y_offset = main_text_y_offset + main_text_bounding_rect.height() + 15
    painter.setFont(subtitle_font) 
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
    
    # Main Window Creation and Startup
    main_window = WebBrowserWindow() 


    SPLASH_DURATION_MS = 2500 
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
