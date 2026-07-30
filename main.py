"""main.py
Crosshair Studio Pro - Emil Kowalski Design Engineering Edition

Key Features & Upgrades:
- Dark Mode 🌙 & Light Mode ☀️ Theme Switcher in Settings tab.
- "by Mustafa Mutlu" credit line included in Settings.
- Tab names: Nişangah, Renk, Ön Ayarlar, Görsel, Ayarlar.
- Bounded PNG scale (8px..140px) to prevent screen overflow & click blocking.
- Multi-Language (TR/EN), custom preset save/delete/persist, URL import.
"""

import sys
import os
import json
import urllib.request
from PySide6 import QtCore, QtGui, QtWidgets

PRESETS_FILE = os.path.join(os.path.dirname(__file__), "custom_presets.json")

# ---------------------------------------------------------------
# Multi-Language Dictionary (TR / EN)
# ---------------------------------------------------------------
TRANSLATIONS = {
    "tr": {
        "title": "CROSSHAIR STUDIO PRO",
        "tab_geometry": "Nişangah",
        "tab_color": "Renk",
        "tab_presets": "Ön Ayarlar",
        "tab_image": "Görsel",
        "tab_settings": "Ayarlar",
        "preview_scene": "ÖNİZLEME SAHNESİ:",
        "crosshair_type": "NIŞANGAH TİPİ",
        "length": "Çizgi Uzunluğu",
        "width": "Çizgi Kalınlığı",
        "gap": "Merkez Boşluğu",
        "dot_radius": "Nokta Yarıçapı",
        "rotation": "Döndürme (°)",
        "png_scale": "PNG Görsel Ölçeği (%)",
        "quick_swatches": "HIZLI RENK PALETİ",
        "red": "Kırmızı (R)",
        "green": "Yeşil (G)",
        "blue": "Mavi (B)",
        "opacity": "Genel Opaklık",
        "outline_enable": "Siyah Çerçeve / Gölge Ekle",
        "outline_width": "Çerçeve Kalınlığı",
        "built_in_presets": "HAZIR SPOR NİŞANGAHLARI",
        "custom_presets": "KAYDETTİĞİNİZ ÖZEL NİŞANGAHLAR",
        "preset_name_ph": "Özel preset adı yazın...",
        "btn_save_preset": "Preset'i Kaydet",
        "btn_delete_preset": "Seçili Preset'i Sil",
        "btn_toggle_overlay": "Nişangahı Aç / Kapat",
        "btn_hide_tray": "Tepsiye Gizle",
        "png_section_title": "BİLGİSAYARDAN PNG YÜKLE",
        "btn_browse_file": "PNG Dosyası Seç...",
        "url_import_title": "WEB URL İLE GÖRSEL YÜKLE",
        "url_ph": "https://site.com/crosshair.png",
        "btn_download_url": "URL'den İndir & Yükle",
        "lang_section": "DİL SEÇİMİ / LANGUAGE",
        "theme_section": "TEMA SEÇİMİ / THEME",
        "theme_dark": "Koyu Tema 🌙",
        "theme_light": "Açık Tema ☀️",
        "developer_credit": "by Mustafa Mutlu",
        "shortcut_info": "İpucu: ESC tuşu pencereyi sistem tepsisine gizler.",
        "dark_grid": "Koyu Izgara",
        "light_grid": "Açık Izgara",
        "pure_black": "Saf Siyah",
        "msg_saved": "Preset başarıyla kaydedildi!",
        "msg_deleted": "Preset silindi.",
        "msg_invalid_url": "Lütfen geçerli bir resim URL'si girin.",
        "msg_img_loaded": "Görsel nişangah olarak yüklendi!",
        "msg_img_error": "Resim indirilemedi veya geçersiz format.",
    },
    "en": {
        "title": "CROSSHAIR STUDIO PRO",
        "tab_geometry": "Crosshair",
        "tab_color": "Color",
        "tab_presets": "Presets",
        "tab_image": "Image",
        "tab_settings": "Settings",
        "preview_scene": "PREVIEW SCENE:",
        "crosshair_type": "CROSSHAIR TYPE",
        "length": "Line Length",
        "width": "Thickness",
        "gap": "Center Gap",
        "dot_radius": "Dot Radius",
        "rotation": "Rotation (°)",
        "png_scale": "PNG Scale (%)",
        "quick_swatches": "QUICK COLOR PALETTE",
        "red": "Red (R)",
        "green": "Green (G)",
        "blue": "Blue (B)",
        "opacity": "Overall Opacity",
        "outline_enable": "Enable Dark Outline / Shadow",
        "outline_width": "Outline Thickness",
        "built_in_presets": "BUILT-IN PRESETS",
        "custom_presets": "YOUR SAVED PRESETS",
        "preset_name_ph": "Enter custom preset name...",
        "btn_save_preset": "Save Preset",
        "btn_delete_preset": "Delete Selected Preset",
        "btn_toggle_overlay": "Toggle Overlay",
        "btn_hide_tray": "Hide to Tray",
        "png_section_title": "LOAD LOCAL PNG FILE",
        "btn_browse_file": "Browse PNG File...",
        "url_import_title": "IMPORT FROM WEB URL",
        "url_ph": "https://site.com/crosshair.png",
        "btn_download_url": "Download & Apply URL",
        "lang_section": "LANGUAGE SELECTION",
        "theme_section": "THEME SELECTION",
        "theme_dark": "Dark Mode 🌙",
        "theme_light": "Light Mode ☀️",
        "developer_credit": "by Mustafa Mutlu",
        "shortcut_info": "Tip: Press ESC to hide the settings window to tray.",
        "dark_grid": "Dark Grid",
        "light_grid": "Light Grid",
        "pure_black": "Pure Black",
        "msg_saved": "Preset saved successfully!",
        "msg_deleted": "Preset deleted.",
        "msg_invalid_url": "Please enter a valid image URL.",
        "msg_img_loaded": "Image applied as crosshair!",
        "msg_img_error": "Failed to download or parse image.",
    }
}


