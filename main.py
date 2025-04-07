import subprocess
import time
import pyautogui
import pygetwindow as gw
import os

# Firefox installation path
firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"

# Ensure Firefox exists at the specified path
if not os.path.exists(firefox_path):
    firefox_path = r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
    if not os.path.exists(firefox_path):
        print("Firefox nicht gefunden. Bitte den Pfad überprüfen.")
        exit(1)

# Close any existing Firefox instances
os.system("taskkill /f /im firefox.exe")
time.sleep(2)

# Get monitor information (using pyautogui to get screen size)
screen_width, screen_height = pyautogui.size()
# Assuming dual monitor setup with equal resolution
monitor1_bounds = (0, 0, screen_width // 2, screen_height)
monitor2_bounds = (screen_width // 2, 0, screen_width, screen_height)

print(f"Erkannte Bildschirmgröße: {screen_width}x{screen_height}")
print(f"Monitor 1: {monitor1_bounds}")
print(f"Monitor 2: {monitor2_bounds}")

# 1. Start Firefox on primary display (Touchscreen)
print("Starte Firefox im Kiosk-Modus auf dem Touchscreen...")
touchscreen_process = subprocess.Popen([
    firefox_path,
    "--kiosk",
    "https://www.emuseum.ch/de/projection"
])

# Wait for the window to open
time.sleep(5)

# Get the first Firefox window
firefox_windows = gw.getWindowsWithTitle("Firefox")
if firefox_windows:
    first_window = firefox_windows[0]
    print(f"Touchscreen-Fenster gefunden: {first_window.title}")
    # Ensure window is positioned on first monitor
    first_window.moveTo(monitor1_bounds[0], monitor1_bounds[1])
    first_window.resizeTo(monitor1_bounds[2] - monitor1_bounds[0], 
                         monitor1_bounds[3] - monitor1_bounds[1])
else:
    print("Touchscreen-Fenster nicht gefunden")

# 2. Start Firefox on secondary display (Monitor)
print("Starte Firefox für den zweiten Monitor...")
monitor_process = subprocess.Popen([
    firefox_path,
    "--new-window",
    "https://www.emuseum.ch/de/projection/screen"
])

# Wait for the second window to load
time.sleep(5)

# Find all Firefox windows after the second window starts
firefox_windows_after = gw.getWindowsWithTitle("Firefox")

# Find the new window
second_window = None
if len(firefox_windows_after) > len(firefox_windows):
    for window in firefox_windows_after:
        if window not in firefox_windows:
            second_window = window
            break
else:
    # If we can't find a new window, try to use any available one
    second_window = firefox_windows_after[-1] if firefox_windows_after else None

if second_window:
    print(f"Monitor-Fenster gefunden: {second_window.title}")
    # Position on the second monitor
    second_window.moveTo(monitor2_bounds[0], monitor2_bounds[1])
    second_window.activate()
    time.sleep(1)
    # Make it fullscreen
    pyautogui.press('f11')
else:
    print("Monitor-Fenster nicht gefunden")

print("Beide Browser sind gestartet. Drücke Strg+C im Terminal, um zu beenden.")

try:
    # Keep the script running
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Beende Anwendung...")
    # Terminate processes when the user interrupts
    touchscreen_process.terminate()
    monitor_process.terminate()

