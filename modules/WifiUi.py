import customtkinter
import random


class WifiUi(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.configure(fg_color="transparent")
        self.root = parent

        self.network_frames = []  # Keep track of the network frames

        self.wifi_list_label = customtkinter.CTkLabel(
            master=self, text="Available WiFi Networks", font=("Arial", 12))
        self.wifi_list_label.pack(pady=(10, 0))

        self.networks_container = customtkinter.CTkFrame(master=self)
        self.networks_container.pack(
            fill=customtkinter.BOTH, expand=True, padx=20, pady=(10, 20))

        self.simulate_wifi_scanning()

    def simulate_wifi_scanning(self):
        self.update_wifi_list()
        self.after(5000, self.simulate_wifi_scanning)

    def update_wifi_list(self):
        # Clear existing network frames
        for frame in self.network_frames:
            frame.destroy()
        self.network_frames.clear()

        # Generate simulated WiFi networks
        wifi_networks = [
            {"name": "WiFi_1", "strength": "Strong"},
            {"name": "WiFi_2", "strength": "Moderate"},
            {"name": "WiFi_3", "strength": "Weak"},
            {"name": "Home_Network", "strength": "Strong"},
        ]

        # Simulate network changes
        if random.choice([True, False]):
            wifi_networks.append({
                "name": f"New_Network_{random.randint(4, 100)}",
                "strength": random.choice(['Weak', 'Moderate', 'Strong'])
            })
        if random.choice([True, False]) and wifi_networks:
            wifi_networks.pop(random.randint(0, len(wifi_networks) - 1))

        # Create frames and widgets for each network
        for network in wifi_networks:
            frame = customtkinter.CTkFrame(master=self.networks_container)
            frame.pack(pady=5, fill=customtkinter.X)

            label = customtkinter.CTkLabel(
                master=frame, text=f"{network['name']} - {network['strength']}", font=("Arial", 10))
            label.pack(side=customtkinter.LEFT, padx=(10, 0))

            button = customtkinter.CTkButton(
                master=frame, text="Connect", width=50, height=20, command=lambda n=network['name']: self.connect_to_network(n))
            button.pack(side=customtkinter.RIGHT, padx=(0, 10))

            self.network_frames.append(frame)  # Keep track of the frame

    def connect_to_network(self, network_name):
        # Placeholder action for connecting to a network
        print(f"Connecting to {network_name}...")
