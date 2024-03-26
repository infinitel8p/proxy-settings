import logging
import winreg

logger = logging.getLogger(__name__)


def activate():
    """
    Attempts to activate the system's proxy settings by modifying the Windows Registry.
    If the script does not have sufficient permissions to modify the registry, it logs a message
    instructing the user to run the script with administrative privileges.

    Returns:
        True if the proxy was successfully activated, False otherwise.
    """
    try:
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            0, winreg.KEY_WRITE
        )

        # Set the ProxyEnable value to 1 (activated)
        winreg.SetValueEx(registry_key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(registry_key)

        logger.info('Proxy activated successfully')
        return True
    except PermissionError as e:
        logger.error(
            f"Insufficient permissions to change the registry. Please run this program as an administrator. Error: {e}")
        return False
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}')
        return False


def deactivate():
    """
    Attempts to deactivate the system's proxy settings by modifying the Windows Registry.
    If the script does not have sufficient permissions to modify the registry, it logs a message
    instructing the user to run the script with administrative privileges.

    Returns:
        True if the proxy was successfully deactivated, False otherwise.
    """

    try:
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, winreg.KEY_WRITE)

        # Set the ProxyEnable value to 0 (deactivated)
        winreg.SetValueEx(registry_key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(registry_key)

        logger.info('Deactivated Proxy successfully')
        return True
    except PermissionError as e:
        logger.error(
            "Insufficient permissions to change the registry. Please run this program as an administrator.")
        return False
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        return False


def change_address(new_address):
    """
    Changes the proxy address in the Windows Registry to the specified new address.

    Args:
        new_address (str): The new proxy server address in the format "ip:port".
    """
    try:
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings",
            0, winreg.KEY_WRITE
        )

        winreg.SetValueEx(registry_key, "ProxyServer",
                          0, winreg.REG_SZ, new_address)
        winreg.CloseKey(registry_key)

        logger.info(f"Changed proxy address to {new_address}")
    except Exception as e:
        logger.error(f"Failed to change proxy address: {e}")


def fill_in_ip():
    """
    Retrieves the current proxy IP address from the Windows Registry.
    If no proxy address has been set, it returns '0.0.0.0'.

    Returns:
        str: The current proxy IP address or '0.0.0.0' if unset.
    """
    try:
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings",
            0, winreg.KEY_READ
        )

        proxy_server_ip, _ = winreg.QueryValueEx(
            registry_key, "ProxyServer")
        winreg.CloseKey(registry_key)

        # If the ProxyServer key exists, extract the IP address
        ip_address = proxy_server_ip.split(
            ":")[0] if proxy_server_ip else "0.0.0.0"
        return ip_address
    except Exception as e:
        print(e)  # printing e to make use of the exception
        return "0.0.0.0"


def fill_in_port():
    """
    Retrieves the current proxy port from the Windows Registry.
    If no port address has been set, it returns '8080'.

    Returns:
        str: The current proxy port or '8080' if unset.
    """
    try:
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings",
            0, winreg.KEY_READ
        )

        proxy_server_port, _ = winreg.QueryValueEx(
            registry_key, "ProxyServer")
        winreg.CloseKey(registry_key)

        # If the ProxyServer key exists, extract the port
        ip_address = proxy_server_port.split(
            ":")[-1] if proxy_server_port else "8080"
        return ip_address
    except Exception as e:
        return "8080"


def status_check():
    """
    Checks if the proxy is currently enabled by querying the Windows Registry.

    Returns:
        bool: True if the proxy is enabled, False otherwise.
    """
    try:
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            0, winreg.KEY_READ
        )

        value, _ = winreg.QueryValueEx(registry_key, "ProxyEnable")
        winreg.CloseKey(registry_key)

        if value == 1:
            logger.info('Proxy is currently active')
            return True
        else:
            logger.info('Proxy is currently inactive')
            return False

    except FileNotFoundError:
        # The ProxyEnable key does not exist
        logger.info("The ProxyEnable registry key does not exist.")
        return False
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}')
        return False


def server_check():
    """
    Checks and logs the current proxy server settings from the Windows Registry.
    If no proxy server is configured, it attempts to set a placeholder value and rechecks.

    Returns:
        str: The current proxy server address or a placeholder if initially unset.
    """
    try:
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            0, winreg.KEY_READ
        )

        # Query the value of the ProxyServer key
        value, _ = winreg.QueryValueEx(registry_key, "ProxyServer")
        winreg.CloseKey(registry_key)

        logger.info(f"Current Proxy Server: {value}")
        return value

    except FileNotFoundError:
        # The ProxyServer key does not exist, attempt to create it with a placeholder
        logger.warning("No Proxy Server found!")
        try:
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                0, winreg.KEY_WRITE
            )

            winreg.SetValueEx(registry_key, "ProxyServer",
                              0, winreg.REG_SZ, "0.0.0.0:0")
            winreg.CloseKey(registry_key)

            logger.info("Set ProxyServer address to: 0.0.0.0:0")
            return "0.0.0.0:0"

        except PermissionError as e:
            logger.error(
                "Insufficient permissions to change the registry. Please run this program as an administrator.")
            return "Permission Error"

        except Exception as e:
            logger.error(f'An unexpected error occurred: {e}')
            return "Error"

    except Exception as e:
        logger.error(
            f'An unexpected error occurred while checking the ProxyServer registry key: {e}')
        return "Error"
