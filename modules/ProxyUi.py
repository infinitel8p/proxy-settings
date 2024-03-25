import customtkinter
import logging
from modules import proxy
from modules.loggingHandler import TkinterHandler


class ProxyUi(customtkinter.CTkFrame):
    def __init__(self, parent, version):

        # Main Frame
        super().__init__(master=parent)
        self.configure(fg_color="transparent")
        self.root = parent

        # Create the main frames for widgets
        self.frame = customtkinter.CTkFrame(
            master=self, fg_color="transparent")
        self.frame.pack(pady=15, padx=15, fill="both", expand=True)

        self.horizontal_frame = customtkinter.CTkFrame(
            master=self.frame, fg_color="transparent")
        self.horizontal_frame.grid(
            row=0, column=0, sticky="ew", padx=5, pady=5)
        self.frame.grid_columnconfigure(
            0, weight=1)

        # Proxy Address Entry
        self.entry_ip = customtkinter.CTkEntry(
            self.horizontal_frame, width=75, justify="center", placeholder_text="Proxy ip-address")
        self.entry_ip.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.entry_ip.insert(0, proxy.fill_in_ip())
        self.entry_ip.bind("<Return>", command=self.proxy_changer)

        # Proxy Port Entry
        self.entry_port = customtkinter.CTkEntry(
            self.horizontal_frame, width=50, justify="center", placeholder_text="Proxy port")
        self.entry_port.grid(row=0, column=1, sticky="ew", padx=(0, 5))
        self.entry_port.insert(0, proxy.fill_in_port())
        self.entry_port.bind("<Return>", command=self.proxy_changer)

        # Apply Button
        self.button = customtkinter.CTkButton(
            self.horizontal_frame, width=50, text="Apply", command=self.proxy_changer)
        self.button.grid(row=0, column=2, sticky="ew")

        # Configure horizontal frame's columns to distribute space
        self.horizontal_frame.grid_columnconfigure(
            0, weight=3)
        self.horizontal_frame.grid_columnconfigure(
            1, weight=1)
        self.horizontal_frame.grid_columnconfigure(
            2, weight=1)

        # Proxy ON/OFF Switch
        self.switch = customtkinter.CTkSwitch(
            master=self.frame, text="Turn Proxy ON/OFF", progress_color="green", command=self.proxy_toggle)
        self.switch.grid(row=1, column=0, sticky="w", padx=5, pady=(10, 0))

        # Status Label
        self.label = customtkinter.CTkLabel(
            master=self.frame, text="Disabled", text_color="red")
        self.label.grid(row=1, column=0, sticky="e", padx=15, pady=(10, 0))

        self.version_label = customtkinter.CTkLabel(
            self, text=f"version {version}", text_color="grey", font=("Arial", 10))
        self.version_label.pack(side=customtkinter.BOTTOM)

        # Set up the log output widget
        self.log_output = customtkinter.CTkTextbox(self, height=150)
        self.log_output.pack(side=customtkinter.BOTTOM,
                             fill=customtkinter.BOTH, expand=True, padx=5)

        # Set up the logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # Add the TkinterHandler to the logger
        self.handler = TkinterHandler(self.log_output)
        self.logger.addHandler(self.handler)

    def proxy_changer(self, event=None):
        """
        Changes the proxy address to the value entered in the Tkinter Entry widget.

        Args:
            event (Event, optional): The event that triggered this method. Defaults to None.
        """
        proxy.change_address(f"{self.entry_ip.get()}:{self.entry_port.get()}")

    def proxy_toggle(self):
        """
        Toggles the proxy on or off based on the value of the switch.
        If the switch is off, the proxy is deactivated and the label text changes to 'Disabled' in red.
        If the switch is on, the proxy is activated and the label text changes to 'Enabled' in green.
        """
        is_on = self.switch.get() == 1
        action = proxy.activate if is_on else proxy.deactivate
        label_text = "Enabled" if is_on else "Disabled"
        text_color = "green" if is_on else "red"

        if action():
            self.label.configure(text=label_text, text_color=text_color)
        else:
            # Reset the switch to its original state if the action fails
            if is_on:
                self.switch.deselect()
            else:
                self.switch.select()
