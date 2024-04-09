import customtkinter
from modules import wifi
import platform


if platform.system() == "Darwin":
    import modules.wifi_macOS as wifi
elif platform.system() == "Windows":
    import modules.wifi as wifi


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
        """
        Starts the WiFi scanning process.

        This method initializes the process to update the list of available WiFi networks and the timer for refresh intervals.
        It calls `update_wifi_list` to populate the list of WiFi networks and `update_timer` to start the countdown for the refresh.
        """

        self.update_wifi_list()
        self.update_timer()

    def update_timer(self):
        """
        Updates the countdown timer for the next WiFi list refresh.

        This method decrements the countdown time every second and updates the timer label with the remaining time.
        Once the countdown reaches 0, the label is updated to indicate that a refresh is happening. The method
        schedules itself to be called every 1 second until the countdown reaches 0, at which point it resets the label and stops updating.
        """

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
        """
        Updates the list of available WiFi networks displayed to the user.

        This method resets the countdown timer for refreshing the WiFi list, clears any existing network frames from the previous scan,
        and performs a new scan for WiFi networks. For each network found, it creates a frame with the network's details displayed and a "Connect" button. If already connected to a network,
        the network's details are diplayed in green with a "Disconnect" button. It schedules `start_wifi_scanning` to be called again after the refresh interval
        to update the list regularly.
        """

        self.countdown_time = self.refresh_interval // 1000

        # Clear existing network frames
        for frame in self.network_frames:
            frame.destroy()
        self.network_frames.clear()

        # Scan for WiFi networks and get real data
        wifi_networks = wifi.scan_wifi_networks()
        connected_ssid = wifi.get_connected_ssid()

        # Create frames and widgets for each network
        for network in wifi_networks:
            frame = customtkinter.CTkFrame(master=self.networks_container)
            frame.pack(pady=5, fill=customtkinter.X)

            # Determine if this is the connected network
            is_connected = network['connected']

            # Updated to use 'ssid' and 'signal' keys
            label_text = f"{network['ssid']} - Signal: {network['signal']}%"
            label = customtkinter.CTkLabel(
                master=frame, text=label_text, font=("Arial", 10), text_color="green" if is_connected else "white")
            label.pack(side=customtkinter.LEFT, padx=(10, 0))

            # Display a "Disconnect" button for the connected network, "Connect" button for others
            button_text = "Disconnect" if is_connected else "Connect"
            if is_connected:
                def button_command(
                    ssid=connected_ssid): return wifi.disconnect_from_wifi(ssid, self)
            else:
                button_command = lambda ssid=network['ssid']: wifi.connect_to_wifi(
                    ssid, self)
            button = customtkinter.CTkButton(
                master=frame, text=button_text, width=50, height=20, command=button_command)
            button.pack(side=customtkinter.RIGHT, padx=(0, 5))

            self.network_frames.append(frame)  # Keep track of the frame

        # Schedule the next update
        self.after(self.refresh_interval, self.start_wifi_scanning)
