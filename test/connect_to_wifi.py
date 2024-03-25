import subprocess
from pywifi import PyWiFi, const, Profile
import time
import logging


# Reset any existing logging configuration
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Now, configure the basic logging again
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logging.getLogger('pywifi').setLevel(logging.WARNING)


def connect_to_wifi(ssid, password=None):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]  # Select the first wireless interface

    # Check if already connected
    if is_already_connected(ssid):
        logging.info(f"Already connected to {ssid}.")
        return

    # Check if the network is known (saved)
    profile = find_network_profile(iface, ssid)
    if not profile:
        # It's a new network, prompt for password
        password = input(f"Enter password for {ssid}: ")

    # If profile exists but no password was provided, try to connect using the existing profile
    if profile and not password:
        logging.info(f"Trying to connect to known network {ssid}...")
        iface.connect(profile)
    else:
        # Connect with a new profile or provided password
        profile = create_profile(ssid, password)
        temp_profile = iface.add_network_profile(profile)
        iface.connect(temp_profile)

    result = wait_for_connection(iface)
    if result == "Connected":
        logging.info(f"Successfully connected to {ssid}")
    elif result == "Timeout":
        logging.warning(
            "Connection attempt timed out. Please check the network status and password.")
    else:
        logging.error("Failed to connect for an unknown reason.")


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
        logging.error(f"Failed to get connected SSID: {e.output}")
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


if __name__ == "__main__":
    ssid = ''  # Enter the SSID
    connect_to_wifi(ssid)
