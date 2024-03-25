import subprocess
import re


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
    result = subprocess.run(command, capture_output=True,
                            text=True, shell=True, encoding='cp850')
    for line in result.stdout.split('\n'):
        if "SSID" in line and "BSSID" not in line:
            return re.findall(r':\s*(.*)', line)[0].strip()
    return None


# Run the "netsh" command to list the available Wi-Fi networks
result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'],
                        capture_output=True, text=True, encoding='cp850')

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
        # Determine if the current network is the one connected
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
        network['ssid'] = 'Hidden Network'
        network['connected'] = False

# Sort the list of networks by signal strength
networks = sorted(networks, key=lambda x: x['signal'], reverse=True)

# Print the list of networks sorted by signal strength, with signal strength and authentication type for each network
for network in networks:
    print(
        f"SSID: {network['ssid']}, Signal Strength: {network['signal']}%, Auth Type: {network['auth']}, Connected: {network['connected']}")
