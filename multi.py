# simple script to test multiple show commands
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Task, Result
import keyring

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

print_result(results)
