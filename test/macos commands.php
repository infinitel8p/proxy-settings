networksetup -listnetworkserviceorder
networksetup -listallnetworkservices
networksetup -listallhardwareports
networksetup -detectnewhardware
networksetup -getmacaddress <hardwareport or device name>
networksetup -getcomputername
networksetup -setcomputername <name>
networksetup -getinfo <networkservice>
networksetup -setmanual <networkservice> <ip> <subnet> <router>
networksetup -setdhcp <networkservice> [clientid]
networksetup -setbootp <networkservice>
networksetup -setmanualwithdhcprouter <networkservice> <ip> 
networksetup -getadditionalroutes <networkservice>
networksetup -setadditionalroutes <networkservice> [ <dest> <mask> <gateway> ]*
networksetup -setv4off <networkservice>
networksetup -setv6off <networkservice>
networksetup -setv6automatic <networkservice>
networksetup -setv6LinkLocal <networkservice>
networksetup -setv6manual <networkservice> <networkservice> <address> <prefixlength> <router>
networksetup -getv6additionalroutes <networkservice>
networksetup -setv6additionalroutes <networkservice> [ <dest> <prefixlength> <gateway> ]*
networksetup -getdnsservers <networkservice>
networksetup -setdnsservers <networkservice> <dns1> [dns2] [...] 
networksetup -getsearchdomains <networkservice>
networksetup -setsearchdomains <networkservice> <domain1> [domain2] [...] 
networksetup -create6to4service <newnetworkservicename> 
networksetup -set6to4automatic <networkservice> 
networksetup -set6to4manual <networkservice> <relayaddress> 
networksetup -getwebproxy <networkservice>
networksetup -setwebproxy <networkservice> <domain> <port number> <authenticated> <username> <password>
networksetup -setwebproxystate <networkservice> <on off>
networksetup -getsecurewebproxy <networkservice>
networksetup -setsecurewebproxy <networkservice> <domain> <port number> <authenticated> <username> <password>
networksetup -setsecurewebproxystate <networkservice> <on off>
networksetup -getsocksfirewallproxy <networkservice>
networksetup -setsocksfirewallproxy <networkservice> <domain> <port number> <authenticated> <username> <password>
networksetup -setsocksfirewallproxystate <networkservice> <on off>
networksetup -getproxybypassdomains <networkservice>
networksetup -setproxybypassdomains <networkservice> <domain1> [domain2] [...] 
networksetup -getproxyautodiscovery <networkservice>
networksetup -setproxyautodiscovery <networkservice> <on off>
networksetup -getairportnetwork <device name>
networksetup -setairportnetwork <device name> <network> [password]
networksetup -getairportpower <device name>
networksetup -setairportpower <device name> <on off>
networksetup -listpreferredwirelessnetworks <device name>
networksetup -addpreferredwirelessnetworkatindex <device name> <network> <index> <security type> [password]
networksetup -removepreferredwirelessnetwork <device name> <network>
networksetup -removeallpreferredwirelessnetworks <device name>
networksetup -getnetworkserviceenabled <networkservice>
networksetup -setnetworkserviceenabled <networkservice> <on off>
networksetup -createnetworkservice <newnetworkservicename> <hardwareport>
networksetup -renamenetworkservice <networkservice> <newnetworkservicename>
networksetup -duplicatenetworkservice <networkservice> <newnetworkservicename>
networksetup -removenetworkservice <networkservice>
networksetup -ordernetworkservices <service1> <service2> <service3> <...>
networksetup -getMTU <hardwareport or device name>
networksetup -setMTU <hardwareport or device name> <value>
networksetup -listvalidMTUrange <hardwareport or device name>
networksetup -getmedia <hardwareport or device name>
networksetup -setmedia <hardwareport or device name> <subtype> [option1] [option2] [...]
networksetup -listvalidmedia <hardwareport or device name>
networksetup -createVLAN <VLAN name> <parent device name> <tag>
networksetup -deleteVLAN <VLAN name> <parent device name> <tag>
networksetup -listVLANs
networksetup -listdevicesthatsupportVLAN
networksetup -isBondSupported <hardwareport>
networksetup -createBond <bondname> <hardwareport1> <hardwareport2> <...>
networksetup -deleteBond <bonddevicename>
networksetup -addDeviceToBond <hardwareport> <bonddevicename>
networksetup -removeDeviceFromBond <hardwareport> <bonddevicename>
networksetup -listBonds
networksetup -showBondStatus <bonddevicename>
networksetup -listpppoeservices
networksetup -showpppoestatus <service name ie., MyPPPoEService>
networksetup -createpppoeservice <device name ie., en0> <service name> <account name> <password> [pppoe service name]
networksetup -deletepppoeservice <service name>
networksetup -setpppoeaccountname <service name> <account name>
networksetup -setpppoepassword <service name> <password>
networksetup -connectpppoeservice <service name>
networksetup -disconnectpppoeservice <service name>
networksetup -getcurrentlocation
networksetup -listlocations
networksetup -createlocation <location name> [populate]
networksetup -deletelocation <location name>
networksetup -switchtolocation <location name>
networksetup -listalluserprofiles
networksetup -listloginprofiles <service name>
networksetup -enablesystemprofile <service name> <on off>
networksetup -enableloginprofile <service name> <profile name> <on off>
networksetup -enableuserprofile <profile name> <on off>
networksetup -import8021xProfiles <service name> <file path>
networksetup -export8021xProfiles <service name> <file path> <yes no>
networksetup -export8021xUserProfiles <file path> <yes no>
networksetup -export8021xLoginProfiles <service name> <file path> <yes no>
networksetup -export8021xSystemProfile <service name> <file path> <yes no>
networksetup -settlsidentityonsystemprofile <service name> <file path> <passphrase>
>networksetup -settlsidentityonuserprofile <profile name> <file path> <passphrase>networksetup -deletesystemprofile <service name> 
networksetup -deleteloginprofile <service name> <profile name>
networksetup -deleteuserprofile <profile name>
networksetup -version
networksetup -help
networksetup -printcommands