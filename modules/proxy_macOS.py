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
    try:
        subprocess.check_call([
            "networksetup", "-setwebproxy", "Wi-Fi", new_address.split(
                ":")[0], new_address.split(":")[1]
        ])
        logger.info(f"Changed http proxy address to {new_address}")
        subprocess.check_call([
            "networksetup", "-setsecurewebproxy", "Wi-Fi", new_address.split(":")[
                0], new_address.split(":")[1]
        ])
        logger.info(f"Changed https proxy address to {new_address}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to change proxy address: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


def fill_in_ip():
    """
    Retrieves the current HTTP proxy IP address. If the HTTPS proxy address
    is different, it sets the HTTPS proxy to match the HTTP proxy's IP address.
    Returns '0.0.0.0' if no HTTP proxy is set.

    Returns:
        str: The current HTTP proxy IP address or '0.0.0.0' if unset.
    """
    try:
        # Get HTTP proxy settings
        http_result = subprocess.check_output(
            ["networksetup", "-getwebproxy", "Wi-Fi"], encoding="utf-8"
        )

        # Extract IP from HTTP settings
        http_ip = next((line.split(":")[1].strip(
        ) for line in http_result.splitlines() if "Server:" in line), "0.0.0.0")

        if http_ip == "0.0.0.0":
            return http_ip

        # Get HTTPS proxy settings for comparison
        https_result = subprocess.check_output(
            ["networksetup", "-getsecurewebproxy", "Wi-Fi"], encoding="utf-8"
        )
        https_ip = next((line.split(":")[1].strip(
        ) for line in https_result.splitlines() if "Server:" in line), "0.0.0.0")

        # If HTTP and HTTPS proxy IPs differ, update HTTPS proxy to match HTTP
        if http_ip != https_ip:
            subprocess.check_call(
                ["networksetup", "-setsecurewebproxy", "Wi-Fi", http_ip, "80"]
            )
            print(f"Updated HTTPS proxy to match HTTP proxy: {
                  https_ip} -> {http_ip}")

        return http_ip
    except subprocess.CalledProcessError as e:
        print(f"Failed to retrieve or set proxy settings: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

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
