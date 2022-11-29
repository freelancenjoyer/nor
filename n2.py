from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
import keyring

pw = keyring.get_password('ssh', 'username')

nr = InitNornir(config_file="config.yaml")

nr.inventory.defaults.username = "username"
nr.inventory.defaults.password = pw


result = nr.run(task=netmiko_send_command, command_string="show cdp neighbor", use_textfsm=True)

print_result(result)
