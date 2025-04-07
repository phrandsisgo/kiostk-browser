import subprocess
import time
import pyautogui
import pygetwindow as gw

# 1. Starte Firefox im Kiosk-Modus (für Touchscreen)
subprocess.Popen([
    r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "--kiosk",
    "https://www.emuseum.ch/de/projection"
])

# 2. Warte ein paar Sekunden
time.sleep(3)

# 3. Starte ein zweites Firefox-Fenster (für Monitor)
subprocess.Popen([
    r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "--kiosk",
    "https://www.emuseum.ch/de/projection/screen"
])

# 4. Warte, bis das Fenster geladen ist
time.sleep(5)

# 5. Aktiviere das Fenster und drücke F11
windows = gw.getWindowsWithTitle("seite-fuer-monitor")  # Passe den Tab-Titel an
if windows:
    win = windows[0]
    win.activate()
    time.sleep(1)
    pyautogui.press('f11')
else:
    print("Fenster nicht gefunden")

# Optional: Fenster gezielt auf Monitor 2 verschieben
# Beispiel: win.moveTo(x=1920, y=0)  # Falls Monitor 2 rechts ist

# Setze die Koordinaten für die Fenster
windows = gw.getWindowsWithTitle("seite-fuer-touchscreen")  # Passe den Tab-Titel an
if windows:
    win = windows[0]
    win.moveTo(0, 0)
else:
    print("Fenster nicht gefunden")

windows = gw.getWindowsWithTitle("seite-fuer-monitor")  # Passe den Tab-Titel an
if windows:
    win = windows[0]
    win.moveTo(1920, 0)
else:
    print("Fenster nicht gefunden")
