import subprocess
import logging
import win32com.shell.shell as shell


proxy_server_address = 0
proxy_port = 0
deactivate = 'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f'
activate = 'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f'
change_address = f'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d {proxy_server_address}:{proxy_port} /f'

#shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c ' + deactivate)


def status_check():
    # check current regkey value for proxy
    regkey_check = subprocess.Popen(
        'reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable', shell=True, stdout=subprocess.PIPE)
    regkey_check_return = regkey_check.stdout.read().split()

    if regkey_check_return[-1] == b'0x0':
        print('Proxy is currently inactive')
        logging.info('Proxy is currently inactive')
        return
    if regkey_check_return[-1] == b'0x1':
        print('Proxy is currently active')
        logging.info('Proxy is currently active')
        return
    else:
        print(
            f"Debug: {regkey_check_return[-1]}, {type(regkey_check_return[-1])}")


def server_check():
    # check current regkey value for proxy
    regkey_check = subprocess.Popen(
        'reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer', shell=True, stdout=subprocess.PIPE)
    regkey_check_return = regkey_check.stdout.read().split()

    # try to convert outputted bytes to string
    try:
        value = regkey_check_return[-1].decode("utf-8")
        # if output was indeed bytes return its value which now should be a string to main.py
        if type(regkey_check_return[-1]) is bytes:
            return value
        else:
            # if the output was not in bytes print its value and type for debugging purposes
            print(
                f"Debug: {regkey_check_return[-1]}, {type(regkey_check_return[-1])}")

    # handle error most likely resulting from missing reg key
    except:
        # create missing reg key with placeholder address
        print("Creating Registry key, setting proxy address...")
        create_proxy_regsz = subprocess.Popen(
            f'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d 0.0.0.0:0 /f', shell=True, stdout=subprocess.PIPE)
        create_proxy_regsz_return = create_proxy_regsz.stdout.read()
        print(
            f'{create_proxy_regsz_return.decode("utf-8")}Set Proxy address to: 0.0.0.0:0')

        # try to read the value again
        regkey_check2 = subprocess.Popen(
            'reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer', shell=True, stdout=subprocess.PIPE)
        regkey_check_return2 = regkey_check2.stdout.read().split()

        # convert outputted bytes to string
        value = regkey_check_return2[-1].decode("utf-8")
        if type(regkey_check_return2[-1]) is bytes:
            return value
        else:
            print(
                f"Debug: {regkey_check_return2[-1]}, {type(regkey_check_return2[-1])}")
