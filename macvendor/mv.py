from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from collections import OrderedDict
from mac_vendor_lookup import MacLookup
import keyring
import csv

pw = keyring.get_password('ssh', 'peps')

nr = InitNornir(config_file="config.yaml")

nr.inventory.defaults.username = "peps"
nr.inventory.defaults.password = pw

result = nr.run(task=netmiko_send_command, command_string="show mac address-table", use_textfsm=True)

medlist = []

for i in result:
    if type(result[i].result) == str:
        continue
    for k in result[i].result:
        ordict = OrderedDict(k)
        ordict.update({'hostname': i})
        ordict.update({'maclookup': "unknown"})
        ordict.move_to_end('hostname', last = False)
        medlist.append(ordict)

for i in medlist:
    try:
        i['maclookup'] = MacLookup().lookup(i['destination_address'])
    except KeyError as e:
        i['maclookup'] = "UNKNOWN"

headlist = []

for key in medlist[0].keys():
    headlist.append(key)


myfile = open('output.csv', 'w')
writer = csv.writer(myfile)
writer.writerow(headlist)
for dictionary in medlist:
    writer.writerow(dictionary.values())
myfile.close()

print(medlist)
