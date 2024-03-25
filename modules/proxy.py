import logging
import subprocess
from win32com.shell import shell as shell
import pywintypes


proxy_server_query = r'reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer'
proxy_status_query = r'reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable'
deactivate_proxy = r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f'
activate_proxy = r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f'


logger = logging.getLogger(__name__)


def activate():
    """Activates the proxy by modifying the registry key value for the proxy.
    """
    try:
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe',
                             lpParameters='/c ' + activate_proxy)
    except pywintypes.error as e:
        if e.winerror == 1223:
            logger.warning('Activation cancelled by the user.')
            return False
        else:
            logger.error(f'An error occurred: {e}')
            return False
    logger.info('Activated Proxy')
    return True


def deactivate():
    """Deactivates the proxy by modifying the registry key value for the proxy.
    """
    try:
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe',
                             lpParameters='/c ' + deactivate_proxy)
    except pywintypes.error as e:
        if e.winerror == 1223:
            logger.warning('Deactivation cancelled by the user.')
            return False
        else:
            logger.error(f'An error occurred: {e}')
            return False
    logger.info('Deactivated Proxy')
    return True


def change_address(new_address):
    """Changes the proxy address in the Windows Registry to the specified new address.

    Args:
        new_address (str): The new proxy server address in the format "ip:port".
    """
    subprocess.run(
        fr'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d {new_address} /f', shell=True)
    logger.info(f"Changed proxy address to {new_address}")


def fill_in_ip():
    """Retrieves the current proxy IP address from the Windows Registry.
    If no proxy address has been set, it returns '0.0.0.0'.

    Returns:
        str: The current proxy IP address or '0.0.0.0' if unset.
    """
    try:
        value = subprocess.check_output(
            proxy_server_query).decode("utf-8").split()[-1].split(":")[0]
        return value
    except:
        value = "0.0.0.0"
        return value


def fill_in_port():
    """Retrieves the current proxy port from the Windows Registry.
    If no port address has been set, it returns '8080'.

    Returns:
        str: The current proxy port or '8080' if unset.
    """
    try:
        value = subprocess.check_output(
            proxy_server_query, shell=True).decode("utf-8").strip().split(":")[-1]
        return value
    except:
        value = "8080"
        return value


def status_check():
    """Checks if the proxy is currently enabled by querying the Windows Registry.

    Returns:
        bool: True if the proxy is enabled, False otherwise.
    """
    global logger
    # check current regkey value for proxy
    regkey_check = subprocess.Popen(
        proxy_status_query, shell=True, stdout=subprocess.PIPE)
    regkey_check_return = regkey_check.stdout.read().split()

    if regkey_check_return[-1] == b'0x0':
        logger.info('Proxy is currently inactive')
        return False
    if regkey_check_return[-1] == b'0x1':
        logger.info('Proxy is currently active')
        return True
    else:
        logger.debug(
            f"{regkey_check_return[-1]}, {type(regkey_check_return[-1])}")


def server_check():
    """Checks and logs the current proxy server settings from the Windows Registry.
    If no proxy server is configured, it attempts to set a placeholder value and rechecks.

    Returns:
        str: The current proxy server address or a placeholder if initially unset.
    """
    global logger
    # check current regkey value for proxy
    regkey_check = subprocess.Popen(
        proxy_server_query, shell=True, stdout=subprocess.PIPE)
    regkey_check_return = regkey_check.stdout.read().split()

    # try to convert outputted bytes to string
    try:
        value = regkey_check_return[-1].decode("utf-8")
        # if output was indeed bytes return its value which now should be a string to main.py
        if type(regkey_check_return[-1]) is bytes:
            logger.info(f"Current Proxy Server: {value}")
            return value
        else:
            # if the output was not in bytes log its value and type for debugging purposes
            logger.debug(
                f"{regkey_check_return[-1]}, {type(regkey_check_return[-1])}")

    # handle error most likely resulting from missing reg key
    except:
        # create missing reg key with placeholder address
        logger.warning("No Proxy Server found!")
        logger.info("Creating REG_SZ key...")
        logger.info("Setting proxy address...")
        create_proxy_regsz = subprocess.Popen(
            r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d 0.0.0.0:0 /f',
            shell=True, stdout=subprocess.PIPE)
        create_proxy_regsz_return = create_proxy_regsz.stdout.read().decode("utf-8").split()
        logger.info(" ".join(create_proxy_regsz_return))
        logger.info("Set Proxy address to: 0.0.0.0:0")

        # try to read the value again
        logging.info("Confirming Proxy Server...")
        regkey_check2 = subprocess.Popen(
            proxy_server_query, shell=True, stdout=subprocess.PIPE)
        regkey_check_return2 = regkey_check2.stdout.read().split()

        # convert outputted bytes to string
        value = regkey_check_return2[-1].decode("utf-8")
        if type(regkey_check_return2[-1]) is bytes:
            logger.info(f"Current Proxy Server: {value}")
            return value
        else:
            logger.debug(
                f"{regkey_check_return2[-1]}, {type(regkey_check_return2[-1])}")
