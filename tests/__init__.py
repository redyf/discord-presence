import os
import platform
import subprocess
from pypresence import Presence
import psutil
from uptime import uptime
from Xlib import X, display, error
import time

# Initialize Discord Rich Presence
client_id = ""  # Replace with your Discord Application Client ID
RPC = Presence(client_id)
RPC.connect()


def get_active_window_title():
    try:
        active_window = (
            subprocess.check_output(["wdisplays", "-r", "window"]).decode().strip()
        )
        return active_window
    except subprocess.CalledProcessError:
        return None


def get_system_info():
    system_info = {
        "os": platform.system(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "ram_usage": psutil.virtual_memory().percent,
        "uptime": int(uptime()),
        "active_window": get_active_window_title(),
    }
    # Calculate uptime in days, hours, and minutes
    uptime_seconds = int(system_info["uptime"])
    uptime_days = uptime_seconds // (24 * 3600)
    uptime_hours = (uptime_seconds % (24 * 3600)) // 3600
    uptime_minutes = (uptime_seconds % 3600) // 60

    system_info[
        "uptime_formatted"
    ] = f"{uptime_days}d {uptime_hours}h {uptime_minutes}m"
    return system_info


def update_presence():
    system_info = get_system_info()
    details = f"OS: {system_info['os']} | Uptime: {system_info['uptime_formatted']}"
    state = f"CPU: {system_info['cpu_usage']}% | RAM: {system_info['ram_usage']}%"
    large_image = "lofi"  # Replace with your large image key
    large_text = "Rain is a beautiful thing isn't it?"

    active_window = get_active_window_title() or "No Active Window"
    small_image_key = active_window.replace(
        " ", "_"
    ).lower()  # Use window title as the small image key

    small_image = "nixos"  # Replace with your default small image key
    small_text = active_window

    buttons = [{"label": "My profile", "url": "https://github.com/redyf"}]

    RPC.update(
        details=details,
        state=state,
        large_image=large_image,
        large_text=large_text,
        small_image=small_image_key,
        small_text=active_window,
        buttons=buttons,
    )


if __name__ == "__main__":
    while True:
        update_presence()
        time.sleep(30)  # Update every 30 seconds
