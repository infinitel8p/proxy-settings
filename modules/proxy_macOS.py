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
        # Disable HTTP proxy
        subprocess.check_call([
            "networksetup", "-setwebproxystate", "Wi-Fi", "off"
        ])
        logger.info("HTTP-Proxy deactivated successfully.")
        # Disable HTTPS proxy
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
        proxy_status = status_check()

        subprocess.check_call([
            "networksetup", "-setwebproxy", "Wi-Fi", new_address.split(
                ":")[0], new_address.split(":")[1]
        ])
        logger.info(f"Changed http proxy address to {new_address}")
        subprocess.check_call([
            "networksetup", "-setsecurewebproxy", "Wi-Fi", new_address.split(":")[
                0], new_address.split(":")[1]
        ])

        if not proxy_status:
            # reset state to previous
            deactivate()

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
            ["networksetup", "-getwebproxy", "Wi-Fi"], encoding="utf-8")
        http_ip = next((line.split(":")[1].strip(
        ) for line in http_result.splitlines() if "Server:" in line), "0.0.0.0")

        # Get HTTPS proxy settings for comparison
        https_result = subprocess.check_output(
            ["networksetup", "-getsecurewebproxy", "Wi-Fi"], encoding="utf-8")
        https_ip = next((line.split(":")[1].strip(
        ) for line in https_result.splitlines() if "Server:" in line), "0.0.0.0")

        # If HTTP and HTTPS proxy IPs differ, update HTTPS proxy to match HTTP
        proxy_status = status_check()
        if http_ip != https_ip:
            subprocess.check_call(
                ["networksetup", "-setsecurewebproxy", "Wi-Fi", http_ip, "8080"])
            logger.info(
                f"Updated HTTPS proxy IP to match HTTP proxy IP: {https_ip} -> {http_ip}")

        if not proxy_status:
            # reset state to previous
            deactivate()

        return http_ip
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to retrieve or set proxy settings: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    return "0.0.0.0"


def fill_in_port():
    """
    Retrieves the current HTTP proxy Port address. If the HTTPS proxy address
    is different, it sets the HTTPS Port to match the HTTP proxy's Port address.
    Returns '0.0.0.0' if no HTTP proxy is set.

    Returns:
        str: The current proxy port or '8080' if unset.
    """
    # networksetup -getwebproxy "Wi-Fi"
    try:
        # Get HTTP proxy settings
        http_result = subprocess.check_output(
            ["networksetup", "-getwebproxy", "Wi-Fi"], encoding="utf-8")
        http_ip = next((line.split(":")[1].strip(
        ) for line in http_result.splitlines() if "Server:" in line), "0.0.0.0")
        http_port = next((line.split(":")[1].strip(
        ) for line in http_result.splitlines() if "Port:" in line), "8080")

        # Get HTTPS proxy settings for comparison
        https_result = subprocess.check_output(
            ["networksetup", "-getsecurewebproxy", "Wi-Fi"], encoding="utf-8")
        https_port = next((line.split(":")[1].strip(
        ) for line in https_result.splitlines() if "Port:" in line), "8080")

        # If HTTP and HTTPS proxy IPs differ, update HTTPS proxy to match HTTP
        proxy_status = status_check()

        if http_port != https_port:
            subprocess.check_call(
                ["networksetup", "-setsecurewebproxy", "Wi-Fi", http_ip, "8080"])
            logger.info(
                f"Updated HTTPS proxy to match HTTP proxy: {https_port} -> {http_port}")

        if not proxy_status:
            # reset state to previous
            deactivate()

        return http_port
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to retrieve or set proxy settings: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    return "8080"


def status_check():
    """
    Checks if the proxy is currently enabled.

    Returns:
        bool: True if the proxy is enabled, False otherwise.
    """

    try:
        # Get HTTP proxy settings
        http_result = subprocess.check_output(
            ["networksetup", "-getwebproxy", "Wi-Fi"], encoding="utf-8")
        http_enabled = next((line.split(":")[1].strip(
        ) for line in http_result.splitlines() if "Enabled:" in line), "No")

        # Get HTTPS proxy settings for comparison
        https_result = subprocess.check_output(
            ["networksetup", "-getsecurewebproxy", "Wi-Fi"], encoding="utf-8")
        https_enabled = next((line.split(":")[1].strip(
        ) for line in https_result.splitlines() if "Enabled:" in line), "No")

        if http_enabled != https_enabled:
            subprocess.check_call(
                ["networksetup", "-setsecurewebproxystate", "Wi-Fi", http_enabled])
            logger.info(
                f"Updated HTTPS proxy to match HTTP proxy: {https_enabled} -> {http_enabled}")

        if http_enabled == "Yes":
            logger.info('Proxy is currently active')
            return True
        else:
            logger.info('Proxy is currently inactive')

    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to retrieve or set proxy settings: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    return False


def server_check():
    """
    Checks and logs the current proxy server settings.
    If no proxy server is configured, it attempts to set a placeholder value and rechecks.

    Returns:
        str: The current proxy server address or a placeholder if initially unset.
    """
    try:
        # Check the current proxy settings
        check_result = subprocess.check_output(
            ["networksetup", "-getwebproxy", "Wi-Fi"], encoding="utf-8")

        server = "0.0.0.0"
        port = "0"

        # Parse the command output for Server and Port
        for line in check_result.splitlines():
            if "Server:" in line:
                server = line.split(":")[1].strip()
            elif "Port:" in line:
                port = line.split(":")[1].strip()

        # Check if the proxy server is not set or set to the default placeholder
        if server == "0.0.0.0" or not server:
            logger.warning("No Proxy Server found or set to default!")
            proxy_status = status_check()

            # Proxy is not properly set, proceed to set the default values
            subprocess.check_output(
                ["networksetup", "-setwebproxy", "Wi-Fi", "0.0.0.0", "0"], encoding="utf-8")
            logger.info("Set the HTTP proxy server to 0.0.0.0:0")
            subprocess.check_output(
                ["networksetup", "-setsecurewebproxy", "Wi-Fi", "0.0.0.0", "0"], encoding="utf-8")
            logger.info("Set the HTTPS proxy server to 0.0.0.0:0")

            if not proxy_status:
                # reset state to previous
                deactivate()

            return "0.0.0.0:0"
        else:
            # Proxy is properly set, log the server address
            logger.info(f"Current Proxy Server: {server}:{port}")
            return f"{server}:{port}"
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to retrieve or set proxy settings: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    return "0.0.0.0:0"
