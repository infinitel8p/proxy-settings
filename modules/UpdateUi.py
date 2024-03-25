import customtkinter
import subprocess
import tempfile
import requests
import json
import time
import sys
import os


class UpdateUi(customtkinter.CTkToplevel):
    """This class is used to create a pop-up window to inform the user that a new version of the application is available and ask if they want to update.
    Attributes:
        hotkeys (list): List of hotkeys associated with the window
        updating (bool): A flag to indicate whether the update process is currently in progress
        parent (customtkinter.CTkToplevel): The parent window of this class
        background (CTkFrame): The background frame of the window
        label1 (CTkLabel): Label that displays the current and latest version of the application
        label2 (CTkLabel): Label that asks the user if they want to update
        button_grid (CTkFrame): Frame that contains the "Yes" and "No" buttons
        button1 (CTkButton): "No" button
        button2 (CTkButton): "Yes" button
    Methods:
        __init__(self, parent): Initializes the class by creating the window, setting its properties, creating the UI elements and adding the
        "Yes" and "No" buttons.
        add_output(self, text): Add text to the output textbox
        update(self, event=None): The function that downloads and installs the update. Defaults to `None`.
    """

    def __init__(self, parent):
        """Initializes the class by creating the window, setting its properties, creating the UI elements and adding the "Yes" and "No" buttons.
        Args:
            parent (customtkinter.CTkToplevel): The parent window of this class.
        """

        # Main Frame
        super().__init__(parent)
        self.hotkeys = []
        self.wm_title("Update Required")
        self.attributes("-topmost", True)
        self.attributes("-toolwindow", 1)
        self.parent = parent
        self.updating = False

        self.background = customtkinter.CTkFrame(
            self, bg_color=['gray92', 'gray14'], corner_radius=6)
        self.background.pack(padx=10, pady=10)

        # Set the label font and text size
        self.label1 = customtkinter.CTkLabel(
            self.background,
            text=f"A new version of the application is available.\nCurrent version: {self.parent.version} | Latest release: {self.parent.latest_version}",
            font=("Arial", 14, "bold"))
        self.label1.pack(padx=10, pady=5)

        self.label2 = customtkinter.CTkLabel(
            self.background, text="Would you like to update?")
        self.label2.pack(pady=5)

        self.button_grid = customtkinter.CTkFrame(
            self, fg_color="transparent")
        self.button_grid.pack(pady=(10, 15), side=customtkinter.BOTTOM)

        self.button1 = customtkinter.CTkButton(
            self.button_grid, text="No", command=self.destroy, width=90)
        self.button1.grid(row=0, column=0, padx=(0, 5))

        self.button2 = customtkinter.CTkButton(
            self.button_grid, text="Yes", command=self.update, width=90)
        self.button2.grid(row=0, column=1, padx=(5, 0))

    def add_output(self, text):
        """
        Add text to the output textbox
        Parameters:
            text (str): The text to be added to the output textbox
        """

        self.output.configure(state='normal')
        self.output.insert(
            customtkinter.END, text)
        self.output.see(customtkinter.END)
        self.output.configure(state='disabled')
        self.background.update()

    def update(self, event=None):
        """
        The function that downloads and installs the update
        Parameters:
            event (_type_): The event that triggered the function call. This is usually an event such as a button press
            and is automatically passed by the function call. Defaults to `None`.
        """

        self.updating = True
        self.button1.destroy()
        self.button2.destroy()
        self.button_grid.destroy()
        self.label2.destroy()

        self.output = customtkinter.CTkTextbox(self.background)
        self.output.pack(padx=5, pady=5, fill=customtkinter.BOTH, expand=True)
        self.output.configure(state='disabled')

        self.add_output("Prepairing update...\n\n")
        time.sleep(0.5)

        # Prepare download directory
        temp_dir = tempfile.gettempdir()
        download_path = os.path.join(os.path.join(os.path.join(
            temp_dir, "Proxy Settings"), "Updates"), f"Update {self.parent.latest_version}")
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        self.add_output(f"Download directory created at:\n{download_path}\n\n")

        url = "https://api.github.com/repos/infinitel8p/proxy-settings/releases"
        try:
            # Fetch release information
            releases_response = requests.get(url)
            releases_data = json.loads(releases_response.text)
            assets_response = requests.get((releases_data[0]["assets_url"]))
            assets_data = json.loads(assets_response.text)
            download_url = assets_data[0]["browser_download_url"]

            # Prepare for downloading
            response = requests.get(download_url, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # No content length header
                self.add_output(
                    "Cannot determine file size for progress tracking.\n\n")
                open(os.path.join(download_path, "Proxy Settings.exe"),
                     'wb').write(response.content)
            else:
                # Create and display the progress bar
                total_length = int(total_length)
                downloaded = 0
                self.progress_bar = customtkinter.CTkProgressBar(
                    self.background)
                self.progress_bar.pack(padx=5, pady=(
                    0, 5), fill=customtkinter.X, expand=True)
                self.add_output("Downloading new release...\n\n")

                # Download with progress update
                with open(os.path.join(download_path, "Proxy Settings.exe"), 'wb') as f:
                    for data in response.iter_content(chunk_size=4096):
                        downloaded += len(data)
                        f.write(data)
                        self.progress_bar.set(downloaded / total_length)
                        self.background.update_idletasks()  # Update the UI to reflect progress

            # log successful download of new .exe
            self.add_output(f"Downloaded update to:\n{download_path}\n\n")
            time.sleep(0.5)

        except (KeyError, IndexError, requests.exceptions.RequestException) as e:
            self.add_output(
                f"Error during download: {e}\n\nClosing setup in 5 sec...")
            time.sleep(5)
            self.destroy()

        # log creation of updater files
        self.add_output("Creating update handlers...\n\n")
        time.sleep(0.5)

        # create updater.ps1
        with open(os.path.join(download_path, "updater.ps1"), "w") as outfile:
            outfile.write(f"""echo "Closing Proxy Settings.exe.."
Start-Sleep 2
taskkill /F /IM "Proxy Settings.exe" /T
echo "Copying Proxy Settings.exe from {download_path} -> {os.path.join(os.path.dirname(sys.executable), 'Proxy Settings_1.exe')}..."
Start-Sleep 1
Copy-Item -Path "{os.path.join(download_path, "Proxy Settings.exe")}" -Destination "{os.path.join(os.path.dirname(sys.executable), "Proxy Settings_1.exe")}" -Force
echo "Deleting old executable..."
Start-Sleep 1
Remove-Item "{os.path.join(os.path.dirname(sys.executable), "Proxy Settings.exe")}"
echo "Renaming Proxy Settings_1.exe to Proxy Settings.exe..."
Start-Sleep 1
Rename-Item "{os.path.join(os.path.dirname(sys.executable), "Proxy Settings_1.exe")}" "{os.path.join(os.path.dirname(sys.executable), "Proxy Settings.exe")}"
echo "Launching Proxy Settings.exe..."
Start-Sleep 3
start "{os.path.join(os.path.dirname(sys.executable), "Proxy Settings.exe")}"
echo ""
echo "Update finished!"
echo "You can close this window now."
Exit""")
            outfile.close()

        # log successful creation of updater.ps1
        self.add_output("updater.ps1 successfully created!\n\n")
        time.sleep(0.5)

        # create updater.bat
        with open(os.path.join(download_path, "updater.bat"), "w") as outfile:
            outfile.write(
                f"""PowerShell -File "{os.path.join(download_path, "updater.ps1")}"\nexit""")
            outfile.close()

        # log successful creation of updater.bat
        self.add_output("updater.bat successfully created!\n\n")
        time.sleep(0.5)

        # log update start in 5 sek
        self.add_output("Starting update in 5 seconds!\n\n")
        time.sleep(0.5)

        # log estimated time
        self.add_output("Estimated update time: 10-15 sec.\n\n")
        time.sleep(2.5)

        # launch update
        subprocess.Popen(
            f"""start cmd /k "{os.path.join(download_path, 'updater.bat')}" """, shell=True)
        self.destroy()
