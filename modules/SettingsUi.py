import os
import json
import logging
import tempfile
import customtkinter


class SettingsUi(customtkinter.CTkFrame):
    def __init__(self, parent, version):

        # Main Frame
        super().__init__(master=parent)
        self.configure(fg_color="transparent")
        self.root = parent

        # set log folder path or create it if it does not exist
        temp_dir = tempfile.gettempdir()
        self.log_path = os.path.join(os.path.join(
            os.path.dirname(temp_dir), 'Proxy Settings'), "logs")
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

        # default settings
        settings_json = {"log_path": ""}

        # open the settings.json and if FileNotFoundError then create it
        try:
            with open(os.path.join(self.log_path, "settings.json"), "r") as infile:
                json_object = json.load(infile)
        except FileNotFoundError:
            with open(os.path.join(self.log_path, "settings.json"), "w+") as outfile:
                json.dump(settings_json, outfile)
            with open(os.path.join(self.log_path, "settings.json"), "r") as infile:
                json_object = json.load(infile)

        # Save Button
        self.save_button = customtkinter.CTkButton(
            self, text="Save", command=lambda: self.save_settings("log_path"))
        self.save_button.pack()

        # Version Label
        self.version_label = customtkinter.CTkLabel(
            self, text=f"version {version}", text_color="grey", font=("Arial", 10))
        self.version_label.pack(side=customtkinter.BOTTOM)

    def save_settings(self, new_value):
        """
        Dumps changes into the `settings.json` file, located in os.path.join(log_path, "settings.json").

        Args:
            new_value (_type_): Specific value to save into the json file. This value represents the configuration, preference or setting that the user has selected or modified and should be saved.
        """

        # create settings string
        settings_json = {
            "log_path": f"{self.log_path}",
        }

        # write settings to file
        with open(os.path.join(self.log_path, "settings.json"), "r") as infile:
            settings_data = json.load(infile)
        # add missing key
            settings_data[new_value] = settings_json[new_value]
        with open(os.path.join(self.log_path, "settings.json"), "w") as outfile:
            json.dump(settings_data, outfile)

        logging.info(
            f"Settings updated → {new_value} = {settings_json[new_value]}")
