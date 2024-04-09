import os
import re
import time
import logging
import subprocess
import customtkinter

logger = logging.getLogger(__name__)

encoding = 'utf-8'


def get_connected_ssid():
    """
    Retrieves the SSID of the currently connected WiFi network on macOS using networksetup.

    This function uses the `networksetup -listallhardwareports` command to find the device name
    for the Wi-Fi interface, then uses `networksetup -getairportnetwork <device_name>` to obtain details
    about the current wireless network connection. It parses the command output to extract the SSID
    of the network the device is currently connected to. If no SSID is found (indicating no current connection),
    the function returns None.

    Returns:
        str: The SSID of the currently connected WiFi network, or None if the device is not connected to any network.
    """

    # Command to list all hardware ports
    list_ports_command = ["networksetup", "-listallhardwareports"]
    try:
        ports_result = subprocess.run(
            list_ports_command, check=True, capture_output=True, text=True)
        wifi_device = None
        for line in ports_result.stdout.split('\n'):
            if "Wi-Fi" in line or "Airport" in line:  # "Airport" is for backward compatibility
                wifi_device = line.split(": ")[1]
                break

        if wifi_device:
            # Command to get the SSID of the connected network using the Wi-Fi device name
            get_ssid_command = ["networksetup",
                                "-getairportnetwork", wifi_device]
            ssid_result = subprocess.run(
                get_ssid_command, check=True, capture_output=True, text=True)
            ssid = re.search(r'Current Wi-Fi Network: (.*)',
                             ssid_result.stdout)
            if ssid:
                return ssid.group(1).strip()
    except subprocess.CalledProcessError as e:
        print(f"Failed to get connected SSID: {e.stderr}")
    return None


print(get_connected_ssid())


def scan_wifi_networks():
    """
    Scans for available WiFi networks and returns their details.

    Returns:
        A list of dictionaries, where each dictionary represents a WiFi network with keys 'ssid', 'signal', and 'auth'.
        'signal' is an integer representing the signal strength percentage, 'ssid' is the name of the network,
        and 'auth' is the authentication type. If 'auth' or 'ssid' could not be determined, they are set to 'Unknown'.
    """

    return None


def connect_to_wifi(ssid, wifi_ui, password=None):
    """
    Attempts to connect to a specified WiFi network.

    This function handles the connection process to a WiFi network specified by the SSID. It checks if the device
    is already connected to the target network, searches for a known network profile, and either connects using an existing
    profile or prompts for a password to create a new profile. The connection result is logged.

    Parameters:
        ssid (str): The SSID of the WiFi network to connect to.
        wifi_ui: A reference to the GUI component that initiated the disconnect action.
        password (str, optional): The password for the WiFi network. If not provided and the network is not known,
                                the user will be prompted to enter a password.

    Notes:
        - The function logs information about the connection process, including success, timeout, and failure messages.
        - If connecting to a network that requires a password not provided in the call, the function will prompt the user to input it.
    """

    wifi = PyWiFi()
    iface = wifi.interfaces()[0]  # Select the first wireless interface

    # Check if already connected
    if is_already_connected(ssid):
        logger.info(f"Already connected to {ssid}.")
        return

    # Check if the network is known (saved)
    profile = find_network_profile(iface, ssid)
    if not profile:
        # It's a new network, prompt for password
        dialog = customtkinter.CTkInputDialog(
            text=f"Enter password for {ssid}:", title="Password required")
        from tkinter import PhotoImage
        dialog.iconphoto(True, PhotoImage(file=os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))), "images", "verbindung.png")))

        password = dialog.get_input()
        if password == None:
            logger.warning("Connection cancelled by the user.")
            return

    # If profile exists but no password was provided, try to connect using the existing profile
    if profile and not password:
        logger.info(f"Trying to connect to known network {ssid}...")
        iface.connect(profile)
    else:
        # Connect with a new profile or provided password
        profile = create_profile(ssid, password)
        temp_profile = iface.add_network_profile(profile)
        iface.connect(temp_profile)

    result = wait_for_connection(iface)
    if result == "Connected":
        logger.info(f"Successfully connected to {ssid}")
    elif result == "Timeout":
        logger.warning(
            "Connection attempt timed out. Please check the network status and password.")
    else:
        logger.error("Failed to connect for an unknown reason.")

    wifi_ui.master.master.set("Proxy Settings")


def disconnect_from_wifi(ssid, wifi_ui):
    """
    This function disconnects the device from the WiFi network specified by the SSID.
    If the device is not connected to the specified network, it logs a message indicating that the device is not connected to that network.

    Parameters:
        ssid (str): The SSID of the WiFi network to disconnect from.
        wifi_ui: A reference to the GUI component that initiated the disconnect action.
    """

    pass


def find_network_profile(iface, ssid):
    """
    Searches for an existing network profile by SSID on the given wireless interface.

    Parameters:
        iface: The wireless interface object from PyWiFi.
        ssid (str): The SSID of the WiFi network to search for.

    Returns:
        The network profile matching the SSID if found, None otherwise.
    """

    return None


def create_profile(ssid, password):
    """
    This function sets up a profile with the given SSID and password, configuring it for WPA2-PSK authentication by default.

    Parameters:
        ssid (str): The SSID of the WiFi network.
        password (str): The password for the WiFi network.

    Returns:
        A PyWiFi Profile object configured for the specified network.
    """

    return None


def is_already_connected(ssid):
    """
    Checks if the device is already connected to a specified WiFi network.

    Parameters:
        ssid (str): The SSID of the WiFi network to check against the currently connected network.

    Returns:
        True if the device is currently connected to the network specified by the SSID, False otherwise.
    """

    return None


def wait_for_connection(iface, timeout=10):
    """
    This function waits for up to a specified timeout for the device to connect to a WiFi network,
    checking the connection status at 1-second intervals.

    Parameters:
        iface: The wireless interface object from PyWiFi.
        timeout (int, optional): The maximum time to wait for a connection, in seconds. Default is 10 seconds.

    Returns:
        A string indicating the connection result, either "Connected" or "Timeout".
    """

    return None
