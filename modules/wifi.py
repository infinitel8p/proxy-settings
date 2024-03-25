import os
import re
import time
import logging
import subprocess
import customtkinter
from pywifi import PyWiFi, const, Profile

logging.getLogger('pywifi').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def get_connected_ssid():
    """
    Retrieves the SSID of the currently connected WiFi network.

    This function uses the `netsh wlan show interfaces` command to obtain details about the current wireless
    network connection. It parses the command output to extract the SSID of the network the device is currently
    connected to. If no SSID is found (indicating no current connection), the function returns None.

    Returns:
        str: The SSID of the currently connected WiFi network, or None if the device is not connected to any network.
    """

    # Function to get the SSID of the currently connected Wi-Fi network
    command = "netsh wlan show interfaces"
    try:

        result = subprocess.check_output(
            command, shell=True, text=True, stderr=subprocess.STDOUT, encoding='cp850')
        for line in result.split('\n'):
            if "SSID" in line and "BSSID" not in line:
                return re.findall(r':\s*(.*)', line)[0].strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get connected SSID: {e.output}")
    return None


def scan_wifi_networks():
    """
    Scans for available WiFi networks and returns their details.

    This function uses the `netsh` command to list available Wi-Fi networks and parses its output
    to extract SSIDs, signal strengths, and authentication types of the networks. The networks are then sorted
    by signal strength in descending order.

    Returns:
        A list of dictionaries, where each dictionary represents a WiFi network with keys 'ssid', 'signal', and 'auth'.
        'signal' is an integer representing the signal strength percentage, 'ssid' is the name of the network,
        and 'auth' is the authentication type. If 'auth' or 'ssid' could not be determined, they are set to 'Unknown'.
    """

    # Run the "netsh" command to list the available Wi-Fi networks
    result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'],
                            capture_output=True, text=True, encoding='cp850')  # Using cp850 encoding for Windows console output - may need to adjust for other systems (e.g., utf-8)

    # Parse the output to extract the SSIDs, signal strengths, and authentication types of the available networks
    networks = []
    current_network = {}
    connected_ssid = get_connected_ssid()

    for line in result.stdout.split('\n'):
        line = line.strip()
        if line.startswith('SSID'):
            ssid = re.findall(r':\s*(.*)', line)[0]
            current_network['ssid'] = ssid
        elif line.startswith('Auth'):
            auth = re.findall(r':\s*(.*)', line)[0]
            current_network['auth'] = auth
        elif line.startswith('Signal'):
            signal = int(re.findall(r':\s*(.*)%', line)[0])
            current_network['signal'] = signal
            current_network['connected'] = (ssid == connected_ssid)
            networks.append(current_network.copy())
            current_network.clear()

    # Set authentication type to 'Unknown' for networks where it was not found
    for network in networks:
        if 'auth' not in network:
            network['auth'] = 'Unknown'

    # Set SSID to 'Unknown' for networks where it was not found
    for network in networks:
        if 'ssid' not in network or network['ssid'] == '':
            network['ssid'] = 'Unknown'
            network['connected'] = False

    # Sort the list of networks by signal strength
    networks.sort(key=lambda x: (-x.get('connected', False), -x['signal']))

    return networks


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
    Disconnects from a specified WiFi network.

    This function disconnects the device from the WiFi network specified by the SSID.
    If the device is not connected to the specified network, it logs a message indicating that the device is not connected to that network.

    Parameters:
        ssid (str): The SSID of the WiFi network to disconnect from.
        wifi_ui: A reference to the GUI component that initiated the disconnect action.
    """

    wifi = PyWiFi()
    iface = wifi.interfaces()[0]  # Select the first wireless interface

    if is_already_connected(ssid):
        iface.disconnect()
        logger.info(f"Disconnected from {ssid}")
    else:
        logger.info(f"Not connected to {ssid}")

    wifi_ui.master.master.set("Proxy Settings")


def find_network_profile(iface, ssid):
    """
    Searches for an existing network profile by SSID on the given wireless interface.

    Parameters:
        iface: The wireless interface object from PyWiFi.
        ssid (str): The SSID of the WiFi network to search for.

    Returns:
        The network profile matching the SSID if found, None otherwise.
    """

    existing_profiles = iface.network_profiles()
    for profile in existing_profiles:
        if profile.ssid == ssid:
            return profile
    return None


def create_profile(ssid, password):
    """
    Creates a new profile for connecting to a WiFi network.

    This function sets up a profile with the given SSID and password, configuring it for WPA2-PSK authentication by default.

    Parameters:
        ssid (str): The SSID of the WiFi network.
        password (str): The password for the WiFi network.

    Returns:
        A PyWiFi Profile object configured for the specified network.
    """

    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password
    return profile


def is_already_connected(ssid):
    """
    Checks if the device is already connected to a specified WiFi network.

    Parameters:
        ssid (str): The SSID of the WiFi network to check against the currently connected network.

    Returns:
        True if the device is currently connected to the network specified by the SSID, False otherwise.
    """

    connected_ssid = get_connected_ssid()
    return connected_ssid == ssid


def wait_for_connection(iface, timeout=10):
    """
    Waits for a connection to be established to a WiFi network.

    This function waits for up to a specified timeout for the device to connect to a WiFi network,
    checking the connection status at 1-second intervals.

    Parameters:
        iface: The wireless interface object from PyWiFi.
        timeout (int, optional): The maximum time to wait for a connection, in seconds. Default is 10 seconds.

    Returns:
        A string indicating the connection result, either "Connected" or "Timeout".
    """

    start_time = time.time()
    while time.time() - start_time < timeout:
        if iface.status() == const.IFACE_CONNECTED:
            return "Connected"
        time.sleep(1)
    return "Timeout"
