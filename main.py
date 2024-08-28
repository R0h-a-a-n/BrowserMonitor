import psutil
import time
import win32gui
import re

blocked_keywords = ["keyword"]

def get_active_window_title():
    window = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(window)
    return window_title

def monitor_firefox():
    try:
        while True:
            active_window_title = get_active_window_title()

            if "firefox" in active_window_title.lower():
                print(f"Monitoring active Firefox window: {active_window_title}")

                for keyword in blocked_keywords:
                    if re.search(keyword, active_window_title, re.IGNORECASE):
                        print(f"Blocked keyword '{keyword}' detected. Killing Firefox...")
                        kill_firefox_processes()
                        break

            time.sleep(2)  
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")

def kill_firefox_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() in ["firefox", "firefox.exe"]:
            try:
                proc.terminate()  
                proc.wait(timeout=3)  
                print(f"Terminated Firefox process: {proc.info['pid']}")
            except psutil.NoSuchProcess:
                print(f"Process {proc.info['pid']} does not exist.")
            except psutil.TimeoutExpired:
                print(f"Process {proc.info['pid']} did not terminate in time, force killing...")
                proc.kill()  
                print(f"Force killed Firefox process: {proc.info['pid']}")

if __name__ == "__main__":
    monitor_firefox()

# back to the past?
