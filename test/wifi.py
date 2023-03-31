import subprocess
import re

# Run the "netsh" command to list the available Wi-Fi networks
result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'],
                        capture_output=True, text=True, encoding='cp850')

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

# Sort the list of networks by signal strength
networks = sorted(networks, key=lambda x: x['signal'], reverse=True)

# Print the list of networks sorted by signal strength, with signal strength and authentication type for each network
# for network in networks:
#    if 'ssid' not in network:
#        continue
#    print(
#        f"SSID: {network['ssid']}, Signal Strength: {network['signal']}%, Authentication Type: {network['auth']}")
print(networks)