# ---------------------------------------------------------------
# System Tray Icon Generator
# ---------------------------------------------------------------
def create_tray_icon() -> QtGui.QIcon:
    pixmap = QtGui.QPixmap(32, 32)
    pixmap.fill(QtCore.Qt.transparent)
    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    
    # Outer dark shadow
    painter.setPen(QtCore.Qt.NoPen)
    painter.setBrush(QtGui.QColor(0, 0, 0, 140))
    painter.drawEllipse(3, 3, 26, 26)

    # Accent blue circle
    painter.setBrush(QtGui.QColor(10, 132, 255))
    painter.drawEllipse(2, 2, 26, 26)

    # Crosshair vector lines
    pen = QtGui.QPen(QtCore.Qt.white, 2)
    pen.setCapStyle(QtCore.Qt.RoundCap)
    painter.setPen(pen)
    painter.drawLine(16, 9, 16, 13)
    painter.drawLine(16, 19, 16, 23)
    painter.drawLine(9, 16, 13, 16)
    painter.drawLine(19, 16, 23, 16)
    painter.drawPoint(16, 16)
    painter.end()
    
    return QtGui.QIcon(pixmap)


# ---------------------------------------------------------------
# Emil Design Engineering QSS Tokens (DARK MODE)
# ---------------------------------------------------------------
EMIL_DARK_QSS = """
QDialog, QWidget#MainContainer {
    background-color: #1a1a1e;
    color: #f4f4f7;
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif;
    border-radius: 18px;
}

QWidget#HeaderBar {
    background-color: #24242a;
    border-top-left-radius: 18px;
    border-top-right-radius: 18px;
    border-bottom: 1px solid #383842;
}

QWidget#CardPanel {
    background-color: #24242a;
    border: 1px solid #383842;
    border-radius: 14px;
}

QLabel {
    color: #a0a0ab;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.4px;
}

QLabel#TitleText {
    color: #ffffff;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.8px;
}

QScrollArea {
    background: transparent;
    border: none;
}

QScrollBar:vertical {
    background: #1a1a1e;
    width: 6px;
    border-radius: 3px;
}

QScrollBar::handle:vertical {
    background: #383842;
    border-radius: 3px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background: #50505c;
}

QTabWidget::pane {
    border: 1px solid #383842;
    border-radius: 14px;
    background-color: #1a1a1e;
    top: -1px;
}

QTabBar::tab {
    background: #24242a;
    color: #a0a0ab;
    padding: 10px 14px;
    font-size: 11px;
    font-weight: 600;
    border-radius: 10px;
    margin: 3px 2px;
}

QTabBar::tab:selected {
    background: #0a84ff;
    color: #ffffff;
}

QTabBar::tab:hover:!selected {
    background: #383842;
    color: #f4f4f7;
}

QComboBox, QLineEdit {
    background-color: #1a1a1e;
    color: #ffffff;
    border: 1px solid #383842;
    border-radius: 10px;
    padding: 9px 12px;
    font-size: 12px;
    font-weight: 500;
}

QComboBox:hover, QLineEdit:focus {
    border-color: #0a84ff;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #24242a;
    color: #ffffff;
    selection-background-color: #0a84ff;
    border: 1px solid #383842;
    border-radius: 10px;
    padding: 6px;
}

QSlider::groove:horizontal {
    height: 6px;
    background: #383842;
    border-radius: 3px;
}

QSlider::sub-page:horizontal {
    background: #0a84ff;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #ffffff;
    width: 18px;
    height: 18px;
    margin-top: -6px;
    margin-bottom: -6px;
    border-radius: 9px;
    border: 1px solid #e4e4e7;
}

QSlider::handle:horizontal:hover {
    background: #f4f4f7;
    border-color: #0a84ff;
}

QPushButton {
    background-color: #24242a;
    color: #ffffff;
    border: 1px solid #383842;
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #383842;
    border-color: #50505c;
}

QPushButton:pressed {
    background-color: #141418;
    padding-top: 11px;
    padding-bottom: 9px;
}

QPushButton#PrimaryBtn {
    background-color: #0a84ff;
    border: none;
    color: #ffffff;
}

QPushButton#PrimaryBtn:hover {
    background-color: #0071e3;
}

QPushButton#DangerBtn {
    background-color: #ef4444;
    border: none;
    color: #ffffff;
}

QPushButton#DangerBtn:hover {
    background-color: #dc2626;
}

QPushButton#SwatchBtn {
    border-radius: 14px;
    border: 2px solid #383842;
}

QPushButton#SwatchBtn:hover {
    border-color: #ffffff;
}

QRadioButton {
    color: #f4f4f7;
    font-size: 12px;
    font-weight: 600;
}
"""


