import objc
import CoreWLAN


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
