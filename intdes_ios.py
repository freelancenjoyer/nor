# performs multiple commands on ios devices such as "show ip int br" and "show int des"
# adds description to show ip int br and dumps it into csv
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Task, Result
from collections import OrderedDict
import keyring
import csv

pw = keyring.get_password('ssh', 'username')

nr = InitNornir(config_file="config.yaml")

nr.inventory.defaults.username = "username"
nr.inventory.defaults.password = pw

def multiple_tasks(task: Task):
    task.run(
        task=netmiko_send_command, command_string="show ip int br", use_textfsm=True
    )

    task.run(
        task=netmiko_send_command, command_string="show int des", use_textfsm=True
    )

results = nr.run(
    task=multiple_tasks
)

medlist = []

for i in results:
    if type(results[i][1].result) == str:
        continue
    for (a, b) in zip(results[i][1].result, results[i][2].result):
        ordict = OrderedDict(a)
        ordict.update({'description': b.get('descrip')})
        ordict.move_to_end('description', last = False)
        ordict.update({'hostname': i})
        ordict.move_to_end('hostname', last = False)
        medlist.append(ordict)

headlist = []

for key in medlist[0].keys():
    headlist.append(key)

myfile = open('output.csv', 'w')
writer = csv.writer(myfile)
writer.writerow(headlist)
for dictionary in medlist:
    writer.writerow(dictionary.values())
myfile.close()

#print_result(results)