# ---------------------------------------------------------------
# Emil Design Engineering QSS Tokens (LIGHT MODE)
# ---------------------------------------------------------------
EMIL_LIGHT_QSS = """
QDialog, QWidget#MainContainer {
    background-color: #f4f4f7;
    color: #1c1c1e;
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif;
    border-radius: 18px;
}

QWidget#HeaderBar {
    background-color: #e5e5ea;
    border-top-left-radius: 18px;
    border-top-right-radius: 18px;
    border-bottom: 1px solid #d1d1d6;
}

QWidget#CardPanel {
    background-color: #ffffff;
    border: 1px solid #d1d1d6;
    border-radius: 14px;
}

QLabel {
    color: #636366;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.4px;
}

QLabel#TitleText {
    color: #1c1c1e;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.8px;
}

QScrollArea {
    background: transparent;
    border: none;
}

QScrollBar:vertical {
    background: #f4f4f7;
    width: 6px;
    border-radius: 3px;
}

QScrollBar::handle:vertical {
    background: #d1d1d6;
    border-radius: 3px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background: #aeaeb2;
}

QTabWidget::pane {
    border: 1px solid #d1d1d6;
    border-radius: 14px;
    background-color: #f4f4f7;
    top: -1px;
}

QTabBar::tab {
    background: #e5e5ea;
    color: #636366;
    padding: 10px 14px;
    font-size: 11px;
    font-weight: 600;
    border-radius: 10px;
    margin: 3px 2px;
}

QTabBar::tab:selected {
    background: #0a84ff;
    color: #ffffff;
}

QTabBar::tab:hover:!selected {
    background: #d1d1d6;
    color: #1c1c1e;
}

QComboBox, QLineEdit {
    background-color: #ffffff;
    color: #1c1c1e;
    border: 1px solid #d1d1d6;
    border-radius: 10px;
    padding: 9px 12px;
    font-size: 12px;
    font-weight: 500;
}

QComboBox:hover, QLineEdit:focus {
    border-color: #0a84ff;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #1c1c1e;
    selection-background-color: #0a84ff;
    selection-color: #ffffff;
    border: 1px solid #d1d1d6;
    border-radius: 10px;
    padding: 6px;
}

QSlider::groove:horizontal {
    height: 6px;
    background: #e5e5ea;
    border-radius: 3px;
}

QSlider::sub-page:horizontal {
    background: #0a84ff;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #ffffff;
    width: 18px;
    height: 18px;
    margin-top: -6px;
    margin-bottom: -6px;
    border-radius: 9px;
    border: 1px solid #aeaeb2;
}

QSlider::handle:horizontal:hover {
    background: #f4f4f7;
    border-color: #0a84ff;
}

QPushButton {
    background-color: #ffffff;
    color: #1c1c1e;
    border: 1px solid #d1d1d6;
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #f4f4f7;
    border-color: #aeaeb2;
}

QPushButton:pressed {
    background-color: #e5e5ea;
    padding-top: 11px;
    padding-bottom: 9px;
}

QPushButton#PrimaryBtn {
    background-color: #0a84ff;
    border: none;
    color: #ffffff;
}

QPushButton#PrimaryBtn:hover {
    background-color: #0071e3;
}

QPushButton#DangerBtn {
    background-color: #ef4444;
    border: none;
    color: #ffffff;
}

QPushButton#DangerBtn:hover {
    background-color: #dc2626;
}

QPushButton#SwatchBtn {
    border-radius: 14px;
    border: 2px solid #d1d1d6;
}

QPushButton#SwatchBtn:hover {
    border-color: #1c1c1e;
}

QRadioButton {
    color: #1c1c1e;
    font-size: 12px;
    font-weight: 600;
}
"""


