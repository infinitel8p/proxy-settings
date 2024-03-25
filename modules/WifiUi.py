import customtkinter
import subprocess
import re


class WifiUi(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.configure(fg_color="transparent")
        self.root = parent
        self.refresh_interval = 10000

        self.network_frames = []  # Keep track of the network frames

        self.wifi_list_label = customtkinter.CTkLabel(
            master=self, text="Available WiFi Networks", font=("Arial", 12))
        self.wifi_list_label.pack(pady=(0, 5))

        self.networks_container = customtkinter.CTkScrollableFrame(master=self)
        self.networks_container.pack(
            fill=customtkinter.BOTH, expand=True)

        self.timer_label = customtkinter.CTkLabel(
            master=self, text="Next refresh in 5 seconds", text_color="grey", font=("Arial", 10))
        self.timer_label.pack(side=customtkinter.BOTTOM)

        self.start_wifi_scanning()

    def start_wifi_scanning(self):
        self.update_wifi_list()
        self.update_timer()

    def update_timer(self):
        # Decrement the timer and update the label
        self.countdown_time -= 1
        self.timer_label.configure(
            text=f"Next refresh in {self.countdown_time} seconds")

        if self.countdown_time > 0:
            # Schedule the timer to update again in 1 second
            self.after(1000, self.update_timer)
        else:
            # Reset the timer label when it reaches 0
            self.timer_label.configure(text="Refreshing...")

    def update_wifi_list(self):
        self.countdown_time = self.refresh_interval // 1000

        # Clear existing network frames
        for frame in self.network_frames:
            frame.destroy()
        self.network_frames.clear()

        # Scan for WiFi networks and get real data
        wifi_networks = self.scan_wifi_networks()

        # Create frames and widgets for each network
        for network in wifi_networks:
            frame = customtkinter.CTkFrame(master=self.networks_container)
            frame.pack(pady=5, fill=customtkinter.X)

            # Updated to use 'ssid' and 'signal' keys
            label_text = f"{network['ssid']} - Signal: {network['signal']}%"
            label = customtkinter.CTkLabel(
                master=frame, text=label_text, font=("Arial", 10))
            label.pack(side=customtkinter.LEFT, padx=(10, 0))

            # Ensure the lambda function captures the current network's 'ssid' correctly in the loop
            button = customtkinter.CTkButton(master=frame, text="Connect", width=50, height=20,
                                             command=lambda n=network['ssid']: self.connect_to_network(n))
            button.pack(side=customtkinter.RIGHT, padx=(0, 5))

            self.network_frames.append(frame)  # Keep track of the frame

        # Schedule the next update
        self.after(self.refresh_interval, self.start_wifi_scanning)

    def scan_wifi_networks(self):
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

    def connect_to_network(self, network_name):
        # Placeholder action for connecting to a network
        print(f"Connecting to {network_name}...")
