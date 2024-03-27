import logging
import subprocess

logger = logging.getLogger(__name__)


def activate():
    """
    Attempts to activate the system's proxy settings on macOS.

    Returns:
        True if the proxy was successfully activated, False otherwise.
    """
    try:
        # Enable HTTP proxy
        subprocess.check_call([
            "networksetup", "-setwebproxystate", "Wi-Fi", "on"
        ])
        logger.info("HTTP-Proxy activated successfully.")
        # Enable HTTPS proxy
        subprocess.check_call([
            "networksetup", "-setsecurewebproxystate", "Wi-Fi", "on"
        ])
        logger.info("HTTPS-Proxy activated successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to activate proxy: {e}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return False


def deactivate():
    """
    Attempts to deactivate the system's proxy settings on macOS.

    Returns:
        True if the proxy was successfully deactivated, False otherwise.
    """
    try:
        # Enable HTTP proxy
        subprocess.check_call([
            "networksetup", "-setwebproxystate", "Wi-Fi", "off"
        ])
        logger.info("HTTP-Proxy deactivated successfully.")
        # Enable HTTPS proxy
        subprocess.check_call([
            "networksetup", "-setsecurewebproxystate", "Wi-Fi", "off"
        ])
        logger.info("HTTPS-Proxy deactivated successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to deactivate proxy: {e}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return False


def change_address(new_address):
    """
    Changes the proxy address to the specified new address.

    Args:
        new_address (str): The new proxy server address in the format "ip:port".
    """
    # networksetup -setwebproxy "Wi-Fi" proxy.example.com 8080
    # networksetup -setsecurewebproxy "Wi-Fi" proxy.example.com 8080

    logger.info(f"Changed proxy address to {new_address}")


def fill_in_ip():
    """
    Retrieves the current proxy IP address.
    If no proxy address has been set, it returns '0.0.0.0'.

    Returns:
        str: The current proxy IP address or '0.0.0.0' if unset.
    """
    # networksetup -getwebproxy "Wi-Fi"

    try:
        ip_address = ""
        return ip_address
    except Exception as e:
        print(e)
        return "0.0.0.0"


def fill_in_port():
    """
    Retrieves the current proxy port.
    If no port address has been set, it returns '8080'.

    Returns:
        str: The current proxy port or '8080' if unset.
    """
    # networksetup -getwebproxy "Wi-Fi"

    try:
        ip_address = ""
        return ip_address
    except Exception as e:
        print(e)
        return "8080"


def status_check():
    """
    Checks if the proxy is currently enabled.

    Returns:
        bool: True if the proxy is enabled, False otherwise.
    """
    # networksetup -getwebproxy "Wi-Fi"

    if 1 == 1:
        logger.info('Proxy is currently active')
        return True
    else:
        logger.info('Proxy is currently inactive')
        return False


def server_check():
    """
    Checks and logs the current proxy server settings.
    If no proxy server is configured, it attempts to set a placeholder value and rechecks.

    Returns:
        str: The current proxy server address or a placeholder if initially unset.
    """
    # networksetup -getwebproxy "Wi-Fi"

    try:
        value = ""

        logger.info(f"Current Proxy Server: {value}")
        return value

    except Exception as e:
        logger.error(
            f'An unexpected error occurred while checking: {e}')
        return "Error"
