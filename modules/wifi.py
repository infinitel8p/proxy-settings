import subprocess
import re
import logging
import subprocess
from pywifi import PyWiFi, const, Profile
import time

logging.getLogger('pywifi').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


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

    # Sort the list of networks by signal strength
    networks = sorted(networks, key=lambda x: x['signal'], reverse=True)

    return networks


def connect_to_wifi(ssid, password=None):
    """
    Attempts to connect to a specified WiFi network.

    This function handles the connection process to a WiFi network specified by the SSID. It checks if the device
    is already connected to the target network, searches for a known network profile, and either connects using an existing
    profile or prompts for a password to create a new profile. The connection result is logged.

    Parameters:
        ssid (str): The SSID of the WiFi network to connect to.
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
        password = input(f"Enter password for {ssid}: ")

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


def get_connected_ssid():
    """
    Retrieves the SSID of the currently connected WiFi network.

    Uses the `netsh wlan show interfaces` command to find the currently connected network's SSID.

    Returns:
        The SSID of the currently connected network, or None if the SSID could not be determined or if not connected to any network.
    """

    # Get the currently connected SSID
    command = "netsh wlan show interfaces"
    try:
        output = subprocess.check_output(
            command, shell=True, text=True, stderr=subprocess.STDOUT, encoding='cp850')
        # Search for the SSID in the command output
        for line in output.split('\n'):
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get connected SSID: {e.output}")
    return None


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
