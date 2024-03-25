import subprocess
import re
import logging
import subprocess
from pywifi import PyWiFi, const, Profile
import time

logging.getLogger('pywifi').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def scan_wifi_networks():
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
    existing_profiles = iface.network_profiles()
    for profile in existing_profiles:
        if profile.ssid == ssid:
            return profile
    return None


def create_profile(ssid, password):
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password
    return profile


def get_connected_ssid():
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
    connected_ssid = get_connected_ssid()
    return connected_ssid == ssid


def wait_for_connection(iface, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if iface.status() == const.IFACE_CONNECTED:
            return "Connected"
        time.sleep(1)
    return "Timeout"
