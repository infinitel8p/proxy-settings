pyinstaller --onefile --noconfirm --windowed --icon "/Users/ludo/Documents/proxy-settings/images/verbindung.ico" --name "Proxy Settings" --add-data "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/customtkinter:customtkinter/" --add-data "/Users/ludo/Documents/proxy-settings/images:images" --add-data "/Users/ludo/Documents/proxy-settings/modules:modules" --add-data "/Users/ludo/Documents/proxy-settings/themes:themes" main.pyw --clean