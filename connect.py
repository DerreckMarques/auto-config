#auto-config
import sys
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.utils.config import Config

hostname = input("Device hostname: ")
junos_username = input("Junos OS username: ")
junos_password = getpass("Junos OS or SSH key password: ")

dev = Device(host=hostname, user=junos_username, passwd=junos_password)
try:
    dev.open()
except ConnectError as err:
    print ("Cannot connect to device: {0}".format(err))
    sys.exit(1)
except Exception as err:
    print (err)
    sys.exit(1)

with Config(dev, mode='private') as cu:  
        cu.load('set system services netconf traceoptions file test.log', format='set')
        cu.pdiff()
        cu.commit(confirm=10)
#print (dev.facts)
dev.close()