# ---------------------------------------------------------------
# Core Crosshair Render Engine
# ---------------------------------------------------------------
class CrosshairRenderer:
    @staticmethod
    def draw(painter: QtGui.QPainter, cx: int, cy: int, params: dict):
        style = params.get("style", "Cross")
        length = params.get("length", 12)
        width = params.get("width", 2)
        gap = params.get("gap", 4)
        dot_radius = params.get("dot_radius", 2)
        color = params.get("color", QtGui.QColor(0, 255, 150))
        opacity = params.get("opacity", 255) / 255.0
        
        outline_enabled = params.get("outline_enabled", True)
        outline_color = params.get("outline_color", QtGui.QColor(0, 0, 0))
        outline_width = params.get("outline_width", 1)
        rotation = params.get("rotation", 0)

        png_pixmap = params.get("png_pixmap", None)
        png_scale = params.get("png_scale", 100) / 100.0

        painter.save()
        painter.translate(cx, cy)
        if rotation != 0:
            painter.rotate(rotation)

        # Custom PNG
        if style == "Custom PNG" and png_pixmap and not png_pixmap.isNull():
            base_size = 32
            target_dim = max(6, int(base_size * png_scale))
            target_dim = min(140, target_dim)

            scaled_pixmap = png_pixmap.scaled(
                target_dim, target_dim,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            painter.setOpacity(opacity)
            painter.drawPixmap(-scaled_pixmap.width() // 2, -scaled_pixmap.height() // 2, scaled_pixmap)
            painter.restore()
            return

        # Procedural Vector
        final_color = QtGui.QColor(color)
        final_color.setAlpha(int(final_color.alpha() * opacity))
        
        final_outline_color = QtGui.QColor(outline_color)
        final_outline_color.setAlpha(int(final_outline_color.alpha() * opacity))

        def draw_lines(pen: QtGui.QPen):
            painter.setPen(pen)
            if style in ("Cross", "T-Style", "Cross + Dot"):
                painter.drawLine(-gap - length, 0, -gap, 0)
                painter.drawLine(gap, 0, gap + length, 0)
                painter.drawLine(0, gap, 0, gap + length)
                if style != "T-Style":
                    painter.drawLine(0, -gap - length, 0, -gap)

            elif style == "Circle":
                radius = gap + length
                painter.setBrush(QtCore.Qt.NoBrush)
                painter.drawEllipse(QtCore.QPoint(0, 0), radius, radius)

        if outline_enabled and outline_width > 0:
            out_pen = QtGui.QPen(final_outline_color, width + (outline_width * 2))
            out_pen.setCapStyle(QtCore.Qt.SquareCap)
            draw_lines(out_pen)
            
            if dot_radius > 0 or style == "Dot":
                r_out = dot_radius + outline_width
                painter.setPen(QtCore.Qt.NoPen)
                painter.setBrush(QtGui.QBrush(final_outline_color))
                painter.drawEllipse(QtCore.QPoint(0, 0), r_out, r_out)

        main_pen = QtGui.QPen(final_color, width)
        main_pen.setCapStyle(QtCore.Qt.SquareCap)
        draw_lines(main_pen)

        if (dot_radius > 0 and style != "Circle") or style == "Dot":
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QtGui.QBrush(final_color))
            painter.drawEllipse(QtCore.QPoint(0, 0), dot_radius, dot_radius)

        painter.restore()


# ---------------------------------------------------------------
# Live Preview Canvas Widget
# ---------------------------------------------------------------
class CrosshairPreviewWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(320, 150)
        self.setFixedHeight(155)
        self.backdrop_mode = "Dark Grid"
        self.params = {}

    def set_params(self, params: dict):
        self.params = params
        self.update()

    def set_backdrop(self, mode: str):
        self.backdrop_mode = mode
        self.update()

    def paintEvent(self, _: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        w, h = self.width(), self.height()

        if self.backdrop_mode == "Light Grid":
            painter.fillRect(0, 0, w, h, QtGui.QColor(240, 240, 245))
            painter.setPen(QtGui.QPen(QtGui.QColor(215, 215, 225), 1))
            grid_size = 20
            for x in range(0, w, grid_size):
                painter.drawLine(x, 0, x, h)
            for y in range(0, h, grid_size):
                painter.drawLine(0, y, w, y)

        elif self.backdrop_mode == "Pure Black":
            painter.fillRect(0, 0, w, h, QtGui.QColor(12, 12, 14))

        else: # Dark Grid
            painter.fillRect(0, 0, w, h, QtGui.QColor(24, 24, 28))
            painter.setPen(QtGui.QPen(QtGui.QColor(42, 42, 50), 1))
            grid_size = 20
            for x in range(0, w, grid_size):
                painter.drawLine(x, 0, x, h)
            for y in range(0, h, grid_size):
                painter.drawLine(0, y, w, y)

        painter.setPen(QtGui.QPen(QtGui.QColor(56, 56, 66), 1))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRoundedRect(0, 0, w - 1, h - 1, 12, 12)

        CrosshairRenderer.draw(painter, w // 2, h // 2, self.params)


# ---------------------------------------------------------------
# Transparent Fullscreen Overlay Window
# ---------------------------------------------------------------
class OverlayWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.Tool
            | QtCore.Qt.WindowTransparentForInput
        )
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.showFullScreen()
        
        self.params = {
            "style": "Cross",
            "length": 12,
            "width": 2,
            "gap": 4,
            "dot_radius": 2,
            "color": QtGui.QColor(0, 255, 150),
            "opacity": 255,
            "outline_enabled": True,
            "outline_color": QtGui.QColor(0, 0, 0),
            "outline_width": 1,
            "rotation": 0,
            "png_pixmap": None,
            "png_scale": 100,
        }

    def update_params(self, new_params: dict):
        self.params.update(new_params)
        self.update()

    def paintEvent(self, _: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        CrosshairRenderer.draw(painter, self.width() // 2, self.height() // 2, self.params)

    def toggle(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()


# ---------------------------------------------------------------
# Config Window
# ---------------------------------------------------------------
class ConfigWindow(QtWidgets.QDialog):
    def __init__(self, overlay: OverlayWindow):
        super().__init__()
        self.overlay = overlay
        self.current_lang = "tr"
        self.current_theme = "dark"
        self.custom_presets = self.load_custom_presets_from_file()
        self.loaded_pixmap = None

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setMinimumSize(480, 680)
        self.resize(500, 740)
        self.setStyleSheet(EMIL_DARK_QSS)
        
        self.drag_position = QtCore.QPoint()

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        container = QtWidgets.QWidget()
        container.setObjectName("MainContainer")
        self.container_layout = QtWidgets.QVBoxLayout(container)
        self.container_layout.setSpacing(12)
        self.container_layout.setContentsMargins(20, 16, 20, 20)

        # 1. Header Bar
        header_widget = QtWidgets.QWidget()
        header_widget.setObjectName("HeaderBar")
        header_layout = QtWidgets.QHBoxLayout(header_widget)
        header_layout.setContentsMargins(14, 12, 14, 12)

        traffic_close = QtWidgets.QPushButton("")
        traffic_close.setFixedSize(12, 12)
        traffic_close.setStyleSheet("QPushButton { background-color: #ef4444; border: none; border-radius: 6px; } QPushButton:hover { background-color: #dc2626; }")
        traffic_close.clicked.connect(self.hide)

        traffic_min = QtWidgets.QPushButton("")
        traffic_min.setFixedSize(12, 12)
        traffic_min.setStyleSheet("QPushButton { background-color: #f59e0b; border: none; border-radius: 6px; } QPushButton:hover { background-color: #d97706; }")
        traffic_min.clicked.connect(self.showMinimized)

        self.title_lbl = QtWidgets.QLabel("CROSSHAIR STUDIO PRO")
        self.title_lbl.setObjectName("TitleText")

        header_layout.addWidget(traffic_close)
        header_layout.addWidget(traffic_min)
        header_layout.addSpacing(10)
        header_layout.addWidget(self.title_lbl)
        header_layout.addStretch()

        self.container_layout.addWidget(header_widget)

        # 2. Live Preview Box
        self.preview_widget = CrosshairPreviewWidget()
        self.container_layout.addWidget(self.preview_widget)

        backdrop_layout = QtWidgets.QHBoxLayout()
        self.backdrop_lbl = QtWidgets.QLabel("ÖNİZLEME SAHNESİ:")
        self.backdrop_lbl.setStyleSheet("font-size: 10px; font-weight: 700;")
        
        self.backdrop_combo = QtWidgets.QComboBox()
        self.backdrop_combo.setMinimumWidth(135)
        self.backdrop_combo.setFixedHeight(28)
        self.backdrop_combo.addItems(["Dark Grid", "Light Grid", "Pure Black"])
        self.backdrop_combo.currentTextChanged.connect(self.on_backdrop_changed)

        backdrop_layout.addWidget(self.backdrop_lbl)
        backdrop_layout.addWidget(self.backdrop_combo)
        backdrop_layout.addStretch()
        self.container_layout.addLayout(backdrop_layout)

        # 3. Main Tab Control
        self.tabs = QtWidgets.QTabWidget()
        
        # --- TAB 1: NİŞANGAH ---
        self.geom_tab = self._create_tab_scroll_area()
        geom_card = QtWidgets.QWidget()
        geom_card.setObjectName("CardPanel")
        geom_layout = QtWidgets.QVBoxLayout(geom_card)
        geom_layout.setSpacing(12)
        geom_layout.setContentsMargins(16, 16, 16, 16)

        style_layout = QtWidgets.QHBoxLayout()
        self.style_lbl = QtWidgets.QLabel("NIŞANGAH TİPİ")
        self.style_combo = QtWidgets.QComboBox()
        self.style_combo.addItems(["Cross", "Dot", "T-Style", "Circle", "Cross + Dot", "Custom PNG"])
        self.style_combo.currentTextChanged.connect(self.update_config)
        style_layout.addWidget(self.style_lbl)
        style_layout.addWidget(self.style_combo)
        geom_layout.addLayout(style_layout)

        self.length_slider, self.lbl_length = self._make_slider(0, 80, 12, "Line Length", geom_layout)
        self.width_slider, self.lbl_width = self._make_slider(1, 16, 2, "Thickness", geom_layout)
        self.gap_slider, self.lbl_gap = self._make_slider(0, 40, 4, "Center Gap", geom_layout)
        self.dot_slider, self.lbl_dot = self._make_slider(0, 12, 2, "Dot Radius", geom_layout)
        self.rotation_slider, self.lbl_rot = self._make_slider(0, 180, 0, "Rotation (°)", geom_layout)
        self.png_scale_slider, self.lbl_png_scale = self._make_slider(10, 300, 100, "PNG Scale (%)", geom_layout)

        self.geom_tab.widget().layout().addWidget(geom_card)

        # --- TAB 2: RENK ---
        self.color_tab = self._create_tab_scroll_area()
        color_card = QtWidgets.QWidget()
        color_card.setObjectName("CardPanel")
        color_layout = QtWidgets.QVBoxLayout(color_card)
        color_layout.setSpacing(12)
        color_layout.setContentsMargins(16, 16, 16, 16)

        self.swatch_lbl = QtWidgets.QLabel("HIZLI RENK PALETİ")
        color_layout.addWidget(self.swatch_lbl)
        
        swatches_layout = QtWidgets.QHBoxLayout()
        swatches = [
            ("Cyan", "#00ffff"),
            ("Green", "#00ff96"),
            ("Yellow", "#ffd700"),
            ("Red", "#ef4444"),
            ("Pink", "#ec4899"),
            ("White", "#ffffff"),
        ]
        for name, hex_code in swatches:
            btn = QtWidgets.QPushButton("")
            btn.setObjectName("SwatchBtn")
            btn.setFixedSize(28, 28)
            btn.setStyleSheet(f"background-color: {hex_code}; border-radius: 14px;")
            btn.setToolTip(name)
            btn.clicked.connect(lambda _, h=hex_code: self.apply_hex_color(h))
            swatches_layout.addWidget(btn)
        swatches_layout.addStretch()
        color_layout.addLayout(swatches_layout)

        self.r_slider, self.lbl_r = self._make_slider(0, 255, 0, "Red (R)", color_layout)
        self.g_slider, self.lbl_g = self._make_slider(0, 255, 255, "Green (G)", color_layout)
        self.b_slider, self.lbl_b = self._make_slider(0, 255, 150, "Blue (B)", color_layout)
        self.opacity_slider, self.lbl_op = self._make_slider(10, 255, 255, "Opacity", color_layout)

        self.outline_check = QtWidgets.QCheckBox("Enable Dark Outline / Shadow")
        self.outline_check.setChecked(True)
        self.outline_check.setStyleSheet("font-weight: 600;")
        self.outline_check.stateChanged.connect(self.update_config)
        color_layout.addWidget(self.outline_check)

        self.outline_width_slider, self.lbl_out_w = self._make_slider(1, 6, 1, "Outline Width", color_layout)
        self.color_tab.widget().layout().addWidget(color_card)

        # --- TAB 3: ÖN AYARLAR ---
        self.preset_tab = self._create_tab_scroll_area()
        preset_card = QtWidgets.QWidget()
        preset_card.setObjectName("CardPanel")
        preset_layout = QtWidgets.QVBoxLayout(preset_card)
        preset_layout.setSpacing(12)
        preset_layout.setContentsMargins(16, 16, 16, 16)

        self.lbl_builtin_presets = QtWidgets.QLabel("HAZIR SPOR NİŞANGAHLARI")
        preset_layout.addWidget(self.lbl_builtin_presets)

        self.preset_combo = QtWidgets.QComboBox()
        self.preset_combo.addItems([
            "Valorant Cyan Dot",
            "CS2 Classic Green",
            "Apex Gold Ring",
            "Overwatch Red Cross",
            "Cyberpunk Neon Pink",
            "Pro Precision Dot",
            "Minimalist T-Style",
        ])
        self.preset_combo.currentTextChanged.connect(self.apply_builtin_preset)
        preset_layout.addWidget(self.preset_combo)

        preset_layout.addSpacing(6)
        self.lbl_custom_presets = QtWidgets.QLabel("KAYDETTİĞİNİZ ÖZEL NİŞANGAHLAR")
        preset_layout.addWidget(self.lbl_custom_presets)

        self.custom_preset_combo = QtWidgets.QComboBox()
        self.refresh_custom_preset_combo()
        self.custom_preset_combo.currentTextChanged.connect(self.apply_custom_preset)
        preset_layout.addWidget(self.custom_preset_combo)

        save_box = QtWidgets.QHBoxLayout()
        self.preset_name_input = QtWidgets.QLineEdit()
        self.preset_name_input.setPlaceholderText("Özel preset adı yazın...")
        self.btn_save_preset = QtWidgets.QPushButton("Preset'i Kaydet")
        self.btn_save_preset.setObjectName("PrimaryBtn")
        self.btn_save_preset.clicked.connect(self.save_current_preset)
        save_box.addWidget(self.preset_name_input)
        save_box.addWidget(self.btn_save_preset)
        preset_layout.addLayout(save_box)

        self.btn_delete_preset = QtWidgets.QPushButton("Seçili Preset'i Sil")
        self.btn_delete_preset.setObjectName("DangerBtn")
        self.btn_delete_preset.clicked.connect(self.delete_selected_preset)
        preset_layout.addWidget(self.btn_delete_preset)
        
        self.preset_tab.widget().layout().addWidget(preset_card)

        # --- TAB 4: GÖRSEL ---
        self.image_tab = self._create_tab_scroll_area()
        image_card = QtWidgets.QWidget()
        image_card.setObjectName("CardPanel")
        image_layout = QtWidgets.QVBoxLayout(image_card)
        image_layout.setSpacing(14)
        image_layout.setContentsMargins(16, 16, 16, 16)

        self.lbl_png_title = QtWidgets.QLabel("BİLGİSAYARDAN PNG YÜKLE")
        image_layout.addWidget(self.lbl_png_title)

        self.btn_browse_png = QtWidgets.QPushButton("PNG Dosyası Seç...")
        self.btn_browse_png.clicked.connect(self.browse_png_file)
        image_layout.addWidget(self.btn_browse_png)

        image_layout.addSpacing(6)
        self.lbl_url_title = QtWidgets.QLabel("WEB URL İLE GÖRSEL YÜKLE")
        image_layout.addWidget(self.lbl_url_title)

        self.url_input = QtWidgets.QLineEdit()
        self.url_input.setPlaceholderText("https://site.com/crosshair.png")
        image_layout.addWidget(self.url_input)

        self.btn_download_url = QtWidgets.QPushButton("URL'den İndir & Yükle")
        self.btn_download_url.setObjectName("PrimaryBtn")
        self.btn_download_url.clicked.connect(self.download_from_url)
        image_layout.addWidget(self.btn_download_url)
        
        self.image_tab.widget().layout().addWidget(image_card)

        # --- TAB 5: AYARLAR ---
        self.settings_tab = self._create_tab_scroll_area()
        settings_card = QtWidgets.QWidget()
        settings_card.setObjectName("CardPanel")
        settings_layout = QtWidgets.QVBoxLayout(settings_card)
        settings_layout.setSpacing(14)
        settings_layout.setContentsMargins(16, 16, 16, 16)

        # Language Switcher
        self.lbl_lang_section = QtWidgets.QLabel("DİL SEÇİMİ / LANGUAGE")
        settings_layout.addWidget(self.lbl_lang_section)

        lang_box = QtWidgets.QHBoxLayout()
        self.radio_tr = QtWidgets.QRadioButton("Türkçe 🇹🇷")
        self.radio_en = QtWidgets.QRadioButton("English 🇬🇧")
        self.radio_tr.setChecked(True)
        self.radio_tr.toggled.connect(lambda ch: self.switch_language("tr") if ch else None)
        self.radio_en.toggled.connect(lambda ch: self.switch_language("en") if ch else None)
        lang_box.addWidget(self.radio_tr)
        lang_box.addWidget(self.radio_en)
        lang_box.addStretch()
        settings_layout.addLayout(lang_box)

        settings_layout.addSpacing(6)

        # Theme Switcher (Dark Mode / Light Mode)
        self.lbl_theme_section = QtWidgets.QLabel("TEMA SEÇİMİ / THEME")
        settings_layout.addWidget(self.lbl_theme_section)

        theme_box = QtWidgets.QHBoxLayout()
        self.radio_dark = QtWidgets.QRadioButton("Koyu Tema 🌙")
        self.radio_light = QtWidgets.QRadioButton("Açık Tema ☀️")
        self.radio_dark.setChecked(True)
        self.radio_dark.toggled.connect(lambda ch: self.switch_theme("dark") if ch else None)
        self.radio_light.toggled.connect(lambda ch: self.switch_theme("light") if ch else None)
        theme_box.addWidget(self.radio_dark)
        theme_box.addWidget(self.radio_light)
        theme_box.addStretch()
        settings_layout.addLayout(theme_box)

        settings_layout.addSpacing(10)

        # Developer Credit & Info
        self.lbl_developer_credit = QtWidgets.QLabel("by Mustafa Mutlu")
        self.lbl_developer_credit.setStyleSheet("font-size: 13px; font-weight: 800; color: #0a84ff; letter-spacing: 1px;")
        settings_layout.addWidget(self.lbl_developer_credit)

        self.lbl_shortcut_info = QtWidgets.QLabel("İpucu: ESC tuşu pencereyi sistem tepsisine gizler.")
        self.lbl_shortcut_info.setStyleSheet("color: #0a84ff; font-size: 11px; font-weight: 600;")
        settings_layout.addWidget(self.lbl_shortcut_info)
        
        self.settings_tab.widget().layout().addWidget(settings_card)

        # Add tabs
        self.tabs.addTab(self.geom_tab, "Nişangah")
        self.tabs.addTab(self.color_tab, "Renk")
        self.tabs.addTab(self.preset_tab, "Ön Ayarlar")
        self.tabs.addTab(self.image_tab, "Görsel")
        self.tabs.addTab(self.settings_tab, "Ayarlar")

        self.container_layout.addWidget(self.tabs)

        # 4. Footer Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.toggle_overlay_btn = QtWidgets.QPushButton("Nişangahı Aç / Kapat")
        self.toggle_overlay_btn.setObjectName("PrimaryBtn")
        self.toggle_overlay_btn.clicked.connect(self.toggle_overlay)

        self.hide_btn = QtWidgets.QPushButton("Tepsiye Gizle")
        self.hide_btn.clicked.connect(self.hide)

        btn_layout.addWidget(self.toggle_overlay_btn)
        btn_layout.addWidget(self.hide_btn)
        self.container_layout.addLayout(btn_layout)

        main_layout.addWidget(container)

        self.apply_builtin_preset("Valorant Cyan Dot")
        self.switch_language("tr")

    def _create_tab_scroll_area(self) -> QtWidgets.QScrollArea:
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        content_w = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(content_w)
        layout.setContentsMargins(4, 4, 4, 4)
        scroll.setWidget(content_w)
        return scroll

    def switch_theme(self, theme_code: str):
        self.current_theme = theme_code
        if theme_code == "light":
            self.setStyleSheet(EMIL_LIGHT_QSS)
        else:
            self.setStyleSheet(EMIL_DARK_QSS)

    def switch_language(self, lang_code: str):
        self.current_lang = lang_code
        t = TRANSLATIONS[lang_code]
        
        self.title_lbl.setText(t["title"])
        self.backdrop_lbl.setText(t["preview_scene"])
        
        # Tabs
        self.tabs.setTabText(0, t["tab_geometry"])
        self.tabs.setTabText(1, t["tab_color"])
        self.tabs.setTabText(2, t["tab_presets"])
        self.tabs.setTabText(3, t["tab_image"])
        self.tabs.setTabText(4, t["tab_settings"])

        # Geometry tab
        self.style_lbl.setText(t["crosshair_type"])
        self.lbl_length.setText(t["length"])
        self.lbl_width.setText(t["width"])
        self.lbl_gap.setText(t["gap"])
        self.lbl_dot.setText(t["dot_radius"])
        self.lbl_rot.setText(t["rotation"])
        self.lbl_png_scale.setText(t["png_scale"])

        # Color tab
        self.swatch_lbl.setText(t["quick_swatches"])
        self.lbl_r.setText(t["red"])
        self.lbl_g.setText(t["green"])
        self.lbl_b.setText(t["blue"])
        self.lbl_op.setText(t["opacity"])
        self.outline_check.setText(t["outline_enable"])
        self.lbl_out_w.setText(t["outline_width"])

        # Presets tab
        self.lbl_builtin_presets.setText(t["built_in_presets"])
        self.lbl_custom_presets.setText(t["custom_presets"])
        self.preset_name_input.setPlaceholderText(t["preset_name_ph"])
        self.btn_save_preset.setText(t["btn_save_preset"])
        self.btn_delete_preset.setText(t["btn_delete_preset"])

        # Image tab
        self.lbl_png_title.setText(t["png_section_title"])
        self.btn_browse_png.setText(t["btn_browse_file"])
        self.lbl_url_title.setText(t["url_import_title"])
        self.url_input.setPlaceholderText(t["url_ph"])
        self.btn_download_url.setText(t["btn_download_url"])

        # Settings tab
        self.lbl_lang_section.setText(t["lang_section"])
        self.lbl_theme_section.setText(t["theme_section"])
        self.radio_dark.setText(t["theme_dark"])
        self.radio_light.setText(t["theme_light"])
        self.lbl_developer_credit.setText(t["developer_credit"])
        self.lbl_shortcut_info.setText(t["shortcut_info"])

        # Footer
        self.toggle_overlay_btn.setText(t["btn_toggle_overlay"])
        self.hide_btn.setText(t["btn_hide_tray"])

        # Backdrop
        self.backdrop_combo.setItemText(0, t["dark_grid"])
        self.backdrop_combo.setItemText(1, t["light_grid"])
        self.backdrop_combo.setItemText(2, t["pure_black"])

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.hide()
            event.accept()
            return
        super().keyPressEvent(event)

    def _make_slider(self, min_val, max_val, start, label, parent_layout):
        header_layout = QtWidgets.QHBoxLayout()
        lbl_name = QtWidgets.QLabel(label)
        lbl_name.setStyleSheet("font-size: 11px; font-weight: 500; text-transform: none;")
        
        lbl_val = QtWidgets.QLabel(str(start))
        lbl_val.setStyleSheet("color: #0a84ff; font-weight: 700; font-size: 11px;")
        
        header_layout.addWidget(lbl_name)
        header_layout.addStretch()
        header_layout.addWidget(lbl_val)

        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(start)
        slider.valueChanged.connect(lambda v, l=lbl_val: l.setText(str(v)))
        slider.valueChanged.connect(self.update_config)

        parent_layout.addLayout(header_layout)
        parent_layout.addWidget(slider)
        return slider, lbl_name

    def apply_hex_color(self, hex_code: str):
        col = QtGui.QColor(hex_code)
        self.r_slider.setValue(col.red())
        self.g_slider.setValue(col.green())
        self.b_slider.setValue(col.blue())

    def apply_builtin_preset(self, name: str):
        presets = {
            "Valorant Cyan Dot": ("Dot", 0, 2, 0, 3, 0, (0, 255, 255), True, 1),
            "CS2 Classic Green": ("Cross", 14, 2, 4, 0, 0, (0, 255, 120), True, 1),
            "Apex Gold Ring": ("Circle", 10, 2, 6, 0, 0, (255, 215, 0), True, 1),
            "Overwatch Red Cross": ("Cross + Dot", 10, 2, 3, 2, 0, (255, 59, 48), True, 1),
            "Cyberpunk Neon Pink": ("Cross", 16, 2, 6, 0, 45, (255, 45, 85), True, 1),
            "Pro Precision Dot": ("Dot", 0, 2, 0, 2, 0, (255, 255, 255), True, 1),
            "Minimalist T-Style": ("T-Style", 12, 2, 2, 0, 0, (0, 255, 180), True, 1),
        }
        data = presets.get(name, ("Cross", 12, 2, 4, 2, 0, (0, 255, 150), True, 1))
        
        style, length, width, gap, dot, rot, (r, g, b), out_en, out_w = data
        self.style_combo.setCurrentText(style)
        self.length_slider.setValue(length)
        self.width_slider.setValue(width)
        self.gap_slider.setValue(gap)
        self.dot_slider.setValue(dot)
        self.rotation_slider.setValue(rot)
        self.r_slider.setValue(r)
        self.g_slider.setValue(g)
        self.b_slider.setValue(b)
        self.outline_check.setChecked(out_en)
        self.outline_width_slider.setValue(out_w)
        self.update_config()

    def load_custom_presets_from_file(self) -> dict:
        if os.path.exists(PRESETS_FILE):
            try:
                with open(PRESETS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def save_custom_presets_to_file(self):
        try:
            with open(PRESETS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.custom_presets, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Failed to save custom presets:", e)

    def refresh_custom_preset_combo(self):
        self.custom_preset_combo.blockSignals(True)
        self.custom_preset_combo.clear()
        if self.custom_presets:
            self.custom_preset_combo.addItems(list(self.custom_presets.keys()))
        else:
            self.custom_preset_combo.addItem("-- Yok / None --")
        self.custom_preset_combo.blockSignals(False)

    def save_current_preset(self):
        name = self.preset_name_input.text().strip()
        if not name:
            return
        
        data = {
            "style": self.style_combo.currentText(),
            "length": self.length_slider.value(),
            "width": self.width_slider.value(),
            "gap": self.gap_slider.value(),
            "dot_radius": self.dot_slider.value(),
            "rotation": self.rotation_slider.value(),
            "r": self.r_slider.value(),
            "g": self.g_slider.value(),
            "b": self.b_slider.value(),
            "opacity": self.opacity_slider.value(),
            "outline_enabled": self.outline_check.isChecked(),
            "outline_width": self.outline_width_slider.value(),
            "png_scale": self.png_scale_slider.value(),
        }
        
        self.custom_presets[name] = data
        self.save_custom_presets_to_file()
        self.refresh_custom_preset_combo()
        self.custom_preset_combo.setCurrentText(name)
        self.preset_name_input.clear()
        
        t = TRANSLATIONS[self.current_lang]
        QtWidgets.QMessageBox.information(self, "Crosshair Studio", t["msg_saved"])

    def delete_selected_preset(self):
        name = self.custom_preset_combo.currentText()
        if name in self.custom_presets:
            del self.custom_presets[name]
            self.save_custom_presets_to_file()
            self.refresh_custom_preset_combo()
            t = TRANSLATIONS[self.current_lang]
            QtWidgets.QMessageBox.information(self, "Crosshair Studio", t["msg_deleted"])

    def apply_custom_preset(self, name: str):
        if name not in self.custom_presets:
            return
        p = self.custom_presets[name]
        self.style_combo.setCurrentText(p.get("style", "Cross"))
        self.length_slider.setValue(p.get("length", 12))
        self.width_slider.setValue(p.get("width", 2))
        self.gap_slider.setValue(p.get("gap", 4))
        self.dot_slider.setValue(p.get("dot_radius", 2))
        self.rotation_slider.setValue(p.get("rotation", 0))
        self.r_slider.setValue(p.get("r", 0))
        self.g_slider.setValue(p.get("g", 255))
        self.b_slider.setValue(p.get("b", 150))
        self.opacity_slider.setValue(p.get("opacity", 255))
        self.outline_check.setChecked(p.get("outline_enabled", True))
        self.outline_width_slider.setValue(p.get("outline_width", 1))
        self.png_scale_slider.setValue(p.get("png_scale", 100))
        self.update_config()

    def browse_png_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "PNG Nişangah Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg *.webp)"
        )
        if file_path and os.path.exists(file_path):
            pix = QtGui.QPixmap(file_path)
            if not pix.isNull():
                self.loaded_pixmap = pix
                self.style_combo.setCurrentText("Custom PNG")
                self.update_config()
                t = TRANSLATIONS[self.current_lang]
                QtWidgets.QMessageBox.information(self, "Crosshair Studio", t["msg_img_loaded"])

    def download_from_url(self):
        url = self.url_input.text().strip()
        t = TRANSLATIONS[self.current_lang]
        if not url.startswith("http://") and not url.startswith("https://"):
            QtWidgets.QMessageBox.warning(self, "Crosshair Studio", t["msg_invalid_url"])
            return

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = response.read()
                pix = QtGui.QPixmap()
                if pix.loadFromData(data):
                    self.loaded_pixmap = pix
                    self.style_combo.setCurrentText("Custom PNG")
                    self.update_config()
                    QtWidgets.QMessageBox.information(self, "Crosshair Studio", t["msg_img_loaded"])
                    return
        except Exception as e:
            print("URL download error:", e)

        QtWidgets.QMessageBox.critical(self, "Crosshair Studio", t["msg_img_error"])

    def on_backdrop_changed(self, text: str):
        if "Dark" in text or "Koyu" in text:
            mode = "Dark Grid"
        elif "Light" in text or "Açık" in text:
            mode = "Light Grid"
        else:
            mode = "Pure Black"
        self.preview_widget.set_backdrop(mode)

    def update_config(self):
        params = {
            "style": self.style_combo.currentText(),
            "length": self.length_slider.value(),
            "width": self.width_slider.value(),
            "gap": self.gap_slider.value(),
            "dot_radius": self.dot_slider.value(),
            "rotation": self.rotation_slider.value(),
            "color": QtGui.QColor(self.r_slider.value(), self.g_slider.value(), self.b_slider.value()),
            "opacity": self.opacity_slider.value(),
            "outline_enabled": self.outline_check.isChecked(),
            "outline_color": QtGui.QColor(0, 0, 0),
            "outline_width": self.outline_width_slider.value(),
            "png_pixmap": self.loaded_pixmap,
            "png_scale": self.png_scale_slider.value(),
        }
        self.preview_widget.set_params(params)
        self.overlay.update_params(params)

    def toggle_overlay(self):
        self.overlay.toggle()


# ---------------------------------------------------------------
# System Tray Integration
# ---------------------------------------------------------------
class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent, config_win, overlay):
        super().__init__(icon, parent)
        self.config_win = config_win
        self.overlay = overlay
        
        menu = QtWidgets.QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #24242a;
                color: #ffffff;
                border: 1px solid #383842;
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item:selected {
                background-color: #0a84ff;
                border-radius: 4px;
            }
        """)
        
        self.show_action = menu.addAction("Ayarları Göster / Settings")
        self.show_action.triggered.connect(self.show_settings)
        
        self.toggle_overlay_action = menu.addAction("Nişangah Aç/Kapat")
        self.toggle_overlay_action.triggered.connect(self.overlay.toggle)
        
        menu.addSeparator()
        
        quit_action = menu.addAction("Çıkış / Exit")
        quit_action.triggered.connect(QtWidgets.QApplication.instance().quit)
        
        self.setContextMenu(menu)
        self.activated.connect(self.on_activated)

    def show_settings(self):
        self.config_win.show()
        self.config_win.raise_()
        self.config_win.activateWindow()

    def on_activated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.DoubleClick:
            self.show_settings()


# ---------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    overlay = OverlayWindow()
    overlay.show()

    config = ConfigWindow(overlay)
    config.show()

    tray_icon = SystemTrayIcon(
        create_tray_icon(),
        parent=app,
        config_win=config,
        overlay=overlay,
    )
    tray_icon.show()

    def intercept_close(event):
        event.ignore()
        config.hide()
    config.closeEvent = intercept_close

    sys.exit(app.exec())

if __name__ == "__main__":
    main()