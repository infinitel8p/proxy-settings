import objc
from CoreLocation import CLLocationManager
import logging

location_manager = CLLocationManager.alloc().init()
location_manager.requestWhenInUseAuthorization()

logger = logging.getLogger()
logger.setLevel(logging.INFO)


ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

if __name__ == '__main__':
    bundle_path = '/System/Library/Frameworks/CoreWLAN.framework'
    objc.loadBundle('CoreWLAN',
                    bundle_path=bundle_path,
                    module_globals=globals())
    iface = CWInterface.interface()
    print(
        f"Interface {str(iface.interfaceName())} - Connected to: {iface.ssid()}\n")
    networks, error = iface.scanForNetworksWithSSID_error_(None, None)
    for network in networks:
        logger.info(network.ssid())
