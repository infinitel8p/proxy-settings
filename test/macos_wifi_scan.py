import objc
from CoreLocation import CLLocationManager
import logging

location_manager = CLLocationManager.alloc().init()
location_manager.requestWhenInUseAuthorization()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

fh = logging.FileHandler('/Users/xpeng/Downloads/logging.log')
fh.setLevel(logging.DEBUG)


ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

if __name__ == '__main__':
    bundle_path = '/System/Library/Frameworks/CoreWLAN.framework'
    objc.loadBundle('CoreWLAN',
                    bundle_path=bundle_path,
                    module_globals=globals())
    iface = CWInterface.interface()
    logger.info(str(iface.interfaceName()))
    logger.info(iface.ssid())
    networks, error = iface.scanForNetworksWithSSID_error_(None, None)
    for network in networks:
        logger.info(network.ssid())
