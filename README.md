# Crosshair Studio Pro 🎯

> **Crosshair Studio Pro** is a modern, ultra-sleek, multi-language desktop Crosshair Overlay & Configurator built with Python and PySide6. Designed with **Emil Kowalski Design Engineering** principles for high performance and clean aesthetics.

**Developed by:** Mustafa Mutlu

---

## 🌟 Key Features

- **🎯 Procedural Vector Engine**:
  - Classic Cross (`+`), Center Dot (`•`), T-Style Crosshair, Circle Ring, and Cross + Dot.
  - Sliders for Line Length, Thickness, Center Gap, Dot Radius, Rotation (`°`), and Opacity.
  - High-contrast customizable Dark Outline / Stroke shadow for maximum visibility on all game maps.

- **🖼️ Custom PNG & Web Image Crosshairs**:
  - Load local PNG, JPG, or WEBP crosshair images directly from your computer.
  - Download & import PNG crosshairs directly from any web URL (`https://...`).
  - Safe, normalized image scale slider (8px to 140px) to prevent screen overflow.

- **🌙 Dark Mode & ☀️ Light Mode Themes**:
  - Switch between **Koyu Tema (Dark Mode 🌙)** and **Açık Tema (Light Mode ☀️)** in one click.
  - Card-based UI containers, 18px rounded dialogs, scrollable panels, and responsive `:pressed` micro-interactions.

- **🇹🇷 Türkçe & 🇬🇧 English Bilingual Support**:
  - Dynamic language switcher updating all UI tabs, sliders, tooltips, buttons, and dialogs instantly.

- **💾 Custom Preset Management**:
  - Save custom crosshairs under your own custom names.
  - Built-in esports presets (*Valorant Cyan Dot*, *CS2 Classic Green*, *Apex Gold Ring*, *Overwatch Red Cross*, *Cyberpunk Neon Pink*, *Pro Precision Dot*, *Minimalist T-Style*).
  - Delete unwanted custom presets; auto-persists to `custom_presets.json`.

- **📌 Desktop Overlay Integration**:
  - Fullscreen transparent always-on-top overlay with 100% click-through input transparency (zero game interference).
  - System Tray integration & `ESC` key hide-to-tray shortcut.

---

## 🛠️ Installation & Usage

### 1. Requirements
Make sure Python 3.9+ is installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python main.py
```

---

## 💻 Building an Executable (Optional)

To package Crosshair Studio Pro as a standalone `.exe` using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile main.py --name "CrosshairStudioPro"
```

The compiled binary will be saved in the `dist/` directory.

---

## 📄 License & Credits

Created by **Mustafa Mutlu**.
Crafted with PySide6 & Design Engineering principles.
