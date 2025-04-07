import subprocess
import time
import pyautogui
import pygetwindow as gw

# 1. Starte Firefox im Kiosk-Modus (für Touchscreen)
touchscreen_process = subprocess.Popen([
    r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "--kiosk",
    "https://www.emuseum.ch/de/projection"
])

# 2. Warte ein paar Sekunden, damit das Fenster Zeit hat, sich zu öffnen
time.sleep(3)

# Speichere alle aktuellen Firefox-Fenster
firefox_windows_before = gw.getWindowsWithTitle("Firefox")

# 3. Starte ein zweites Firefox-Fenster (für Monitor)
monitor_process = subprocess.Popen([
    r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "--new-window",
    "https://www.emuseum.ch/de/projection/screen"
])

# 4. Warte, bis das zweite Fenster geladen ist
time.sleep(5)

# Finde alle Firefox-Fenster nach dem Start des zweiten Fensters
firefox_windows_after = gw.getWindowsWithTitle("Firefox")

# Identifiziere das neu geöffnete Fenster (das zweite Fenster)
second_window = None
for window in firefox_windows_after:
    if window not in firefox_windows_before:
        second_window = window
        break

# Platziere die Fenster auf den jeweiligen Monitoren
first_window = firefox_windows_before[0] if firefox_windows_before else None

if first_window:
    print(f"Touchscreen-Fenster gefunden: {first_window.title}")
    first_window.moveTo(0, 0)
    first_window.resizeTo(1920, 1080)  # Passe die Größe an
else:
    print("Touchscreen-Fenster nicht gefunden")

if second_window:
    print(f"Monitor-Fenster gefunden: {second_window.title}")
    second_window.moveTo(1920, 0)  # Setze auf zweiten Monitor (x=1920)
    second_window.activate()
    time.sleep(1)
    pyautogui.press('f11')  # Vollbild für zweites Fenster
else:
    print("Monitor-Fenster nicht gefunden")

# Warte auf Benutzereingriff zum Beenden
input("Drücke Enter zum Beenden...")

# Optional: Prozesse beenden beim Programmende
touchscreen_process.terminate()
monitor_process.terminate()

