import os
import re
import time
import logging
import subprocess
import customtkinter
import objc
import CoreWLAN

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

    try:
        # Command to get the SSID of the connected network using the Wi-Fi device name
        get_ssid_command = ["networksetup",
                            "-getairportnetwork", "en0"]  # en0 as default, may need to test/change
        ssid_result = subprocess.run(
            get_ssid_command, check=True, capture_output=True, text=True)
        ssid = re.search(r'Current Wi-Fi Network: (.*)',
                         ssid_result.stdout)
        if ssid:
            return ssid.group(1).strip()
    except subprocess.CalledProcessError as e:
        print(f"Failed to get connected SSID: {e.stderr}")
    return None


def scan_wifi_networks():
    """
    Scans for available WiFi networks on macOS and returns their details, including whether
    the network is the currently connected one.

    Due to macOS API limitations, this function lists available Wi-Fi networks and sets signal strengths
    and authentication types to 'Unknown'. It also indicates whether each network is the one currently connected.

    Returns:
        Available networks (list of dictionaries): A list where each dictionary represents a WiFi network with the following keys:
            - ssid (str): The SSID of the WiFi network.
            - signal (str): Placeholder for signal strength; always 'Unknown' due to macOS API limitations.
            - auth (str): Placeholder for authentication type; always 'Unknown' due to macOS API limitations.
            - connected (bool): Indicates if this is the currently connected network.
    """

    networks = []

    # Get the default WiFi interface
    wifi_interface = CoreWLAN.CWInterface.interface()

    # Get the SSID of the currently connected network, if any
    connected_ssid = wifi_interface.ssid()

    # Perform a scan for networks
    networks_list = wifi_interface.scanForNetworksWithSSID_error_(
        None, objc.nil)[0]

    seen_ssids = set()

    for network in networks_list:
        ssid_str = str(network.ssid())
        if ssid_str not in seen_ssids:
            seen_ssids.add(ssid_str)
            networks.append({
                'ssid': ssid_str,
                'signal': 'Unknown',  # macOS does not easily provide signal strength for scanned networks
                'auth': 'Unknown',  # macOS does not provide auth type for scanned networks in this method
                'connected': (ssid_str == connected_ssid)
            })

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

    # networksetup -setairportnetwork en0 WIFI_SSID_I_WANT_TO_JOIN WIFI_PASSWORD


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
