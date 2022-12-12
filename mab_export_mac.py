# export mab macs to csv
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Task, Result
import keyring
import csv
from netaddr import EUI, mac_unix_expanded

nr = InitNornir(config_file="config.yaml")

# credentials
un = "username"
pw = keyring.get_password('ssh', 'username')

nr.inventory.defaults.username = un
nr.inventory.defaults.password = pw

def multiple_tasks(task: Task):
    task.run(
        task=netmiko_send_command, command_string="show interface switchport", use_textfsm=True
    )

    task.run(
        task=netmiko_send_command, command_string="show mac address-table", use_textfsm=True
    )

results = nr.run(
    task=multiple_tasks
)

medlist1 = []

for i in results:
    if type(results[i][1].result) == str:
        continue
    for k in results[i][1].result:
        if k.get('admin_mode') == 'static access':
            if type(results[i][2].result) == str:
                continue
            for l in results[i][2].result:
                if l.get('destination_port')[0] == k.get('interface'):
                    dct = {}
                    dct["MacAddress"] = EUI(l.get('destination_address'),dialect=mac_unix_expanded)
                    dct["EndPointPolicy"] = ''
                    dct["IdentityGroup"] = 'MAB_TEST'
                    medlist1.append(dct)

headlist1 = []

for key in medlist1[0].keys():
    headlist1.append(key)

myfile = open('output.csv', 'w')
writer = csv.writer(myfile)
writer.writerow(headlist1)
for dictionary in medlist1:
    writer.writerow(dictionary.values())
myfile.close()
